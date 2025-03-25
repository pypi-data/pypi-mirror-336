from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config
import random

# Test Description:
# This test is to verify the functionality of both signal indicator tx (tx_brg) and rx (rx_brg) at BRG level.
# rssi_threshold = phase 0 , check the if rssi value is between 0 to -25.
# brg0_rx_brg1_tx  = phase 1+2  
# phase 1 - One BRG will be configured as signal indicator tx, and the other as signal indicator rx, and we expect to see signal indicator packets only from the rx BRG according to the tx params (repetition and cycle params).
# phase 2 - Same as phase 1, but with different tx params configured.
# brg0_none_brg1_rx = phase 3 - One rx BRG without any tx BRG. We don't expect to see any signal indicator packets. This phase is to verify the brg module logic is working properly, and no tag packet is accidentally being treated as signal indicator packet.
# brg0_rxtx_brg1_rxtx =  phase 4 - Both BRG's will be configured to be transmitters and receivers, with different tx params for each one. we expect
# to see signal indicator packets from both BRG's, according to the tx params.
# brg0_tx_brg1_none = phase 5 - One BRG will be configured as signal indicator tx, but no rx, so we don't expect to receive signal indicatopr packets.
# that way we can assure the logic within the receiver is not confused by the signal indicator uuid as external sensor.

# Test MACROS #
DEFAULT_HDR = ag.Hdr(group_id=ag.GROUP_ID_GW2BRG)
NUM_OF_SCANNING_tx_signal_ind_cycle = 2
DEFAULT_SCAN_TIME = 60
SCAN_DELAY_TIME = 5
BOARD_TYPES_2_POLARIZATION_ANT_LIST = [ag.BOARD_TYPE_MINEW_SINGLE_BAND_V0, ag.BOARD_TYPE_MINEW_DUAL_BAND_V0, ag.BOARD_TYPE_ENERGOUS_V2, ag.BOARD_TYPE_ERM_V0, ag.BOARD_TYPE_ERM_V1]
BLE4_LISTEN_PERIOD = 15
BLE4_BROADCAST_DURATION = BLE4_LISTEN_PERIOD + 1

# Test functions #
def mqtt_scan_n_create_log_file(test, duration, phase):
    test.mqttc.flush_pkts()
    mqtt_scan_wait(test, duration=duration)
    generate_log_file(test, f"{phase}")

def get_all_signal_ind_pkt(test=None, rx_brg=None, tx_brg=None):
    if rx_brg == test.brg1:
        all_sensor_packets = cert_mqtt.get_all_brg1_ext_sensor_pkts(mqttc=test.mqttc, test=test)
    elif rx_brg == test.brg0:
        all_sensor_packets = cert_mqtt.get_all_sensor_pkts(mqttc=test.mqttc, test=test)
    signal_ind_pkts = []
    for p in all_sensor_packets:
        if p[SENSOR_UUID] == "{:06X}".format(ag.SENSOR_SERVICE_ID_SIGNAL_INDICATOR) and p[BRIDGE_ID] == rx_brg.id_str and (p[SENSOR_ID] == tx_brg.id_alias or hex_str2int(p[SENSOR_ID]) == tx_brg.id_str):
            signal_ind_pkts.append(p)
    return signal_ind_pkts

def expected_signal_ind_pkts_calc(tx_brg, rx_brg):
    if (tx_brg.board_type in BOARD_TYPES_2_POLARIZATION_ANT_LIST):
        tx_brg_ant_polarization_num = 2
    else:
        tx_brg_ant_polarization_num = 1
    if (rx_brg.board_type in BOARD_TYPES_2_POLARIZATION_ANT_LIST):
        rx_brg_ant_polarization_num = 2
        result = [(NUM_OF_SCANNING_tx_signal_ind_cycle * tx_brg_ant_polarization_num * rx_brg_ant_polarization_num) - 1,
                  NUM_OF_SCANNING_tx_signal_ind_cycle * tx_brg_ant_polarization_num * rx_brg_ant_polarization_num]
    else:
        rx_brg_ant_polarization_num = 1
        result = [NUM_OF_SCANNING_tx_signal_ind_cycle * tx_brg_ant_polarization_num * rx_brg_ant_polarization_num]
    return result

