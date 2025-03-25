from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config

# Test Description:
#   This test is to verify the functionality of both signal indicator tx (tx_brg) and rx (rx_brg) at BRG level.
#   We will configure several signal indicator params during the test, and check the functionality of the signal indicator logic
#   for each of them.
#   It is important to execute the test with several setups: 2 Fanstel BRG's, 2 Minew BRG's and 1 Fanstel and 1 Minew BRG.
#   At first, we will configure several tx signal indicator params and check for ack's, to verify all indicated params were
#   received at the cloud.
#   Then, we will examine the signal indicator end-2-end logic with both transmitter and receiver:
#   phase 1 - One BRG will be configured as signal indicator tx, and the other as signal indicator rx, and we expect to see
#   signal indicator packets only from the tx BRG, and according to the tx params (to check the repetition and cycle params).
#   phase 2 - Same as phase 1, but with different tx params configured.
#   phase 3 - One rx BRG without any tx BRG. We don't expect to see any signal indicator packets. This phase is to verify the
#   brg module logic is working properly, and no tag packet is accidentally being treated as signal indicator packet.
#   phase 4 - Both BRG's will be configured to be transmitters and receivers, with different tx params for each one. we expect
#   to see signal indicator packets from both BRG's, according to the tx params.
#   phase 5 - One BRG will be configured as signal indicator tx, but no rx, so we don't expect to receive signal indicatopr packets.
#   that way we can assure the logic within the receiver is not confused by the signal indicator uuid as external sensor.


# Test MACROS #
DEFAULT_HDR = ag.Hdr(group_id=ag.GROUP_ID_GW2BRG)
NUM_OF_SCANNING_CYCLE = 2
DEFAULT_SCAN_TIME = 60
SCAN_DELAY_TIME = 5
BOARD_TYPES_2_POLARIZATION_ANT_LIST = [ag.BOARD_TYPE_MINEW_SINGLE_BAND_V0, ag.BOARD_TYPE_MINEW_DUAL_BAND_V0, ag.BOARD_TYPE_ENERGOUS_V2, ag.BOARD_TYPE_ERM_V0, ag.BOARD_TYPE_ERM_V1]

# Test functions #
def mqtt_scan_n_create_log_file(test, duration, phase):
    test.mqttc.flush_pkts()
    mqtt_scan_wait(test, duration=duration)
    generate_log_file(test, phase)

def get_all_signal_ind_pkt(test=None, rx_brg=None, tx_brg=None):
    if rx_brg == test.brg1:
        all_sensor_packets = cert_mqtt.get_all_brg1_ext_sensor_pkts(mqttc=test.mqttc, test=test)
    elif rx_brg == test.brg0:
        all_sensor_packets = cert_mqtt.get_all_sensor_pkts(mqttc=test.mqttc, test=test)
    signal_ind_pkts = []
    for p in all_sensor_packets:
        if p[SENSOR_UUID] == "{:06X}".format(ag.SENSOR_SERVICE_ID_SIGNAL_INDICATOR) and p[BRIDGE_ID] == rx_brg.id_str and (p[SENSOR_ID] == tx_brg.id_alias):
            signal_ind_pkts.append(p)
    #TODO: logging print 
    print(f" Found {len(signal_ind_pkts)} signal indicator pkts \n")
    return signal_ind_pkts

def expected_signal_ind_pkts_calc(tx_brg, rx_brg):
    if (tx_brg.board_type in BOARD_TYPES_2_POLARIZATION_ANT_LIST):
        tx_brg_ant_polarization_num = 2
    else:
        tx_brg_ant_polarization_num = 1
    if (rx_brg.board_type in BOARD_TYPES_2_POLARIZATION_ANT_LIST):
        rx_brg_ant_polarization_num = 2
        result = [(NUM_OF_SCANNING_CYCLE * tx_brg_ant_polarization_num * rx_brg_ant_polarization_num) - 1,
                  NUM_OF_SCANNING_CYCLE * tx_brg_ant_polarization_num * rx_brg_ant_polarization_num]
    else:
        rx_brg_ant_polarization_num = 1
        result = [NUM_OF_SCANNING_CYCLE * tx_brg_ant_polarization_num * rx_brg_ant_polarization_num]
    return result

def rssi_check(test, received_signal_ind_pkts ):
    threshold_rssi  = [0,80]
    for p in received_signal_ind_pkts:
        #TODO: logging print
        # print(f"rssi value: {p[RSSI]}")
        if not threshold_rssi[0] < p[RSSI] < threshold_rssi[1]:
            test.rc = TEST_FAILED
            test.add_reason("rssi value is wrong, out of 0 to 80 ")

    return test

