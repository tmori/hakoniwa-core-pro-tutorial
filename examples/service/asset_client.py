#!/usr/bin/python
# -*- coding: utf-8 -*-
import hakopy
import sys
import time
from hakoniwa_pdu.pdu_manager import PduManager
from hakoniwa_pdu.impl.shm_communication_service import ShmCommunicationService
from hakoniwa_pdu.service.hako_asset_service_config import HakoAssetServiceConfig
from hakoniwa_pdu.service.hako_asset_service_client import HakoAssetServiceClient

from hakoniwa_pdu.pdu_msgs.hako_srv_msgs.pdu_pytype_AddTwoIntsRequest import AddTwoIntsRequest
from hakoniwa_pdu.pdu_msgs.hako_srv_msgs.pdu_pytype_AddTwoIntsResponse import AddTwoIntsResponse
from hakoniwa_pdu.pdu_msgs.hako_srv_msgs.pdu_conv_AddTwoIntsRequestPacket import py_to_pdu_AddTwoIntsRequestPacket, pdu_to_py_AddTwoIntsRequestPacket
from hakoniwa_pdu.pdu_msgs.hako_srv_msgs.pdu_conv_AddTwoIntsResponsePacket import py_to_pdu_AddTwoIntsResponsePacket, pdu_to_py_AddTwoIntsResponsePacket
import asyncio


asset_name = 'Client'
service_name = 'Service/Add'
service_config_path = './examples/service/service.json'
service_client = None
delta_time_usec = 1000 * 1000

def hako_sleep(sec: int):
    #print(f"INFO: hako_sleep({sec})")
    ret = hakopy.usleep(int(sec * 1000 * 1000))
    if ret == False:
        sys.exit(1)
    time.sleep(sec)
    #print(f"INFO: hako_sleep({sec}) done")
    


async def hako_sleep_async(sec: int):
    await asyncio.to_thread(hako_sleep, sec)

def my_on_initialize(context):
    global asset_name
    global service_name
    global service_client
    print(f"INFO: Initializing asset service client for {asset_name}/{service_name}")
    service_client = HakoAssetServiceClient(pdu_manager, asset_name, service_name, "Client01",
                                            py_to_pdu_AddTwoIntsRequestPacket,
                                            pdu_to_py_AddTwoIntsRequestPacket, 
                                            py_to_pdu_AddTwoIntsResponsePacket,
                                            pdu_to_py_AddTwoIntsResponsePacket)
    service_config = HakoAssetServiceConfig(service_config_path, pdu_manager.pdu_convertor.offmap)
    service_config.append_pdu_def(pdu_manager.pdu_config.get_pdudef())
    service_client.service_config = service_config
    if service_client.initialize() == False:
        raise RuntimeError("Failed to create asset service")

    return 0

def my_on_reset(context):
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
    await run_client_task_for_test()
    #await run_client_task_for_normal()

async def run_client_task_for_normal():
    global pdu_manager, service_client, delta_time_usec

    print("*************** START SERVICE CLIENT ***************")
    req = AddTwoIntsRequest()
    req.a = 1
    req.b = 2

    while True:
        # 送信成功までリトライ
        while not service_client.request(req):
            print("INFO: Can not send request")
            await hako_sleep_async(1)

        # レスポンス到着まで待機
        while not service_client.is_response_in(service_client.poll()):
            print("INFO: APL wait for response")
            await hako_sleep_async(1)

        res: AddTwoIntsResponse = service_client.get_response()
        print(f"Response data: {res}")

        # 次のリクエストを作成
        req = AddTwoIntsRequest()
        req.a = res.sum
        req.b = res.sum + 1

async def run_client_task_for_test():
    global pdu_manager
    global service_client
    global delta_time_usec
    is_timeout_heppend = False
    print("*************** START SERVICE CLIENT ***************")
    req = AddTwoIntsRequest()
    req.a = 1
    req.b = 2
    res = AddTwoIntsResponse()
    print(f"Request data: {req}")
    result = service_client.request(req, 2000, -1)
    if result == False:
        print("ERROR: Failed to send request")
        return -1
    print("INFO: APL wait for response ")

    while True:
        await hako_sleep_async(1)
        event = service_client.poll()
        if event < 0:
            print(f"ERROR: Failed to poll asset service client: {event}")
            return -1
        if service_client.is_response_in(event):
            res = service_client.get_response()
            print(f"Response data: {res}")
            break
        if service_client.is_request_timeout(event):
            print("INFO: Request timeout")
            is_timeout_heppend = True
            break
    if is_timeout_heppend:
        print("WARNING: APL cancel request is happened.")
        while service_client.cancel_request() == False:
            print("INFO: APL cancel_request() is not done")
            await hako_sleep_async(1)
        print("INFO: APL cancel_request() is done")
        while True:
            event = service_client.poll()
            if event < 0:
                print(f"ERROR: Failed to poll asset service client: {event}")
                return -1
            if service_client.is_request_cancel_done(event):
                print("INFO: Request cancel done")
                break
            elif service_client.is_response_in(event):
                res = service_client.get_response()
                print(f"Response data: {res}")
                break
            else:
                print("INFO: Request cancel is not done")
            await hako_sleep_async(1)

    print("*************** FINISH SERVICE CLIENT ***************")
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
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <config_path> [external]")
        return 1

    config_path = sys.argv[1]
    delta_time_usec = 1000 * 1000
    isExternal = False
    if len(sys.argv) == 3 and sys.argv[2] == 'external':
        isExternal = True
        print("INFO: external mode")

    pdu_manager = PduManager()
    pdu_manager.initialize(config_path=config_path, comm_service=ShmCommunicationService())
    pdu_manager.start_service_nowait()

    if isExternal:
        ret = hakopy.init_for_external()
    else:
        ret = hakopy.asset_register(asset_name, config_path, my_callback, delta_time_usec, hakopy.HAKO_ASSET_MODEL_CONTROLLER)
    if ret == False:
        print(f"ERROR: hako_asset_register() returns {ret}.")
        return 1
    ret = hakopy.service_initialize(service_config_path)
    if ret < 0:
        print(f"ERROR: hako_asset_service_initialize() returns {ret}.")
        return 1
    
    if isExternal:
        my_on_initialize(None)
        my_on_manual_timing_control(None)
    else:
        ret = hakopy.start()
        print(f"INFO: hako_asset_start() returns {ret}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
