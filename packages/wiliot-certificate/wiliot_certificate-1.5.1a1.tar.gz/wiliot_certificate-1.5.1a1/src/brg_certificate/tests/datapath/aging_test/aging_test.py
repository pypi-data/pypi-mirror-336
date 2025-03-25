from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config
import brg_certificate.cert_data_sim as cert_data_sim


def send_get_HB(test):
    cert_config.send_brg_action(test, ag.ACTION_SEND_HB)
    test, HB_list = cert_common.scan_for_mgmt_pkts(test, [eval_pkt(f'Brg2GwHbV{test.active_brg.api_version}')])
    return HB_list

def calculate_aging_time(pacer_interval):
    return max(60, pacer_interval)

def calculate_sending_time(duplicates, delay, num_of_sim_tags):
    if delay <= 0.02:
        return duplicates*0.02*num_of_sim_tags
    else:
        actual_delay = max(delay, duplicates*(ag.PIXEL_SIM_MIN_CYCLE))
        actual_delay = actual_delay/1000
        return actual_delay*num_of_sim_tags

def combination_func(test, datapath_module, pacer_interval, num_of_sim_tags, aging_time):

    test = cert_config.brg_configure(test, fields=[BRG_PACER_INTERVAL], values=[pacer_interval], module=datapath_module)[0]
    if test.rc == TEST_FAILED and test.reason != TEST_PASSED:
        for i in range(2):
            if test.rc == TEST_PASSED:
                return test
            test = cert_config.brg_configure(test, fields=[BRG_PACER_INTERVAL], values=[pacer_interval], module=datapath_module)[0]
        test = test.add_reason("Didn't succeed to configure after two attempts - No pkt was found!")
        return test
    duplication = 1
    delay = 0 
    pixel_sim_thread = cert_data_sim.DataSimThread(test=test, num_of_pixels=num_of_sim_tags, duplicates=duplication, delay=delay, pkt_types=[0],pixels_type=GEN2)
    cycle_time = calculate_sending_time(duplication, delay, num_of_sim_tags)
    sending_time = cycle_time*4
    print(f"Simulator send pixels for {sending_time} sec")
    pixel_sim_thread.start()
    start_time = time.time()
    # sending time 
    ctr_tags_sending_time = []
    while (time.time() - start_time) < sending_time:
        HB_list = send_get_HB(test)
    
    pixel_sim_thread.stop()
    for p in HB_list:  
        ctr_tags_sending_time.append(p[MGMT_PKT].pkt.tags_ctr)
    print (f"\nSimulator stop generating packets\n")
    #TODO: logging print(debug)
    # print(f"ctr_tags_list: {ctr_tags_sending_time}\n")
    
    # waiting time - until the aging value 
    # during of the aging time we expect to get the ctr_tags equal to the number of pixels
    ctr_tags_aging_time = []
    print(f"waiting for aging time of {aging_time} sec")
    while (time.time() - start_time) < (cycle_time*3+aging_time):
        HB_list = send_get_HB(test)
        for p in HB_list:  
            ctr_tags_aging_time.append(p[MGMT_PKT].pkt.tags_ctr)
    print(f"\naging time: {aging_time} passed\n")
    #TODO: logging print(debug)
    # print(f"ctr_tags_list: {ctr_tags_aging_time}\n")
    start_aging_time = time.time()
    ctr_tags_deleting_time = []
    
    found_zero = 0 
    time_finding = 0
    # stop after two HB packets, we expect to get the ctr_tags 0 in the second HB packet after the aging time 
    print(f"Start of deleting time, wait for zero value ")
    while (time.time() - start_aging_time) <= 120:
        test, HB_list = cert_common.scan_for_mgmt_pkts(test, [eval_pkt(f'Brg2GwHbV{test.active_brg.api_version}')])
        for p in HB_list:  
            ctr_tags_deleting_time.append(p[MGMT_PKT].pkt.tags_ctr)
            if p[MGMT_PKT].pkt.tags_ctr == 0:
                found_zero = 1
                time_finding =  round(time.time()-start_aging_time, 2)
                print(f"Finding time: {time_finding}")
                print(f"Found zero value after {time_finding} sec")
                break   
        if found_zero:
            break
    # sending time and the deleting time should be the same
    print(f"Deleting time: {cycle_time} passed\n")
    #TODO: logging print(debug)
    # print(f"Ctr_tags_deleting_time: {ctr_tags_deleting_time}\n")
    
    # expected to get the ctr_tags 0 in the second HB packet after the aging time
    if found_zero == 0 or time_finding > 60:
        test.rc = TEST_FAILED
        test.add_reason("The last counter value is not zero")
        print("The last counter value is not zero\n")
    else:
        # NOTE: because sometimes when it didn't find HB pkt it failed the test. 
        test.rc = TEST_PASSED
    return test

def low_pacer(test, datapath_module, num_of_sim_tags):
    pacer_interval = 15
    aging_time = calculate_aging_time(pacer_interval) 
    test = combination_func(test, datapath_module, pacer_interval= pacer_interval, num_of_sim_tags=num_of_sim_tags , aging_time=aging_time) 
    return test

def high_pacer(test, datapath_module, num_of_sim_tags):
    pacer_interval = 300
    aging_time = calculate_aging_time(pacer_interval)
    test = combination_func(test, datapath_module, pacer_interval= pacer_interval, num_of_sim_tags=num_of_sim_tags , aging_time=aging_time) 
    return test

def run(test):
    # Test prolog
    datapath_module = eval_pkt(f'ModuleDatapathV{test.active_brg.api_version}')
    test = cert_common.test_prolog(test)
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test)

    STRESS_TEST_MAP = {"low_pacer": low_pacer, "high_pacer": high_pacer}
    num_of_pixels = 500
    
    for param in test.params:
        functionality_run_print(param.name)
        test = STRESS_TEST_MAP[param.value](test, datapath_module, num_of_pixels)
        generate_log_file(test, param.name)
        field_functionality_pass_fail_print(test, param.name)
        test.set_phase_rc(param.name, test.rc)
        test.add_phase_reason(param.name, test.reason)
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            break
        else:
            test.reset_result()
        time.sleep(5)

    return cert_common.test_epilog(test, revert_brgs=True, revert_gws=False, modules=[datapath_module])