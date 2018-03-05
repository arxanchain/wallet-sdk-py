"""
Copyright ArxanFintech Technology Ltd. 2018 All Rights Reserved.

Licensed under the Apache License, Version 1.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

                 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import unittest
import mock
import os
import sys
import json
ROOTPATH = os.path.join(
    os.path.dirname(__file__),
    "../"
    )
sys.path.append(ROOTPATH)
from api.wallet import WalletClient

class Response(object):
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

class WalletTest(unittest.TestCase):
    """Wallet test. """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_register_succ(self):
        """ Test register successfully returned. """
        response = {
            "ErrCode":0,
            "ErrMessage":"",
            "Method":"",
            "Payload":"{\"code\":0,\"message\":\"\",\"id\":\"did:axn:2ebde184-e3e1-4964-9b8b-403d06494a5f\",\"endpoint\":\"524a81d5a0d4b54c6c10dbfbb447282b4110720198ec55a7440b0041691268d5\",\"key_pair\":{\"private_key\":\"xGw+VdU3XkCCpCZP5vxs2sXIVh/NnJ+bwjSO5rQkAOpKGpHqf5JDJhNbieFJiz7IfR/hmNNE9MI1xnnxNCzamw==\",\"public_key\":\"ShqR6n+SQyYTW4nhSYs+yH0f4ZjTRPTCNcZ58TQs2ps=\"},\"created\":1519893992,\"coin_id\":\"\",\"transaction_ids\":[\"c9d29dba1a6b3f6935c9e8db0fa4a651a83b00ac53eeb4d73e00812bc020486c\",\"83a09d0c5c30a988ac110c14eb4a5612946f2f3f7855aa993dfaef03cb783ecd\",\"1428f7a821b5455aab4e782bfabbe3bad86dbaa99e010d0755988fd37a43c8e2\"]}"}
        client_cipher = "client cipher"
        server_cipher = "server cipher"
        mock_do_post = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[client_cipher, json.dumps(response)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                wc = WalletClient("http://127.0.0.1:9143", "pWEzB4yMM1518346407", "")
                body={
                    "id": "did:axn:21tDAKCERh95uGgKbJNHYp",
                    "type": "Organization",
                    "access": "xxxxx",
                    "secret": "xxxx",
                    "public_key":  {
                        "usage": "SignVerify",
                        "key_type": "EdDsaPublicKey",
                        "public_key_data": "dGhpcyBpcyBhIHB1YmxpYyBrZXl0aGlzIGlzIGEgcHVibGljIGtleXRoaXMgaXMgYSBwdWJsaWMga2V5dGhpcyBpcyBhIHB1YmxpYyBrZXl0aGlzIGlzIGEgcHVibGljIGtleXRoaXMgaXMgYSBwdWJsaWMga2V5dGhpcyBpcyBhIHB1YmxpYyBrZXk="
                    }
                }
                _, resp = wc.register({}, body)
                self.assertEqual(resp["ErrCode"], 0)

    def test_register_err(self):
        """ Test register with error code. """
        response = {
            "Method":"",
            "ErrCode":107,
            "ErrMessage":"illegal base64 data at input byte 8",
            "Payload":None
            }
        client_cipher = "client cipher"
        server_cipher = "server cipher"
        mock_do_post = mock.Mock(return_value=Response(400, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[client_cipher, json.dumps(response)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                wc = WalletClient("http://127.0.0.1:9143", "pWEzB4yMM1518346407", "")
                body={
                    "id": "did:axn:21tDAKCERh95uGgKbJNHYp",
                    "type": "Organization",
                    "access": "xxxxx",
                    "secret": "xxxx",
                    "public_key":  {
                        "usage": "SignVerify",
                        "key_type": "EdDsaPublicKey",
                        "public_key_data": "dGhpcyBpcyBhIHB1YmxpYyBrZXl0aGlzIGlzIGEgcHVibGljIGtleXRoaXMgaXMgYSBwdWJsaWMga2V5dGhpcyBpcyBhIHB1YmxpYyBrZXl0aGlzIGlzIGEgcHVibGljIGtleXRoaXMgaXMgYSBwdWJsaWMga2V5dGhpcyBpcyBhIHB1YmxpYyBrZXk="
                    }
                }
                _, resp = wc.register({}, body)
                self.assertEqual(resp["ErrCode"], 107)

    def test_register_sub_succ(self):
        """ Test register sub wallet successfully returned. """
        response = {
            "ErrCode": 0,
            "ErrMessage": "",
            "Method": "",
            "Payload": "{\"code\":0,\"message\":\"\",\"id\":\"did:axn:769de30d-2170-453d-81ce-b8f566be1e7a#Organization\",\"endpoint\":\"d9f0f47af158609ef97399a7c38cf7885a0c32da5b4145706361ff6c7a3520e3\",\"key_pair\":{\"private_key\":\"QU9T6vN3g4q3MLAUL8YJxK90bBWvOw+QW4zONXSR1acNCG8tblPVcK/jzKFA/QRyQ+4lv3KN5JfMJRzek05NNw==\",\"public_key\":\"DQhvLW5T1XCv48yhQP0EckPuJb9yjeSXzCUc3pNOTTc=\"},\"created\":1519702836,\"coin_id\":\"\",\"transaction_ids\":[\"1e0edec693c1a22656d5db23d66b91ab9df0dcefef025dd293228e324fc8de4c\",\"bf6e2be1ab2fb0b66be2ee67732c885853524416e4904b6124cc9c5d2b1736d0\"]}"
        }
        client_cipher = "client cipher"
        server_cipher = "server cipher"

        mock_do_post = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[client_cipher, json.dumps(response)])
        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                wc = WalletClient("http://127.0.0.1:9143", "pWEzB4yMM1518346407", "")
                body={
                    "id": "did:axn:21tDAKCERh95uGgKbJNHYp",
                    "type": "Organization",
                    "access": "xxxxx",
                    "secret": "xxxx",
                    "public_key":  {
                        "usage": "SignVerify",
                        "key_type": "EdDsaPublicKey",
                        "public_key_data": "dGhpcyBpcyBhIHB1YmxpYyBrZXl0aGlzIGlzIGEgcHVibGljIGtleXRoaXMgaXMgYSBwdWJsaWMga2V5dGhpcyBpcyBhIHB1YmxpYyBrZXl0aGlzIGlzIGEgcHVibGljIGtleXRoaXMgaXMgYSBwdWJsaWMga2V5dGhpcyBpcyBhIHB1YmxpYyBrZXk="
                    }
                }
                _, resp = wc.register_sub_wallet({}, body)
                self.assertEqual(resp["ErrCode"], 0)

    def test_register_sub_err(self):
        """ Test register sub wallet with error code. """
        response = {
            "Method":"",
            "ErrCode":107,
            "ErrMessage":"illegal base64 data at input byte 8",
            "Payload":None
        }
        client_cipher = "client cipher"
        server_cipher = "server cipher"

        mock_do_post = mock.Mock(return_value=Response(400, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[client_cipher, json.dumps(response)])
        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                wc = WalletClient("http://127.0.0.1:9143", "pWEzB4yMM1518346407", "")
                body={
                    "id": "did:axn:21tDAKCERh95uGgKbJNHYp",
                    "type": "Organization",
                    "access": "xxxxx",
                    "secret": "xxxx",
                    "public_key":  {
                        "usage": "SignVerify",
                        "key_type": "EdDsaPublicKey",
                        "public_key_data": "dGhpcyBpcyBhIHB1YmxpYyBrZXl0aGlzIGlzIGEgcHVibGljIGtleXRoaXMgaXMgYSBwdWJsaWMga2V5dGhpcyBpcyBhIHB1YmxpYyBrZXl0aGlzIGlzIGEgcHVibGljIGtleXRoaXMgaXMgYSBwdWJsaWMga2V5dGhpcyBpcyBhIHB1YmxpYyBrZXk="
                    }
                }
                _, resp = wc.register_sub_wallet({}, body)
                self.assertEqual(resp["ErrCode"], 107)

    def test_query_wallet_infos_succ(self):
        """ Test query wallet infos successfully returned. """
        response = {
            "ErrCode":0,
            "ErrMessage":"",
            "Method":"",
            "Payload":"{\"id\":\"did:axn:2ef06aa4-05bb-4728-8882-343d42faeb8f\",\"type\":\"Organization\",\"endpoint\":\"08a9c5bacda37958d632cb37d4970856b58876e4009e4a8e2220395ac621cc64\",\"status\":\"Valid\",\"created\":1519726724,\"updated\":0,\"hds\":null}"
            }
        server_cipher = "server cipher"
        mock_do_get = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(return_value=json.dumps(response))

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.get', mock_do_get):
                wc = WalletClient("http://127.0.0.1:9143", "pWEzB4yMM1518346407", "")
                id_ = "did:axn:2ef06aa4-05bb-4728-8882-343d42faeb8f"
                _, resp = wc.query_wallet_infos({}, id_)
                self.assertEqual(resp["ErrCode"], 0)

    def test_query_wallet_infos_err(self):
        """ Test query wallet infos with error code. """
        response = {
            "Method":"",
            "ErrCode":107,
            "ErrMessage":"illegal base64 data at input byte 8",
            "Payload":None
            }
        server_cipher = "server cipher"
        mock_do_get = mock.Mock(return_value=Response(400, server_cipher))
        mock_run_cmd = mock.Mock(return_value=json.dumps(response))

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.get', mock_do_get):
                wc = WalletClient("http://127.0.0.1:9143", "pWEzB4yMM1518346407", "")
                id_ = "did:axn:2ef06aa4-05bb-4728-8882-343d42faeb8f"
                _, resp = wc.query_wallet_infos({}, id_)
                self.assertEqual(resp["ErrCode"], 107)

    def test_query_wallet_balance_succ(self):
        """ Test query wallet balance successfully returned. """
        response = {
            "ErrCode":0,
            "ErrMessage":"",
            "Method":"",
            "Payload":"{\"id\":\"did:axn:2ef06aa4-05bb-4728-8882-343d42faeb8f\",\"type\":\"Organization\",\"endpoint\":\"08a9c5bacda37958d632cb37d4970856b58876e4009e4a8e2220395ac621cc64\",\"status\":\"Valid\",\"created\":1519726724,\"updated\":0,\"hds\":null}"
            }
        server_cipher = "server cipher"
        mock_do_get = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(return_value=json.dumps(response))

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.get', mock_do_get):
                wc = WalletClient("http://127.0.0.1:9143", "pWEzB4yMM1518346407", "")
                id_ = "did:axn:2ef06aa4-05bb-4728-8882-343d42faeb8f"
                _, resp = wc.query_wallet_balance({}, id_)
                self.assertEqual(resp["ErrCode"], 0)

    def test_query_wallet_balance_err(self):
        """ Test query wallet balance with error code. """
        response = {
            "Method":"",
            "ErrCode":107,
            "ErrMessage":"illegal base64 data at input byte 8",
            "Payload":None
            }
        server_cipher = "server cipher"
        mock_do_get = mock.Mock(return_value=Response(400, server_cipher))
        mock_run_cmd = mock.Mock(return_value=json.dumps(response))

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.get', mock_do_get):
                wc = WalletClient("http://127.0.0.1:9143", "pWEzB4yMM1518346407", "")
                id_ = "did:axn:2ef06aa4-05bb-4728-8882-343d42faeb8f"
                _, resp = wc.query_wallet_balance({}, id_)
                self.assertEqual(resp["ErrCode"], 107)