def rx_tx_antenna_check(test, received_signal_ind_pkts , tx_brg_, rx_brg_ ):
    #TODO: logging print
    # print(f"length of received signal indicator pkts: {len(received_signal_ind_pkts)}\n ")
    # print(f"tx_brg board_type:{tx_brg_.board_type}\n")
    # print(f"rx_brg board_type:{rx_brg_.board_type}\n")
    
    list = get_polar_signal_ind_pkt(received_signal_ind_pkts,0,0)
    print(f"polar signal ind pkt 0,0: {list}")
    if len(get_polar_signal_ind_pkt(received_signal_ind_pkts, 0, 0)) != NUM_OF_SCANNING_CYCLE:
        test.rc = TEST_FAILED
        test.add_reason("incorrect num of packets with (0,0)!")

    if tx_brg_.board_type in BOARD_TYPES_2_POLARIZATION_ANT_LIST:
        list = get_polar_signal_ind_pkt(received_signal_ind_pkts,0,1)
        print(f"polar signal ind pkt 0,1: {list}")
        if len(get_polar_signal_ind_pkt(pkts=received_signal_ind_pkts, rx_ant=0, tx_ant=1)) != NUM_OF_SCANNING_CYCLE:
            test.rc = TEST_FAILED
            test.add_reason("incorrect num of packets with (0,1)")
    
    if rx_brg_.board_type in BOARD_TYPES_2_POLARIZATION_ANT_LIST:
        list = get_polar_signal_ind_pkt(received_signal_ind_pkts,1,0)
        print(f"polar signal ind pkt 1,0: {list}")
        if len(get_polar_signal_ind_pkt(received_signal_ind_pkts, 1, 0)) != NUM_OF_SCANNING_CYCLE:
            test.rc = TEST_FAILED
            test.add_reason("incorrect num of packets with (1,0)")

    if rx_brg_.board_type in BOARD_TYPES_2_POLARIZATION_ANT_LIST and tx_brg_.board_type in BOARD_TYPES_2_POLARIZATION_ANT_LIST:
        list = get_polar_signal_ind_pkt(received_signal_ind_pkts,1,1)
        print(f"polar signal ind pkt 1,1: {list}")
        if len(get_polar_signal_ind_pkt(received_signal_ind_pkts, 1, 1)) != NUM_OF_SCANNING_CYCLE:
            test.rc = TEST_FAILED
            test.add_reason("incorrect num of packets with (1,1)")
    return test

def get_polar_signal_ind_pkt(pkts, rx_ant, tx_ant):
    for p in pkts:
        #TODO: logging print
        print(f" rx antenna: {p[SENSOR_PKT].pkt.rx_antenna}, tx antenna: {p[SENSOR_PKT].pkt.tx_antenna}  ######    rx_ant: {rx_ant}, tx_ant: {tx_ant}")
    return [p for p in pkts if p[SENSOR_PKT].pkt.rx_antenna == rx_ant and p[SENSOR_PKT].pkt.tx_antenna == tx_ant]

def output_power_check(test, received_signal_ind_pkts, tx_brg_):
    #TODO: verify that in this implement it corresponding to the current board. and verify situation that we have 2 different board type. 
    output_power_def_internal = ag.BRG_DEFAULT_OUTPUT_POWER_2_4
    output_power_def_not_internal = ag.BRG_DEFAULT_DATAPATH_OUTPUT_POWER

    for p in received_signal_ind_pkts:
        print(p[SENSOR_PKT].pkt)
        # NOTE: generic way to identify if the brg is internal or not 
        if len(tx_brg_.__dict__["sup_caps"]) == 3 : # which mean it's internal bridge 
            if p[SENSOR_PKT].pkt.output_power != output_power_def_internal:
                test.rc = TEST_FAILED
                test.add_reason(f"output power of internal brg  is incorrect! \n got:{p[SENSOR_PKT].pkt.out_power}, expected: {output_power_def_internal}\n")
        else:
            if p[SENSOR_PKT].pkt.output_power != output_power_def_not_internal:
                test.rc = TEST_FAILED
                test.add_reason(f"output power of active brg  is incorrect! \n got:{p[SENSOR_PKT].pkt.output_power}, expected: {output_power_def_internal}\n")
    return test