def terminate_test(test, phase, revert_rx_brg=False, revert_tx_brg=False, modules=[]):
    # Temp solution for internal_brg test because test_epilog doesn't support both internal brg and test.brgs
    utPrint(f"Terminating test (phase={phase})!!!!!!!!\n", "BLUE")
    if revert_rx_brg:
        restore_modules = [modules[1]] if (test.internal_brg or phase != 4) else modules
        restore_modules.append(eval_pkt(f'ModuleDatapathV{test.active_brg.api_version}'))
        utPrint(f"reverting rx_brg {test.brg1.id_str} to defaults\n", "BOLD")
        test, response = cert_config.config_brg1_defaults(test, modules=restore_modules, ble5=True)
        if response == NO_RESPONSE and test.exit_on_param_failure:
            test.rc = TEST_FAILED
            test.add_reason(f"BRG {test.brg1.id_str} didn't revert modules "
                                   f"{restore_modules} to default configuration!")

    if revert_tx_brg:
        restore_modules = [modules[0]] if (test.internal_brg or phase != 4) else modules
        restore_modules.append(eval_pkt(f'ModuleDatapathV{test.active_brg.api_version}'))
        utPrint(f"reverting tx_brg {test.brg0.id_str} to defaults\n", "BOLD")
        test, response = cert_config.config_brg_defaults(test, modules=restore_modules, ble5=True)
        if response == NO_RESPONSE and test.exit_on_param_failure:
            test.rc = TEST_FAILED
            test.add_reason(f"BRG {test.brg0.id_str} didn't revert modules"
                                   f"{restore_modules} to default configuration!")
    return cert_common.test_epilog(test)

