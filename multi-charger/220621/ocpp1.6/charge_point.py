import asyncio
import logging
from urllib import request
from flask import Flask, request, jsonify
import json
# import socket


try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys
    sys.exit(1)


from ocpp.v16 import call
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import RegistrationStatus
import requests

logger = logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


class ChargePoint(cp):
    async def send_boot_notification(self, reason, cp_model, cp_vendor, cp_sn, fw_version, imsi, rsi, entityid):
        request = call.BootNotificationPayload(
            Reason=reason,
            charge_point_model=cp_model,
            charge_point_vendor=cp_vendor,
            charge_point_serial_number=cp_sn,
            firmware_version=fw_version,
            Imsi=imsi,
            rssi=rsi,
            Entityid=entityid
        )

        msg = cp.start(self)
        response = await self.call(request)
        print(f"msg:::{msg}")
        print(f"response:::::{response}")
        if response.status == RegistrationStatus.accepted:
            print("Connected to central system.")
        return msg

    async def send_status_notification(self):
        request = call.StatusNotificationPayload(
            connector_id=123,
            error_code="NoError",
            status='Available',
            timestamp='2022-06-13',
            vendor_id="dd123",
        )
        print(f"req::{request}")
        msg = cp.start(self)
        response = await self.call(request)
        print(f"msg:::{msg}")
        print(f"response:::::{response}")
        return msg

    async def send_data_transfer(self):
        request = call.DataTransferPayload(
            vendor_id="helloId",
            message_id="option id",
            data="datas"
        )

        response = await self.call(request)


async def main():
    app = Flask(__name__)

    @app.route('/')
    def greeting():
        return "This is Test API ! "

    @app.route('/status')
    async def send_status_notification():
        async with websockets.connect(
            'ws://15.164.218.59:9000/CP_1',
            subprotocols=['ocpp1.6']
        ) as ws:

            cp = ChargePoint('CP_1', ws)

            msg = await asyncio.gather(cp.start(), cp.send_status_notification())
            print(f"fgfgfg:::{msg[0]}")
        return msg[0]
             
        
    @app.route('/boot')
    async def send_boot_notification():        
        async with websockets.connect(
            'ws://15.164.218.59:9000/CP_1',
            subprotocols=['ocpp1.6']
        ) as ws:

            cp = ChargePoint('CP_1', ws)

            msg = await asyncio.gather(cp.start(), cp.send_boot_notification(
                reason="ApplicationReset", cp_model="Optimus",
                cp_vendor="First C&D", cp_sn="first001", fw_version="V0.1",
                imsi="010-0000-0000", rsi=123213, entityid="hello11233"))
            splited = msg[0].split("{")
            splited = splited[1].split("}")
            data_str = "{" + splited[0] + "}"
            jsonStr = json.loads(data_str)
            print(f"splited::{jsonStr}")
            # splited = splited[0].split(",")
            # print(f"boot:::{splited}") 
        return jsonStr
    @app.route('/create', methods=['POST'])
    def create():
        print(request.is_json)
        params = request.get_json()
        print(params)
        return 'ok'

    app.run(debug=True)
    # async with websockets.connect(
    #     'ws://localhost:9000/CP_1',
    #     subprotocols=['ocpp1.6']
    # ) as ws:

    #     cp = ChargePoint('CP_1', ws)

    #     await asyncio.gather(cp.start(), cp.send_data_transfer())


if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())