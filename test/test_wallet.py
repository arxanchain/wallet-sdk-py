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
from cryption.crypto import sign

class Response(object):
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

IP = "http://127.0.0.1:9143"
APIKEY = "pWEzB4yMM1518346407"
cert_path = "/your/cert/path"
ent_sign_param = {}
cert_store = Client(
        APIKEY,
        cert_path,
        ent_sign_param,
        IP
        )
secret_key_b64 = "0lxEFzMQhn68vY2F0f+nOwP7kl5zjahjPcfyMAJVmzn0HNQssIIYh+c2CgCKEHeUvxqCu6W/sJKqKt2DLJnKpw=="
nonce = "nonce"
did = "did:ara:8uQhQMGzWxR8vw5P3UWH1j"
fromdid = "did:ara:9uQhQMGzWxR8vw5P3UWH1b"
create_time = "1517818060"
payload = {
    "from": "did:axn:8uQhQMGzWxR8vw5P3UWH1j",
    "to": "did:axn:21tDAKCERh95uGgKbJNHYp",
    "issuer": "did:axn:8uQhQMGzWxR8vw5P3UWH1j",
    "asset_id": "1f38a7a1-2c79-465e-a4c0-0038e25c7edg",
    "tokens": [
        {
            "token_id": "0684f2fccc8c3209d34c0ab3d8f690b2c88c9aa87cad41259e981ba9556f42e7",
            "amount": 5
        }
    ],
    "fee": {
        "amount": 10
    }
}

