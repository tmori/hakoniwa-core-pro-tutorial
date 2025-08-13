#!/usr/bin/python
# -*- coding: utf-8 -*-
import hakopy
#import sources.assets.bindings.python.src.hako_pdu as hako_pdu
import sys
import time
from hakoniwa_pdu.pdu_manager import PduManager
from hakoniwa_pdu.impl.shm_communication_service import ShmCommunicationService
from hakoniwa_pdu.service.hako_asset_service_config import HakoAssetServiceConfig
from hakoniwa_pdu.service.hako_asset_service_server import HakoAssetServiceServer

from hakoniwa_pdu.pdu_msgs.hako_srv_msgs.pdu_pytype_AddTwoIntsRequest import AddTwoIntsRequest
from hakoniwa_pdu.pdu_msgs.hako_srv_msgs.pdu_pytype_AddTwoIntsResponse import AddTwoIntsResponse
from hakoniwa_pdu.pdu_msgs.hako_srv_msgs.pdu_conv_AddTwoIntsRequestPacket import py_to_pdu_AddTwoIntsRequestPacket, pdu_to_py_AddTwoIntsRequestPacket
from hakoniwa_pdu.pdu_msgs.hako_srv_msgs.pdu_conv_AddTwoIntsResponsePacket import py_to_pdu_AddTwoIntsResponsePacket, pdu_to_py_AddTwoIntsResponsePacket
import asyncio

asset_name = 'Server'
service_name = 'Service/Add'
service_config_path = './examples/service/service.json'
service_server = None
delta_time_usec = 1000 * 1000
TEST_CASE_NORMAL = 0
TEST_CASE_CANCEL1 = 1
TEST_CASE_CANCEL2 = 2
test_case = TEST_CASE_NORMAL
def hako_sleep(sec: int):
    #print(f"INFO: hako_sleep({sec})")
    ret = hakopy.usleep(int(sec * 1000 * 1000))
    if ret == False:
        sys.exit(1)
    time.sleep(sec)
    #print(f"INFO: hako_sleep({sec}) done")
    return 0

async def hako_sleep_async(sec: int):
    await asyncio.to_thread(hako_sleep, sec)

def my_on_initialize(context):
    global asset_name
    global service_name
    global service_server
    service_server = HakoAssetServiceServer(pdu_manager, asset_name, service_name, 
                                            py_to_pdu_AddTwoIntsRequestPacket,
                                            pdu_to_py_AddTwoIntsRequestPacket, 
                                            py_to_pdu_AddTwoIntsResponsePacket,
                                            pdu_to_py_AddTwoIntsResponsePacket)
    service_config = HakoAssetServiceConfig(service_config_path, pdu_manager.pdu_convertor.offmap)
    service_config.append_pdu_def(pdu_manager.pdu_config.get_pdudef())
    service_server.service_config = service_config
    if service_server.initialize() == False:
        raise RuntimeError("Failed to create asset service")

    return 0

def my_on_reset(context):
    return 0

async def normal_test_case():
    global pdu_manager
    global service_server
    global delta_time_usec
    while True:
        event = service_server.poll()
        if service_server.is_request_in(event):
            # Process the request
            print("Request received")
            request_data: AddTwoIntsRequest = service_server.get_request()
            print(f"Request data: {request_data}")
            res = AddTwoIntsResponse()
            res.sum = request_data.a + request_data.b
            print(f"INFO: OUT: {res}")
            while service_server.normal_reply(res) == False:
                print("INFO: APL normal_reply() is not done")
                await hako_sleep_async(1)
        else:
            await hako_sleep_async(1)