def brg0_tx_brg1_none(test, energy2400_module, ext_sensors_module, tx_brg_, rx_brg_, modules):
    datapath_module = eval_pkt(f'ModuleDatapathV{test.active_brg.api_version}')

    # Phase 5 - Tx BRG without rx. just waiting for packets to be sent from the transmitter and verify
    # The receiver isn't receiving any signal indicator packets.
    phase = "brg0_tx_brg1_none" 
    tx_signal_ind_cycle = 15
    tx_signal_ind_rep  = 1 
    utPrint(f"TX BRG without RX - cycle = {tx_signal_ind_cycle}, repetition = {tx_signal_ind_rep}\n", "BLUE")
    # restore default configuration for receiver #
    utPrint(f"Configuring BRG {rx_brg_.id_str} to default", "BOLD")
    restore_modules = [modules[1]] if (test.internal_brg) else modules
    test = cert_config.config_brg1_defaults(test, modules=restore_modules, ble5=True)[0]
    print_update_wait(BLE4_BROADCAST_DURATION) # BLE5 configuration can take up to BLE4_BROADCAST_DURATION sec
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        test.add_reason(f"BRG {rx_brg_.id_str}: didn't revert to default configuration!")

    # configuring transmitter #
    utPrint(f"Configuring BRG {tx_brg_.id_str} as Signal Indicator Transmitter", "BOLD")
    test =  cert_config.brg1_configure(test=test, module=energy2400_module, fields=[BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP], values=[tx_signal_ind_cycle, tx_signal_ind_rep], ble5=True)[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator transmitter configuration!")

    print_update_wait(BLE4_BROADCAST_DURATION) # BLE5 configuration can take up to BLE4_BROADCAST_DURATION sec
    utPrint(f"BRG {tx_brg_.id_str} configured to be transmitter - cycle = {tx_signal_ind_cycle},"
            f"repetition = {tx_signal_ind_rep}", "BOLD")

    # phase analysis #
    mqtt_scan_n_create_log_file(test, (NUM_OF_SCANNING_tx_signal_ind_cycle*tx_signal_ind_cycle) + SCAN_DELAY_TIME, phase)
    expected_signal_ind_pkts = [0]
    received_signal_ind_pkts = get_all_signal_ind_pkt(test=test, rx_brg=rx_brg_, tx_brg=tx_brg_)
    if len(received_signal_ind_pkts) not in expected_signal_ind_pkts:
        test.rc = TEST_FAILED
        test.add_reason(f"Phase {phase} failed - received signal indicator packet from BRG {rx_brg_.id_str}")

    # Revert bridges to BLE4 before next loop
    utPrint(f"reverting rx_brg {test.brg1.id_str} to defaults\n", "BOLD")
    test, response = cert_config.config_brg1_defaults(test, modules=[datapath_module], ble5=True)
    if response == NO_RESPONSE and test.exit_on_param_failure:
        test.rc = TEST_FAILED
        test.add_reason(f"BRG {test.brg1.id_str} didn't revert datapath_module to default configuration!")

    utPrint(f"reverting tx_brg {test.brg0.id_str} to defaults\n", "BOLD")
    test, response = cert_config.config_brg_defaults(test, modules=[datapath_module], ble5=True)
    if response == NO_RESPONSE and test.exit_on_param_failure:
        test.rc = TEST_FAILED
        test.add_reason(f"BRG {test.brg0.id_str} didn't revert datapath module to default configuration!")

    # Test epilog
    return terminate_test(test, phase=phase, revert_rx_brg=True, revert_tx_brg=True, modules=modules)

def brg0_rxtx_brg1_rxtx(test, energy2400_module, ext_sensors_module, tx_brg_, rx_brg_, modules):
    phase = "brg0_rxtx_brg1_rxtx"

    if not test.internal_brg:
        # Phase 4 - Both BRG's will be configured to be transmitters and receivers, with different tx params for each one.
        # expecting to see signal indicator packets from both BRG's, according to the tx params.
        utPrint(f"Both BRG's are transmitter and receivers, with different values\n", "BLUE")

        # configuring first BRG (tx_brg_) #
        tx_brg_signal_indicator_cycle = 15
        tx_brg_signal_indicator_rep = 3
        # configuring first brg (tx_brg_) as receiver
        utPrint(f"Configuring BRG {tx_brg_.id_str} as Signal Indicator Receiver", "BOLD")
        cert_config.brg_configure_ble5(test=test, module=ext_sensors_module, fields=[BRG_SENSOR0], values=[ag.EXTERNAL_SENSORS_SIGNAL_INDICATOR], wait=False)
        print_update_wait(BLE4_BROADCAST_DURATION) # BLE5 configuration can take up to BLE4_BROADCAST_DURATION sec
        utPrint(f"BRG {tx_brg_.id_str} successfully configured as Signal Indicator Receiver\n", "BOLD")
        
        # configuring transmitter #
        utPrint(f"Configuring BRG {tx_brg_.id_str} as Signal Indicator Transmitter", "BOLD")
        test =  cert_config.brg_configure(test=test, module=energy2400_module, fields=[BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP], values=[tx_brg_signal_indicator_cycle, tx_brg_signal_indicator_rep])[0]
        if test.rc == TEST_FAILED:
            test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator transmitter configuration!")

        print_update_wait(BLE4_BROADCAST_DURATION) # BLE5 configuration can take up to BLE4_BROADCAST_DURATION sec
        utPrint(f"BRG {tx_brg_.id_str} configured to be transmitter - cycle = {tx_brg_signal_indicator_cycle},"
                f"repetition = {tx_brg_signal_indicator_rep}", "BOLD")

        # configuring second brg (rx_brg_) as receiver
        utPrint(f"Configuring BRG {rx_brg_.id_str} as Signal Indicator Receiver", "BOLD")
        test = cert_config.brg1_configure(test=test, module=ext_sensors_module, fields=[BRG_SENSOR0], values=[ag.EXTERNAL_SENSORS_SIGNAL_INDICATOR], ble5=True)[0]
        print_update_wait(BLE4_BROADCAST_DURATION) # BLE5 configuration can take up to BLE4_BROADCAST_DURATION sec
        utPrint(f"BRG {rx_brg_.id_str} successfully configured as Signal Indicator Receiver\n", "BOLD")
        
        # configuring second brg (rx_brg_) as transmitter
        utPrint(f"Configuring BRG {rx_brg_.id_str} as Signal Indicator Transmitter", "BOLD")
        rx_brg_signal_indicator_cycle = 15 
        rx_brg_signal_indicator_rep = 4
        test =  cert_config.brg1_configure(test=test, module=energy2400_module, fields=[BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP], values=[rx_brg_signal_indicator_cycle, rx_brg_signal_indicator_rep], ble5=True)[0]
        print_update_wait(BLE4_BROADCAST_DURATION) # BLE5 configuration can take up to BLE4_BROADCAST_DURATION sec
        if test.rc == TEST_FAILED:
            test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator transmitter configuration!")
        utPrint(f"BRG {tx_brg_.id_str} configured to be transmitter - cycle = {rx_brg_signal_indicator_cycle},"
                f"repetition = {rx_brg_signal_indicator_rep}")
        
        # phase analysis #
        mqtt_scan_n_create_log_file(test, NUM_OF_SCANNING_tx_signal_ind_cycle * max(tx_brg_signal_indicator_cycle, rx_brg_signal_indicator_cycle) + SCAN_DELAY_TIME, phase)
        
        # Analyzing tx_brg_ performance as receiver
        utPrint(f"Analyzing tx_brg {tx_brg_.id_str} performance as a Receiver\n", "BOLD")
        rx_brg_tx_cycles = max(tx_brg_signal_indicator_cycle, rx_brg_signal_indicator_cycle) / rx_brg_signal_indicator_cycle
        expected_signal_ind_pkts = [int(x * rx_brg_tx_cycles) for x in expected_signal_ind_pkts_calc(rx_brg_, tx_brg_)]
        received_signal_ind_pkts = get_all_signal_ind_pkt(test=test, rx_brg=tx_brg_, tx_brg=rx_brg_)
        txt = f"""Phase {phase} - BRG {tx_brg_.id_str} signal indicator packets: received {len(received_signal_ind_pkts)} packets, expected {expected_signal_ind_pkts} packets"""
        print(txt)
        if len(received_signal_ind_pkts) not in expected_signal_ind_pkts:
            test.rc = TEST_FAILED
            test.add_reason(txt)

        # Analyzing rx_brg_ performance as receiver
        utPrint(f"Analyzing rx_brg {rx_brg_.id_str} performance as a Receiver\n", "BOLD")
        tx_brg_tx_cycles = max(tx_brg_signal_indicator_cycle, rx_brg_signal_indicator_cycle) / tx_brg_signal_indicator_cycle
        expected_signal_ind_pkts = [int(x * tx_brg_tx_cycles) for x in expected_signal_ind_pkts_calc(rx_brg_, tx_brg_)]
        received_signal_ind_pkts = get_all_signal_ind_pkt(test=test, rx_brg=rx_brg_, tx_brg=tx_brg_)
        txt = f"""Phase {phase} - BRG {rx_brg_.id_str} signal indicator packets: received {len(received_signal_ind_pkts)} packets, expected {expected_signal_ind_pkts} packets"""
        print(txt)
        if len(received_signal_ind_pkts) not in expected_signal_ind_pkts:
            test.rc = TEST_FAILED
            test.add_reason(txt)
    else:
        test.add_reason("skip for internal BRG")
    return terminate_test(test, phase=phase, revert_rx_brg=True,revert_tx_brg=True, modules=modules)

def brg0_none_brg1_rx(test, energy2400_module, ext_sensors_module, tx_brg_, rx_brg_, modules):
    phase = "brg0_none_brg1_rx"
    # Phase 3 - Rx BRG without tx.Expecting no signal indicator packets to be received.
    tx_signal_ind_cycle = ag.BRG_DEFAULT_SIGNAL_INDICATOR_CYCLE
    tx_signal_ind_rep = ag.BRG_DEFAULT_SIGNAL_INDICATOR_REP
    utPrint(f"RX BRG without TX- cycle = {tx_signal_ind_cycle}, repetition = {tx_signal_ind_rep}\n", "BLUE")
    
    # configuring transmitter #
    utPrint(f"Configuring BRG {tx_brg_.id_str} as Signal Indicator Transmitter", "BOLD")
    test =  cert_config.brg1_configure(test=test, module=energy2400_module, fields=[BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP], values=[tx_signal_ind_cycle, tx_signal_ind_rep],ble5=True)[0]
    print_update_wait(BLE4_BROADCAST_DURATION) # BLE5 configuration can take up to BLE4_BROADCAST_DURATION sec
    if test.rc == TEST_FAILED:
        test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator transmitter configuration!")   
    utPrint(f"BRG {tx_brg_.id_str} configured to default!!! cycle = {tx_signal_ind_cycle},"f"repetition = {tx_signal_ind_rep}", "BOLD")
    
    # phase analysis #
    mqtt_scan_n_create_log_file(test, DEFAULT_SCAN_TIME, phase)
    expected_signal_ind_pkts = [0]
    received_signal_ind_pkts = get_all_signal_ind_pkt(test=test, rx_brg=rx_brg_, tx_brg=tx_brg_)
    if len(received_signal_ind_pkts) not in expected_signal_ind_pkts:
        test.rc = TEST_FAILED
        test.add_reason(f"Phase {phase} failed - received signal indicator packet from BRG"
                            f"{rx_brg_.id_str}")
    return terminate_test(test, phase=phase, revert_rx_brg=True, revert_tx_brg=True, modules=modules)

def brg0_rx_brg1_tx(test, energy2400_module, ext_sensors_module, tx_brg_, rx_brg_, modules):
    phase = "brg0_rx_brg1_tx"
    cycle_rep = [(30,3), (60,4)]
    for tx_signal_ind_cycle, tx_signal_ind_rep in cycle_rep:

        utPrint(f"TX BRG with RX- cycle = {tx_signal_ind_cycle}, repetition = {tx_signal_ind_rep}\n", "BLUE")
        # configuring receiver #
        utPrint(f"Configuring BRG {rx_brg_.id_str} as Signal Indicator Receiver", "BOLD")
        test =  cert_config.brg_configure(test=test, module=energy2400_module, fields=[BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP], values=[tx_signal_ind_cycle, tx_signal_ind_rep])[0]
        if test.rc == TEST_FAILED:
            test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator transmitter configuration!")

        # configuring transmitter #
        utPrint(f"Configuring BRG {tx_brg_.id_str} as Signal Indicator Transmitter", "BOLD")
        test =  cert_config.brg1_configure(test=test, module=energy2400_module, fields=[BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP], values=[tx_signal_ind_cycle, tx_signal_ind_rep],ble5=True)[0]
        print_update_wait(BLE4_BROADCAST_DURATION) # BLE5 configuration can take up to BLE4_BROADCAST_DURATION sec
        if test.rc == TEST_FAILED:
            test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator transmitter configuration!")

        utPrint(f"BRG {tx_brg_.id_str} configured to be transmitter - cycle = {tx_signal_ind_cycle},"f"repetition = {tx_signal_ind_rep}", "BOLD")
        
        # phase analysis
        mqtt_scan_n_create_log_file(test, (NUM_OF_SCANNING_tx_signal_ind_cycle * tx_signal_ind_cycle) + SCAN_DELAY_TIME, phase)
        expected_signal_ind_pkts = expected_signal_ind_pkts_calc(tx_brg_, rx_brg_)
        received_signal_ind_pkts = get_all_signal_ind_pkt(test=test, rx_brg=rx_brg_, tx_brg=tx_brg_)
        txt = f"""Phase {phase} - BRG {rx_brg_.id_str} signal indicator packets: received {len(received_signal_ind_pkts)} packets, expected {expected_signal_ind_pkts} packets"""
        print(txt)
        #TODO: change condition
        if len(received_signal_ind_pkts) not in expected_signal_ind_pkts:
            test.rc = TEST_FAILED
            test.add_reason(txt)
        return terminate_test(test, phase=phase, revert_rx_brg=True,revert_tx_brg=True, modules=modules)

def rssi_threshold(test, energy2400_module, ext_sensors_module, tx_brg_, rx_brg_, modules):
    phase = "rssi_threshold"
    # RSSI Threshold
    rssi_threshold = -25
    tx_signal_ind_cycle = 15
    tx_signal_ind_rep  = 3 
    utPrint(f"TX BRG with RX- cycle = {tx_signal_ind_cycle}, repetition = {tx_signal_ind_rep}\n", "BLUE")
    
    # configuring receiver #
    utPrint(f"Configuring BRG {rx_brg_.id_str} as Signal Indicator Receiver with RSSI Threshold of {rssi_threshold}", "BOLD")
    test =  cert_config.brg1_configure(test=test, module=ext_sensors_module, fields=[BRG_SENSOR0, BRG_RSSI_THRESHOLD], values=[ag.EXTERNAL_SENSORS_SIGNAL_INDICATOR, rssi_threshold], ble5=True)[0]
    print_update_wait(BLE4_BROADCAST_DURATION) # BLE5 configuration can take up to BLE4_BROADCAST_DURATION sec

    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        test.add_reason(f"BRG {rx_brg_.id_str}: didn't receive signal indicator receiver configuration!")
    
    # configuring transmitter #
    utPrint(f"Configuring BRG {tx_brg_.id_str} as Signal Indicator Transmitter", "BOLD")
    test =  cert_config.brg1_configure(test=test, module=energy2400_module, fields=[BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP], values=[tx_signal_ind_cycle, tx_signal_ind_rep],ble5=True)[0]
    print_update_wait(BLE4_BROADCAST_DURATION) # BLE5 configuration can take up to BLE4_BROADCAST_DURATION sec
    if test.rc == TEST_FAILED:
        test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator transmitter configuration!")

    utPrint(f"BRG {tx_brg_.id_str} configured to be transmitter - cycle = {tx_signal_ind_cycle},"
            f"repetition = {tx_signal_ind_rep}", "BOLD")
    # phase analysis #
    mqtt_scan_n_create_log_file(test, (NUM_OF_SCANNING_tx_signal_ind_cycle * tx_signal_ind_cycle) + SCAN_DELAY_TIME, phase)
    received_signal_ind_pkts = get_all_signal_ind_pkt(test=test, rx_brg=rx_brg_, tx_brg=tx_brg_)
    rssi_threshold_viloation_pkts = [p for p in received_signal_ind_pkts if p[RSSI] >= -1*rssi_threshold]
    if rssi_threshold_viloation_pkts:
        test.rc = TEST_FAILED
        test.add_reason(f"rssi_threshold phase failed - BRG {rx_brg_.id_str} echoed" +
                            f" {len(rssi_threshold_viloation_pkts)} signal indicator packets\n with RSSI weaker than {rssi_threshold}")
    field_functionality_pass_fail_print(test, 'phase', phase)
    
    return terminate_test(test, phase=phase, revert_rx_brg=True,revert_tx_brg=True, modules=modules)


SIGNAL_INDICATOR_TEST_MAP = {
    "rssi_threshold" : rssi_threshold, # phase 0 
    "brg0_rx_brg1_tx": brg0_rx_brg1_tx, # phase 1 + 2 
    "brg0_none_brg1_rx": brg0_none_brg1_rx, # phase 3 
    "brg0_rxtx_brg1_rxtx": brg0_rxtx_brg1_rxtx, # phase 4, skip for internal brg  
    "brg0_tx_brg1_none": brg0_tx_brg1_none} # phase 5 

def run(test):

    # Test modules evaluation #
    energy2400_module = eval_pkt(f'ModuleEnergy2400V{test.active_brg.api_version}')
    ext_sensors_module = eval_pkt(f'ModuleExtSensorsV{test.active_brg.api_version}')
    datapath_module = eval_pkt(f'ModuleDatapathV{test.active_brg.api_version}')

    # Transmitter related defines #
    tx_brg_ = test.brg0
    tx_module = energy2400_module

    # Receiver related defines #
    rx_brg_ = test.brg1

    # Modules list #
    modules = [tx_module, ext_sensors_module]

    # Test prolog
    test = cert_common.test_prolog(test)
    test = cert_config.brg_configure(test, fields=[BRG_RX_CHANNEL], values=[ag.RX_CHANNEL_10_250K], module=datapath_module)[0]
    test = cert_config.brg1_configure(test, fields=[BRG_RX_CHANNEL], values=[ag.RX_CHANNEL_10_250K], module=datapath_module)[0]
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        return terminate_test(test, phase=1, revert_rx_brg=True, revert_tx_brg=True, modules=modules)
    for param in test.params: 
        functionality_run_print(param.name)
        test = SIGNAL_INDICATOR_TEST_MAP[param.value](test, energy2400_module, ext_sensors_module, tx_brg_, rx_brg_, modules)
        generate_log_file(test, param.name)
        field_functionality_pass_fail_print(test, param.name)
        test.set_phase_rc(param.name, test.rc)
        test.add_phase_reason(param.name, test.reason)
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            break
        else:
            test.reset_result()
    
    return cert_common.test_epilog(test, revert_brgs=True, modules=[energy2400_module, ext_sensors_module],
                                 brg1_modules=[energy2400_module, ext_sensors_module])
