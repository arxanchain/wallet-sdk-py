# -*- coding: utf-8 -*-

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
create_poe_payload = {
    "id": "",
    "name": "name",
    "parent_id": "parent-poe-id",
    "owner": "owner did",
    "hash": "metadata-hash",
    "metadata": map(ord, '{"address": "北京市", "telephone": "xxx"}')
}
proposal_succ = {
    "ErrMessage": "",
    "Payload": '{"token_id":"687b92d5e2fff8b46e408046399efc19329b443371e0c4298656e1f07e1c0795","txs":[{"version":1,"timestamp":{"time":{"seconds":1528364102,"nanos":232784168}},"txin":[{"ix":4294967295}],"txout":[{"cTokenId":"687b92d5e2fff8b46e408046399efc19329b443371e0c4298656e1f07e1c0795","cType":1,"value":393,"addr":"did:axn:15b17cb2-21c8-4de6-ac07-f9fd1fbe4d93","until":-1,"script":"eyJwdWJsaWNLZXkiOiIzdnNxWUFSQkQ0Z2RNTnh6VTdyMG1ZT3grWVorYlhPK29WWHNkZEI4S0VVPSJ9"}],"founder":"did:axn:8uQhQMGzWxR8vw5P3UWH1j"}]}',
    "ErrCode": 0,
    "Method": ""
    }

proposal_ctoken_succ = {
    "ErrMessage": "",
    "Payload": '[{"txin": [{"sourceHash": "25IOjlVtNJeVeFaRpyFStKaDYfXAEHimD7FbHq4YpW4="}], "founder": "did:axn:8uQhQMGzWxR8vw5P3UWH1j", "timestamp": {"time": {"seconds": 1528446360, "nanos": 854334288}}, "txType": 1, "version": 1, "txout": [{"addr": "did:axn:d435be4b-046a-4a7c-b3a7-29e11d5e8c18", "script": "eyJwdWJsaWNLZXkiOiJ0V2Myck1oNS9jRFo5OTYvM0lNRFNaWEVGd2VTcVBuU0trUHVrMFNDdkhBPSJ9", "cTokenId": "1e1d5e6716274608d054cfc4385786681549ed0b70c4ec44ee6a50ba3e0332b6", "cType": 1, "value": 55, "until": -1}, {"addr": "did:axn:e9dee062-21de-43dd-9d33-ba68cba523e5", "script": "eyJwdWJsaWNLZXkiOiIxUTJxcG14amNQMEg4Qkp1a09FSUYycHhlRU4xZElIQXZsT1N2M1dtMVU0PSJ9", "cTokenId": "1e1d5e6716274608d054cfc4385786681549ed0b70c4ec44ee6a50ba3e0332b6", "cType": 1, "value": 497, "until": -1}]}]',
    "ErrCode": 0,
    "Method": ""
}

proposal_asset_succ = {
    "ErrMessage": "",
    "Payload": '[{"txin": [{"sourceHash": "25IOjlVtNJeVeFaRpyFStKaDYfXAEHimD7FbHq4YpW4="}], "founder": "did:axn:8uQhQMGzWxR8vw5P3UWH1j", "timestamp": {"time": {"seconds": 1528446360, "nanos": 854334288}}, "txType": 1, "version": 1, "txout": [{"addr": "did:axn:d435be4b-046a-4a7c-b3a7-29e11d5e8c18", "script": "eyJwdWJsaWNLZXkiOiJ0V2Myck1oNS9jRFo5OTYvM0lNRFNaWEVGd2VTcVBuU0trUHVrMFNDdkhBPSJ9", "cTokenId": "1e1d5e6716274608d054cfc4385786681549ed0b70c4ec44ee6a50ba3e0332b6", "cType": 1, "value": 55, "until": -1}, {"addr": "did:axn:e9dee062-21de-43dd-9d33-ba68cba523e5", "script": "eyJwdWJsaWNLZXkiOiIxUTJxcG14amNQMEg4Qkp1a09FSUYycHhlRU4xZElIQXZsT1N2M1dtMVU0PSJ9", "cTokenId": "1e1d5e6716274608d054cfc4385786681549ed0b70c4ec44ee6a50ba3e0332b6", "cType": 1, "value": 497, "until": -1}]}]',
    "ErrCode": 0,
    "Method": ""
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
            params = {
                "creator": fromdid,
                "created": create_time,
                "privateB64": secret_key_b64,
                "payload": create_poe_payload,
                "nonce": ""
            }

            _, resp = wc.create_poe({}, payload, params)
            self.assertEqual(resp["ErrCode"], 0)

    def test_create_poe_fail(self):
        """Test create POE with ed25519 signed body failed returned. """

        mock_do_request = mock.Mock(return_value=(0, response_fail))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            params = {
                "creator": fromdid,
                "created": create_time,
                "privateB64": secret_key_b64,
                "payload": create_poe_payload,
                "nonce": ""
            }

            _, resp = wc.create_poe({}, payload, params)
            self.assertEqual(resp["ErrCode"], 107)

    def test_update_poe_succ(self):
        """Test update poe with ed25519 signed body successfully returned. """

        mock_do_request = mock.Mock(return_value=(0, response_succ))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            params = {
                "creator": fromdid,
                "created": create_time,
                "privateB64": secret_key_b64,
                "payload": payload,
                "nonce": ""
            }

            _, resp = wc.update_poe({}, payload, params)
            self.assertEqual(resp["ErrCode"], 0)

    def test_update_poe_fail(self):
        """Test update poe with ed25519 signed body failed returned. """

        mock_do_request = mock.Mock(return_value=(0, response_fail))
        with mock.patch('rest.api.api.Client.do_request', mock_do_request):
            wc = WalletClient(
                    cert_store
                    )
            params = {
                "creator": fromdid,
                "created": create_time,
                "privateB64": secret_key_b64,
                "payload": payload,
                "nonce": ""
            }

            _, resp = wc.update_poe({}, payload, params)
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
            readonly = "True"
            wc = WalletClient(
                    cert_store
                    )
            _, resp = wc.upload_poe({}, file_, poeid, readonly)
            self.assertEqual(resp["ErrCode"], 0)

    def test_upload_poe_err(self):

        mock_do_prepare = mock.Mock(return_value=(0, response_fail))
        with mock.patch('rest.api.api.Client.do_prepare', mock_do_prepare):
            file_ = "{}/requirements.txt".format(os.getcwd())
            poeid = "poe id"
            readonly = "True"
            wc = WalletClient(
                    cert_store
                    )
            _, resp = wc.upload_poe({}, file_, poeid, readonly)
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

        mock_do_request = mock.Mock(side_effect=[(0, proposal_ctoken_succ), (0, response_succ)])
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

        mock_do_request = mock.Mock(side_effect=[(0, proposal_ctoken_succ), (0, response_fail)])
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

        mock_do_request = mock.Mock(side_effect=[(0, proposal_ctoken_succ), (0, response_succ)])
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

        mock_do_request = mock.Mock(side_effect=[(0, proposal_ctoken_succ), (0, response_fail)])
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
        mock_do_request = mock.Mock(side_effect=[(0, proposal_ctoken_succ), (0, response_succ)])
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

        mock_do_request = mock.Mock(side_effect=[(0, proposal_ctoken_succ), (0, response_fail)])
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