def test_rssi_threshold(test, energy2400_module, ext_sensors_module):
    cycle, rep = 30, 3
    tx_brg_ = test.brg0
    rx_brg_ = test.brg1
    rssi_threshold = -25

    utPrint(f"TX BRG with RX- cycle = {cycle}, repetition = {rep}\n", "BLUE")
    # configuring receiver #
    utPrint(f"Configuring BRG {rx_brg_.id_str} as Signal Indicator Receiver with RSSI Threshold of {rssi_threshold}", "BOLD")
    test =  cert_config.brg1_configure(test=test, module=ext_sensors_module, fields=[BRG_SENSOR0, BRG_RSSI_THRESHOLD], values=[ag.EXTERNAL_SENSORS_SIGNAL_INDICATOR, rssi_threshold])[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"BRG {rx_brg_.id_str}: didn't receive signal indicator receiver configuration!")
        return test
    # configuring transmitter #
    utPrint(f"Configuring BRG {tx_brg_.id_str} as Signal Indicator Transmitter", "BOLD")
    test =  cert_config.brg_configure(test=test, module=energy2400_module, fields=[BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP], values=[cycle, rep])[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator transmitter configuration!")
        return test
    utPrint(f"BRG {tx_brg_.id_str} configured to be transmitter - cycle = {cycle},"
            f"repetition = {rep}", "BOLD")
    # phase analysis #
    mqtt_scan_n_create_log_file(test, (NUM_OF_SCANNING_CYCLE * cycle) + SCAN_DELAY_TIME, f"rssi_threshold")
    received_signal_ind_pkts = get_all_signal_ind_pkt(test=test, rx_brg=rx_brg_, tx_brg=tx_brg_)
    for p in received_signal_ind_pkts:
        print(f"rssi value: {p[RSSI]}")
    rssi_threshold_viloation_pkts = [p for p in received_signal_ind_pkts if p[RSSI] >= -1*rssi_threshold]
    if rssi_threshold_viloation_pkts:
        test.rc = TEST_FAILED
        test.add_reason(f"rssi_threshold phase failed - BRG {rx_brg_.id_str} echoed" +
                               f" {len(rssi_threshold_viloation_pkts)} signal indicator packets\n with RSSI weaker than {rssi_threshold}")
    return test

def test_brg0_rx_brg1_tx(test, energy2400_module, ext_sensors_module):
    cycle_rep = [(30,3), (60,4)]
    tx_brg_ = test.brg0
    rx_brg_ = test.brg1

    for cycle,rep in cycle_rep:
        utPrint(f"TX BRG with RX- cycle = {cycle}, repetition = {rep}\n", "BLUE")
        # configuring receiver #
        utPrint(f"Configuring BRG {rx_brg_.id_str} as Signal Indicator Receiver", "BOLD")
        test =  cert_config.brg1_configure(test=test, module=ext_sensors_module, fields=[BRG_SENSOR0], values=[ag.EXTERNAL_SENSORS_SIGNAL_INDICATOR])[0]
        if test.rc == TEST_FAILED:
            test.add_reason(f"BRG {rx_brg_.id_str}: didn't receive signal indicator receiver configuration!")
            return test
        # configuring transmitter #
        utPrint(f"Configuring BRG {tx_brg_.id_str} as Signal Indicator Transmitter", "BOLD")
        test =  cert_config.brg_configure(test=test, module=energy2400_module, fields=[BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP], values=[cycle, rep])[0]
        if test.rc == TEST_FAILED:
            test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator transmitter configuration!")
            return test
        utPrint(f"BRG {tx_brg_.id_str} configured to be transmitter - cycle = {cycle},"
                f"repetition = {rep}", "BOLD")
        # phase analysis #
        mqtt_scan_n_create_log_file(test, (NUM_OF_SCANNING_CYCLE * cycle) + SCAN_DELAY_TIME, f"brg0_rx_brg1_tx_{cycle}_{rep}")
        received_signal_ind_pkts = get_all_signal_ind_pkt(test=test, rx_brg=rx_brg_, tx_brg=tx_brg_)
        expected_signal_ind_pkts = expected_signal_ind_pkts_calc(tx_brg_, rx_brg_)

        if len(received_signal_ind_pkts) not in expected_signal_ind_pkts:
            test.rc = TEST_FAILED
            test.add_reason(f"brg0_rx_brg1_tx phase failed - BRG {rx_brg_.id_str} received wrong number of "
                                    f"signal indicator packets\n received {len(received_signal_ind_pkts)} packets, "
                                    f"expected {expected_signal_ind_pkts} packets")

        test = rx_tx_antenna_check(test, received_signal_ind_pkts, tx_brg_, rx_brg_)
        test = output_power_check(test, received_signal_ind_pkts, tx_brg_)
        test = rssi_check(test, received_signal_ind_pkts)
    return test

def test_brg0_none_brg1_rx(test, energy2400_module, ext_sensors_module):
    cycle, rep = ag.BRG_DEFAULT_SIGNAL_INDICATOR_CYCLE, ag.BRG_DEFAULT_SIGNAL_INDICATOR_REP
    tx_brg_ = test.brg0
    rx_brg_ = test.brg1
    utPrint(f"RX BRG without TX- cycle = {cycle}, repetition = {rep}\n", "BLUE")
    # configuring transmitter to no TX #
    utPrint(f"Configuring BRG {tx_brg_.id_str} to default", "BOLD")
    test =  cert_config.brg_configure(test=test, module=energy2400_module, fields=[BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP], values=[cycle, rep])[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"BRG {tx_brg_.id_str}: didn't revert to default (no signal indicator tx)!")
        return test
    utPrint(f"BRG {tx_brg_.id_str} configured to default!!! cycle = {cycle},"
              f"repetition = {rep}", "BOLD")
    # phase analysis #
    mqtt_scan_n_create_log_file(test, DEFAULT_SCAN_TIME, "brg0_none_brg1_rx")
    expected_signal_ind_pkts = [0]
    received_signal_ind_pkts = get_all_signal_ind_pkt(test=test, rx_brg=rx_brg_, tx_brg=tx_brg_)
    if len(received_signal_ind_pkts) not in expected_signal_ind_pkts:
        test.rc = TEST_FAILED
        test.add_reason(f"brg0_rx_brg1_tx phase failed - BRG {rx_brg_.id_str} received wrong number of "
                                f"signal indicator packets\n received {len(received_signal_ind_pkts)} packets, "
                                f"expected {expected_signal_ind_pkts} packets")

    return test

def test_brg0_rxtx_brg1_rxtx(test, energy2400_module, ext_sensors_module):
    tx_cycle, tx_rep = 15,4
    rx_cycle, rx_rep = 16,4
    tx_brg_ = test.brg0
    rx_brg_ = test.brg1
    utPrint(f"Both BRG's are transmitter and receivers, with different values\n", "BLUE")
    # configuring first brg (tx_brg_) as receiver
    utPrint(f"Configuring BRG {tx_brg_.id_str} as Signal Indicator Receiver", "BOLD")
    test =  cert_config.brg_configure(test=test, module=ext_sensors_module, fields=[BRG_SENSOR0], values=[ag.EXTERNAL_SENSORS_SIGNAL_INDICATOR])[0]
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator receiver configuration!")
        return test
    utPrint(f"BRG {tx_brg_.id_str} successfully configured as Signal Indicator Receiver\n", "BOLD")
    # configuring first brg (tx_brg_) as transmitter
    utPrint(f"Configuring BRG {tx_brg_.id_str} as Signal Indicator Transmitter", "BOLD")
    test =  cert_config.brg_configure(test=test, module=energy2400_module, fields=[BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP], values=[tx_cycle, tx_rep])[0]
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator transmitter configuration!")
        return test
    utPrint(f"BRG {tx_brg_.id_str} configured to be transmitter - cycle = {tx_cycle},"
                f"repetition = {tx_rep}", "BOLD")

    # configuring second brg (rx_brg_) as receiver
    utPrint(f"Configuring BRG {rx_brg_.id_str} as Signal Indicator Receiver", "BOLD")
    test =  cert_config.brg1_configure(test=test, module=ext_sensors_module, fields=[BRG_SENSOR0], values=[ag.EXTERNAL_SENSORS_SIGNAL_INDICATOR])[0]
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        test.add_reason(f"BRG {rx_brg_.id_str}: didn't receive signal indicator receiver configuration!")
        return test
    utPrint(f"BRG {rx_brg_.id_str} successfully configured as Signal Indicator Receiver\n", "BOLD")

    # configuring second brg (rx_brg_) as transmitter (already configured as rx)
    utPrint(f"Configuring BRG {rx_brg_.id_str} as Signal Indicator Transmitter", "BOLD")
    test =  cert_config.brg1_configure(test=test, module=energy2400_module, fields=[BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP], values=[rx_cycle, rx_rep])[0]
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        test.add_reason(f"BRG {rx_brg_.id_str}: didn't receive signal indicator transmitter configuration!")
        return test
    utPrint(f"BRG {rx_brg_.id_str} configured to be transmitter - cycle = {rx_cycle},"
                f"repetition = {rx_rep}")

    # phase analysis #
    mqtt_scan_n_create_log_file(test, NUM_OF_SCANNING_CYCLE * max(tx_cycle, rx_cycle) + SCAN_DELAY_TIME, "brg0_rxtx_brg1_rxtx")

    # Analyzing tx_brg_ performance as receiver
    utPrint(f"Analyzing tx_brg {tx_brg_.id_str} performance as a Receiver\n", "BOLD")
    expected_signal_ind_pkts = expected_signal_ind_pkts_calc(rx_brg_, tx_brg_)
    received_signal_ind_pkts = get_all_signal_ind_pkt(test=test, rx_brg=tx_brg_, tx_brg=rx_brg_)
    if len(received_signal_ind_pkts) not in expected_signal_ind_pkts:
        test.rc = TEST_FAILED
        test.add_reason(f"brg0_rxtx_brg1_rxtx phase failed - BRG {tx_brg_.id_str} received wrong number of "
                                f"signal indicator packets\n received {len(received_signal_ind_pkts)} packets, "
                                f"expected {expected_signal_ind_pkts} packets")

    # Analyzing rx_brg_ performance as receiver
    utPrint(f"Analyzing rx_brg {rx_brg_.id_str} performance as a Receiver\n", "BOLD")
    expected_signal_ind_pkts = expected_signal_ind_pkts_calc(tx_brg_, rx_brg_)
    received_signal_ind_pkts = get_all_signal_ind_pkt(test=test, rx_brg=rx_brg_, tx_brg=tx_brg_)
    if len(received_signal_ind_pkts) not in expected_signal_ind_pkts:
        test.rc = TEST_FAILED
        test.add_reason(f"brg0_rxtx_brg1_rxtx phase failed - BRG {rx_brg_.id_str} received wrong number of "
                                f"signal indicator packets\n received {len(received_signal_ind_pkts)} packets, "
                                f"expected {expected_signal_ind_pkts} packets")
    #NOTE: I skipped the antenna and output power checks for this phase 
    return test

def test_brg0_tx_brg1_none(test, energy2400_module, ext_sensors_module):
    # Tx BRG without rx. just waiting for packets to be sent from the transmitter and verify
    # The receiver isn't receiving any signal indicator packets.
    cycle, rep = 15,3
    tx_brg_ = test.brg0
    rx_brg_ = test.brg1
    utPrint(f"TX BRG without RX - cycle = {cycle}, repetition = {rep}\n", "BLUE")
    # restore default configuration for receiver #
    utPrint(f"Configuring BRG {rx_brg_.id_str} to default", "BOLD")
    test = cert_config.config_brg1_defaults(test, modules=[energy2400_module, ext_sensors_module])[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"BRG {rx_brg_.id_str}: didn't revert to default configuration!")
        return test
    # configuring transmitter #
    utPrint(f"Configuring BRG {tx_brg_.id_str} as Signal Indicator Transmitter", "BOLD")
    test =  cert_config.brg_configure(test=test, module=energy2400_module, fields=[BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP], values=[cycle, rep])[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator transmitter configuration!")
        return test

    # phase analysis #
    mqtt_scan_n_create_log_file(test, (NUM_OF_SCANNING_CYCLE*cycle) + SCAN_DELAY_TIME, "brg0_tx_brg1_none")
    expected_signal_ind_pkts = [0]
    received_signal_ind_pkts = get_all_signal_ind_pkt(test=test, rx_brg=rx_brg_, tx_brg=tx_brg_)
    if len(received_signal_ind_pkts) not in expected_signal_ind_pkts:
        test.rc = TEST_FAILED
        test.add_reason(f"brg0_tx_brg1_none phase failed - received signal indicator packet from BRG"
                                f"{rx_brg_.id_str}")
    test = output_power_check(test, received_signal_ind_pkts, tx_brg_)

    return test

SIGNAL_INDICATOR_TEST_MAP = {"rssi_threshold" : test_rssi_threshold, "brg0_rx_brg1_tx": test_brg0_rx_brg1_tx,
                             "brg0_none_brg1_rx": test_brg0_none_brg1_rx, "brg0_rxtx_brg1_rxtx": test_brg0_rxtx_brg1_rxtx,
                             "brg0_tx_brg1_none": test_brg0_tx_brg1_none}

def run(test):
    # Test modules evaluation #
    energy2400_module = eval_pkt(f'ModuleEnergy2400V{test.active_brg.api_version}')
    ext_sensors_module = eval_pkt(f'ModuleExtSensorsV{test.active_brg.api_version}')

    # Test prolog
    test = cert_common.test_prolog(test)
    for param in test.params:
        functionality_run_print(param.name)
        test = SIGNAL_INDICATOR_TEST_MAP[param.value](test, energy2400_module, ext_sensors_module)
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