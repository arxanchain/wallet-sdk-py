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
from rest.api.api import Client

class Response(object):
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

IP = "http://127.0.0.1:9143"
APIKEY = "pWEzB4yMM1518346407"
cert_path = "/your/cert/path"
cert_store = Client(
        APIKEY,
        cert_path,
        IP
        )
response_succ = {
    "ErrCode":0,
    "ErrMessage":"",
    "Method":"",
    "Payload":"{\"code\":0,\"message\":\"\",\"id\":\"did:axn:2ebde184-e3e1-4964-9b8b-403d06494a5f\",\"endpoint\":\"524a81d5a0d4b54c6c10dbfbb447282b4110720198ec55a7440b0041691268d5\",\"key_pair\":{\"private_key\":\"xGw+VdU3XkCCpCZP5vxs2sXIVh/NnJ+bwjSO5rQkAOpKGpHqf5JDJhNbieFJiz7IfR/hmNNE9MI1xnnxNCzamw==\",\"public_key\":\"ShqR6n+SQyYTW4nhSYs+yH0f4ZjTRPTCNcZ58TQs2ps=\"},\"created\":1519893992,\"coin_id\":\"\",\"transaction_ids\":[\"c9d29dba1a6b3f6935c9e8db0fa4a651a83b00ac53eeb4d73e00812bc020486c\",\"83a09d0c5c30a988ac110c14eb4a5612946f2f3f7855aa993dfaef03cb783ecd\",\"1428f7a821b5455aab4e782bfabbe3bad86dbaa99e010d0755988fd37a43c8e2\"]}"}
response_fail = {
    "Method":"",
    "ErrCode":107,
    "ErrMessage":"illegal base64 data at input byte 8",
    "Payload":None
    }

class WalletTest(unittest.TestCase):
    """Wallet test. """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_register_succ(self):
        """ Test register successfully returned. """

        mock_do_request = mock.Mock(return_value=(0, response_succ))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(cert_store)
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

        mock_do_request = mock.Mock(return_value=(0, response_fail))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
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

        mock_do_request = mock.Mock(return_value=(0, response_succ))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
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

        mock_do_request = mock.Mock(return_value=(0, response_fail))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
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

        mock_do_request = mock.Mock(return_value=(0, response_succ))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            id_ = "did:axn:2ef06aa4-05bb-4728-8882-343d42faeb8f"
            _, resp = wc.query_wallet_infos({}, id_)
            self.assertEqual(resp["ErrCode"], 0)

    def test_query_wallet_infos_err(self):
        """ Test query wallet infos with error code. """

        mock_do_request = mock.Mock(return_value=(0, response_fail))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            id_ = "did:axn:2ef06aa4-05bb-4728-8882-343d42faeb8f"
            _, resp = wc.query_wallet_infos({}, id_)
            self.assertEqual(resp["ErrCode"], 107)

    def test_query_wallet_balance_succ(self):
        """ Test query wallet balance successfully returned. """

        mock_do_request = mock.Mock(return_value=(0, response_succ))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            id_ = "did:axn:2ef06aa4-05bb-4728-8882-343d42faeb8f"
            _, resp = wc.query_wallet_balance({}, id_)
            self.assertEqual(resp["ErrCode"], 0)

    def test_query_wallet_balance_err(self):
        """ Test query wallet balance with error code. """

        mock_do_request = mock.Mock(return_value=(0, response_fail))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            id_ = "did:axn:2ef06aa4-05bb-4728-8882-343d42faeb8f"
            _, resp = wc.query_wallet_balance({}, id_)
            self.assertEqual(resp["ErrCode"], 107)