proposal_resp = {
    "token_id": "0684f2fccc8c3209d34c0ab3d8f690b2c88c9aa87cad41259e981ba9556f42e7",
    "txs": [
        {
            "version": 1,
            "timestamp": {
                "time": {
                    "seconds": 1524901510,
                    "nanos": 312840217
                }
            },
            "txin": [
                {
                    "ix": 4294967295
                }
            ],
            "txout": [
                {
                    "cTokenId": "9483625bb644c7b69a92b53e119536ec58761ef01fe5fe4aaf61f2ccbf301c91",
                    "cType": 1,
                    "value": 1000,
                    "addr": "did:axn:65tGAKCERh95uHllllllRU",
                    "until": -1,
                    "script": {
                        "creator": "",
                        "created": 0,
                        "nonce": "",
                        "signature": "",
                        "publicKey": "CkBkNjdmN2VkNGU5M2NhMzk1MmM4NDgzZGNlN2Y4YTExZmRmOTEyNmU2ZTU2NWMzNzk3MTA1NjkzMWRiMjBkZjEy"
                    }
                }
            ],
            "txType": 0,
            "founder": "did:axn:8uQhQMGzWxR8vw5P3UWH1j"
        }
    ]
}
proposal_succ = {
    "ErrCode":0,
    "ErrMessage":"",
    "Method":"",
    "Payload": json.dumps(proposal_resp)
}
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

    def test_create_poe_succ(self):
        """Test create POE with ed25519 signed body successfully returned. """

        mock_do_request = mock.Mock(return_value=(0, response_succ))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            _, resp = wc.create_poe({}, fromdid, create_time, secret_key_b64, payload)
            self.assertEqual(resp["ErrCode"], 0)

    def test_create_poe_fail(self):
        """Test create POE with ed25519 signed body failed returned. """

        mock_do_request = mock.Mock(return_value=(0, response_fail))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            _, resp = wc.create_poe({}, fromdid, create_time, secret_key_b64, payload)
            self.assertEqual(resp["ErrCode"], 107)

    def test_update_poe_succ(self):
        """Test update poe with ed25519 signed body successfully returned. """

        mock_do_request = mock.Mock(return_value=(0, response_succ))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            _, resp = wc.update_poe({}, fromdid, create_time, secret_key_b64, payload)
            self.assertEqual(resp["ErrCode"], 0)

    def test_update_poe_fail(self):
        """Test update poe with ed25519 signed body failed returned. """

        mock_do_request = mock.Mock(return_value=(0, response_fail))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            _, resp = wc.update_poe({}, fromdid, create_time, secret_key_b64, payload)
            self.assertEqual(resp["ErrCode"], 107)

    def test_query_poe_succ(self):
        mock_do_request = mock.Mock(return_value=(0, response_succ))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            _, resp = wc.query_poe({}, fromdid)
            self.assertEqual(resp["ErrCode"], 0)

    def test_query_poe_err(self):

        mock_do_request = mock.Mock(return_value=(0, response_fail))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            _, resp = wc.query_poe({}, fromdid)
            self.assertEqual(resp["ErrCode"], 107)

    def test_upload_poe_succ(self):

        mock_do_prepare = mock.Mock(return_value=(0, response_succ))
        with mock.patch('rest.api.api.Client.do_prepare', mock_do_prepare):
            file_ = "{}/requirements.txt".format(os.getcwd())
            poeid = "poe id"
            wc = WalletClient(
                    cert_store
                    )
            _, resp = wc.upload_poe({}, file_, poeid)
            self.assertEqual(resp["ErrCode"], 0)

    def test_upload_poe_err(self):

        mock_do_prepare = mock.Mock(return_value=(0, response_fail))
        with mock.patch('rest.api.api.Client.do_prepare', mock_do_prepare):
            file_ = "{}/requirements.txt".format(os.getcwd())
            poeid = "poe id"
            wc = WalletClient(
                    cert_store
                    )
            _, resp = wc.upload_poe({}, file_, poeid)
            self.assertEqual(resp["ErrCode"], 107)

    def test_query_txn_logs_with_endpoint_succ(self):
    
        mock_do_request = mock.Mock(return_value=(0, response_succ))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            _, resp = wc.query_txn_logs_with_endpoint({}, "in", "endpoint001")
            self.assertEqual(resp["ErrCode"], 0)

    def test_query_txn_logs_with_endpoint_err(self):
        mock_do_request = mock.Mock(return_value=(0, response_fail))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            _, resp = wc.query_txn_logs_with_endpoint({}, "in", "endpoint001")
            self.assertEqual(resp["ErrCode"], 107)

    def test_query_txn_logs_with_id_succ(self):
        mock_do_request = mock.Mock(return_value=(0, response_succ))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            _, resp = wc.query_txn_logs_with_id({}, "in", "yourID")
            self.assertEqual(resp["ErrCode"], 0)

    def test_query_txn_logs_with_id_err(self):
        mock_do_request = mock.Mock(return_value=(0, response_fail))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            _, resp = wc.query_txn_logs_with_id({}, "in", "yourID")
            self.assertEqual(resp["ErrCode"], 107)

    def test_transfer_asset_succ(self):
        """Test transfer asset successfully returned. """

        mock_do_request = mock.Mock(side_effect=[(0, proposal_succ), (0, response_succ)])
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            body = {
                "payload": json.dumps(payload),
                "creator": did,
                "created": create_time,	
                "nonce": nonce,
                "privateB64": secret_key_b64
            }
            _, resp = wc.transfer_assets({}, payload, body)
            self.assertEqual(resp["ErrCode"], 0)


    def test_transfer_asset_err(self):
        """Test transfer asset with error code. """

        mock_do_request = mock.Mock(side_effect=[(0, proposal_succ), (0, response_fail)])
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            body = {
                "payload": json.dumps(payload),
                "creator": did,
                "created": create_time,	
                "nonce": nonce,
                "privateB64": secret_key_b64
            }
            _, resp = wc.transfer_assets({}, payload, body)
            self.assertEqual(resp["ErrCode"], 107)

    def test_transfer_colored_tokens_succ(self):
        """Test transfer colored token successfully returned. """

        mock_do_request = mock.Mock(side_effect=[(0, proposal_succ), (0, response_succ)])
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            body = {
                "payload": json.dumps(payload),
                "creator": did,
                "created": create_time,	
                "nonce": nonce,
                "privateB64": secret_key_b64
            }
            _, resp = wc.transfer_colored_tokens({}, payload, body)
            self.assertEqual(resp["ErrCode"], 0)

    def test_transfer_colored_tokens_err(self):
        """Test transfer colored tokens with error code. """

        mock_do_request = mock.Mock(side_effect=[(0, proposal_succ), (0, response_fail)])
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            body = {
                "payload": json.dumps(payload),
                "creator": did,
                "created": create_time,	
                "nonce": nonce,
                "privateB64": secret_key_b64
            }
            _, resp = wc.transfer_colored_tokens({}, payload, body)
            self.assertEqual(resp["ErrCode"], 107)

    def test_issue_asset_succ(self):
        """Test issue asset successfully returned. """ 
        mock_do_request = mock.Mock(side_effect=[(0, proposal_succ), (0, response_succ)])
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            body = {
                "payload": json.dumps(payload),
                "creator": did,
                "created": create_time,	
                "nonce": nonce,
                "privateB64": secret_key_b64
            }
            _, resp = wc.issue_asset({}, payload, body)
            self.assertEqual(resp["ErrCode"], 0)


    def test_issue_asset_err(self):
        """Test issue asset with error code. """

        mock_do_request = mock.Mock(side_effect=[(0, proposal_succ), (0, response_fail)])
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(cert_store)
            body = {
                "payload": json.dumps(payload),
                "creator": did,
                "created": create_time,	
                "nonce": nonce,
                "privateB64": secret_key_b64
            }   
            _, resp = wc.issue_asset({}, payload, body)
            self.assertEqual(resp["ErrCode"], 107)