async def cancel_1_test_case():
    global pdu_manager
    global service_server
    global delta_time_usec
    print("INFO: normal_test_case waiting...")
    await hako_sleep_async(5)
    print("INFO: normal_test_case start")
    event = service_server.poll()
    if event < 0:
        print(f"ERROR: hako_asset_service_server_poll() returns {event}")
        return 1
    if service_server.is_request_in(event):
        req = service_server.get_request()
        print(f"Request data: {req}")
        res = AddTwoIntsResponse()
        res.sum = req.a + req.b
        await hako_sleep_async(5)
        event = service_server.poll()
        print(f"event: {event}")
        if service_server.is_request_cancel(event):
            print("Request cancelled")
            service_server.cancel_reply(res)
        else:
            print("Request not cancelled")
            service_server.normal_reply(res)

    return 0

async def cancel_2_test_case():
    global pdu_manager
    global service_server
    global delta_time_usec
    print("INFO: normal_test_case waiting...")
    await hako_sleep_async(5)
    print("INFO: normal_test_case start")
    event = service_server.poll()
    if event < 0:
        print(f"ERROR: hako_asset_service_server_poll() returns {event}")
        return 1
    if service_server.is_request_in(event):
        req = service_server.get_request()
        print(f"Request data: {req}")
        res = AddTwoIntsResponse()
        res.sum = req.a + req.b
        await hako_sleep_async(5)
        print(f"INFO: OUT: {res}")
        service_server.normal_reply(res)
        event = service_server.poll()
        print(f"event: {event}")

    return 0

pdu_manager = None
def my_on_manual_timing_control(context):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_client_task())
    except KeyboardInterrupt:
        print("Interrupted by user.")
    return 0


async def run_client_task():
    global test_case
    if test_case == TEST_CASE_NORMAL:
        await normal_test_case()
    elif test_case == TEST_CASE_CANCEL1:
        await cancel_1_test_case()
    elif test_case == TEST_CASE_CANCEL2:
        await cancel_2_test_case()

    while True:
        await hako_sleep_async(1)

    return 0

my_callback = {
    'on_initialize': my_on_initialize,
    'on_simulation_step': None,
    'on_manual_timing_control': my_on_manual_timing_control,
    'on_reset': my_on_reset
}
def main():
    global test_case
    global pdu_manager
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <config_path>  <test_case: normal | cancel1 | cancel2> [external]")
        return 1

    asset_name = 'Server'
    config_path = sys.argv[1]
    if sys.argv[2] == 'normal':
        test_case = TEST_CASE_NORMAL
    elif sys.argv[2] == 'cancel1':
        test_case = TEST_CASE_CANCEL1
    elif sys.argv[2] == 'cancel2':
        test_case = TEST_CASE_CANCEL2
    else:
        print(f"ERROR: invalid test case {sys.argv[2]}")
        return 1
    delta_time_usec = 1000 * 1000
    is_external = False
    if len(sys.argv) == 4:
        if sys.argv[3] == 'external':
            is_external = True
            print("INFO: external mode")
        else:
            print(f"ERROR: invalid argument {sys.argv[3]}")
            return 1

    pdu_manager = PduManager()
    pdu_manager.initialize(config_path=config_path, comm_service=ShmCommunicationService())
    pdu_manager.start_service_nowait()

    hakopy.conductor_start(delta_time_usec, delta_time_usec)
    if is_external:
        ret = hakopy.init_for_external()
        if ret < 0:
            print(f"ERROR: init_for_external() returns {ret}.")
            return 1
    else:
        ret = hakopy.asset_register(asset_name, config_path, my_callback, delta_time_usec, hakopy.HAKO_ASSET_MODEL_PLANT)
        if ret == False:
            print(f"ERROR: hako_asset_register() returns {ret}.")
            return 1
    ret = hakopy.service_initialize(service_config_path)
    if ret < 0:
        print(f"ERROR: hako_asset_service_initialize() returns {ret}.")
        return 1
    if is_external:
        hakopy.trigger_event(hakopy.HAKO_TRIGGER_EVENT_ID_START)
        my_on_initialize(None)
        my_on_manual_timing_control(None)
    else:
        ret = hakopy.start()
        print(f"INFO: hako_asset_start() returns {ret}")

    hakopy.conductor_stop()
    return 0

if __name__ == "__main__":
    sys.exit(main())
