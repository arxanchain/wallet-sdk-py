"""
Copyright ArxanFintech Technology Ltd. 2018 All Rights Reserved.
Licensed under the Apache License, Version 2.0 (the "License");
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
import json
import os
import sys
from cryption.crypto import sign
ROOT_PATH = os.path.join(
    os.path.dirname(__file__),
    ".."
    )
sys.path.append(ROOT_PATH)
from api.transaction import Transaction
from rest.api.api import Client

class Response(object):
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

response_succ = {
    "ErrCode":0,
    "ErrMessage":"",
    "Method":"",
    "Payload":"payload string"
    }

response_fail = {
    "Method":"",
    "ErrCode":107,
    "ErrMessage":"illegal base64 data at input byte 8",
    "Payload":None
    }

url = "http://127.0.0.1"
apikey = "alice"
APIKEY = "pWEzB4yMM1518346407"
secret_key_b64 = "0lxEFzMQhn68vY2F0f+nOwP7kl5zjahjPcfyMAJVmzn0HNQssIIYh+c2CgCKEHeUvxqCu6W/sJKqKt2DLJnKpw=="
nonce = "nonce"
did = "did:ara:8uQhQMGzWxR8vw5P3UWH1j"
todid = "did:axn:21tDAKCERh95uGgKbJNHYp"
asset_id = "1f38a7a1-2c79-465e-a4c0-0038e25c7edg"
coin_id = "1f38a7a1-2c79-465e-a4c0-0038e25c7edg"
cert_path = "./cert_path"
create_time = "1517818060"
payload = {
    "from": did,
    "to": todid,
    "asset_id": asset_id,
    "coins": [
    	{
    	    "coin_id": coin_id,
    	    "amount": 5
    	}
    ],
    "fees": {
    	"accounts": [
    	    did
    	],
    	"coins": [
    	    {
    	    	"coin_id": coin_id,
    	    	"amount": 5
    	    }
    	]
    }
}
sig_cipher = "signed cipher"

cert_store = Client(
        APIKEY,
        cert_path,
        url
        )
tc = Transaction(cert_store)
client_cipher = "client cipher"
server_cipher = "server cipher"

class TransactionTest(unittest.TestCase):
    """Transaction test. """
    def setUp(self):
        pass

    def test_transfer_asset_succ(self):
        """Test transfer asset successfully returned. """

        mock_do_post = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response_succ)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                signature = sign(json.dumps(payload), secret_key_b64, did, nonce)
                body = {
                    "payload": json.dumps(payload),
                    "signature": {
                    	"creator": did,
                    	"created": create_time,	
                    	"nonce": nonce,
                    	"signature_value": signature
                    }
                }
                _, resp = tc.transfer_assets({}, body)
                self.assertEqual(resp["ErrCode"], 0)

    def test_transfer_asset_err(self):
        """Test transfer asset with error code. """

        mock_do_post = mock.Mock(return_value=Response(401, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response_fail)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                signature = sign(json.dumps(payload), secret_key_b64, did, nonce)
                body = {
                    "payload": json.dumps(payload),
                    "signature": {
                    	"creator": did,
                    	"created": create_time,	
                    	"nonce": nonce,
                    	"signature_value": signature
                    }
                }
                _, resp = tc.transfer_assets({}, body)
                self.assertEqual(resp["ErrCode"], 107)

    def test_transfer_asset_with_sign_succ(self):
        """Test transfer asset with ed25519 signed body successfully returned. """

        mock_do_post = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response_succ)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                _, resp = tc.transfer_assets_with_sign({}, did, create_time, secret_key_b64, payload)
                self.assertEqual(resp["ErrCode"], 0)

    def test_transfer_colored_tokens_succ(self):
        """Test transfer colored token successfully returned. """

        mock_do_post = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response_succ)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                signature = sign(json.dumps(payload), secret_key_b64, did, nonce)
                body = {
                    "payload": json.dumps(payload),
                    "signature": {
                    	"creator": did,
                    	"created": create_time,	
                    	"nonce": nonce,
                    	"signature_value": signature
                    }
                }
                _, resp = tc.transfer_colored_tokens({}, body)
                self.assertEqual(resp["ErrCode"], 0)

    def test_transfer_colored_tokens_err(self):
        """Test transfer colored tokens with error code. """

        mock_do_post = mock.Mock(return_value=Response(401, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response_fail)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                signature = sign(json.dumps(payload), secret_key_b64, did, nonce)
                body = {
                    "payload": json.dumps(payload),
                    "signature": {
                    	"creator": did,
                    	"created": create_time,	
                    	"nonce": nonce,
                    	"signature_value": signature
                    }
                }
                _, resp = tc.transfer_colored_tokens({}, body)
                self.assertEqual(resp["ErrCode"], 107)

    def test_transfer_colored_tokens_with_sign_succ(self):
        """Test transfer colored token with ed25519 signed body successfully returned. """
        mock_do_post = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response_succ)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                _, resp = tc.transfer_colored_tokens_with_sign({}, did, create_time, secret_key_b64, payload)
                self.assertEqual(resp["ErrCode"], 0)

    def test_issue_colored_token_succ(self):
        """Test issue colored token successfully returned"""

        mock_do_post = mock.Mock(return_value=Response(401, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response_succ)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                signature = sign(json.dumps(payload), secret_key_b64, did, nonce)
                body = {
                    "payload": json.dumps(payload),
                    "signature": {
                    	"creator": did,
                    	"created": create_time,	
                    	"nonce": nonce,
                    	"signature_value": signature
                    }
                }
                _, resp = tc.issue_colored_token({}, body)
                self.assertEqual(resp["ErrCode"], 0)


    def test_issue_colored_token_err(self):
        """Test issue colored token with error code. """
        mock_do_post = mock.Mock(return_value=Response(401, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response_fail)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                signature = sign(json.dumps(payload), secret_key_b64, did, nonce)
                body = {
                    "payload": json.dumps(payload),
                    "signature": {
                    	"creator": did,
                    	"created": create_time,	
                    	"nonce": nonce,
                    	"signature_value": signature
                    }
                }
                _, resp = tc.issue_colored_token({}, body)
                self.assertEqual(resp["ErrCode"], 107)
    
    def test_issue_colored_token_with_sign_succ(self):
        """Test issue colored token with ed25519 signed body successfully returned"""
        mock_do_post = mock.Mock(return_value=Response(401, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response_succ)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                _, resp = tc.issue_colored_token_with_sign({}, did, create_time, secret_key_b64, payload)
                self.assertEqual(resp["ErrCode"], 0)

    def test_issue_asset_succ(self):
        """Test issue asset successfully returned. """ 
        mock_do_post = mock.Mock(return_value=Response(401, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response_succ)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                signature = sign(json.dumps(payload), secret_key_b64, did, nonce)
                body = {
                    "payload": json.dumps(payload),
                    "signature": {
                    	"creator": did,
                    	"created": create_time,	
                    	"nonce": nonce,
                    	"signature_value": signature
                    }
                }
                _, resp = tc.issue_asset({}, body)
                self.assertEqual(resp["ErrCode"], 0)

    def test_issue_asset_succ_with_sign(self):
        """Test issue asset with ed25519 signed body successfully returned. """ 

        mock_do_post = mock.Mock(return_value=Response(401, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response_succ)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                _, resp = tc.issue_asset_with_sign({}, did, create_time, secret_key_b64, payload)
                self.assertEqual(resp["ErrCode"], 0)

    def test_issue_asset_err(self):
        """Test issue asset with error code. """

        mock_do_post = mock.Mock(return_value=Response(401, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response_fail)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                signature = sign(json.dumps(payload), secret_key_b64, did, nonce)
                body = {
                    "payload": json.dumps(payload),
                    "signature": {
                    	"creator": did,
                    	"created": create_time,	
                    	"nonce": nonce,
                    	"signature_value": signature
                    }
                }
                _, resp = tc.issue_asset({}, body)
                self.assertEqual(resp["ErrCode"], 107)

    def test_withdraw_colored_token_succ(self):
        mock_do_post = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response_succ)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                signature = sign(json.dumps(payload), secret_key_b64, did, nonce)
                body = {
                    "payload": json.dumps(payload),
                    "signature": {
                    	"creator": did,
                    	"created": create_time,	
                    	"nonce": nonce,
                    	"signature_value": signature
                    }
                }
                _, resp = tc.withdraw_colored_token({}, body)
                self.assertEqual(resp["ErrCode"], 0)

    def test_withdraw_colored_token_err(self):
        mock_do_post = mock.Mock(return_value=Response(401, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response_fail)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                signature = sign(json.dumps(payload), secret_key_b64, did, nonce)
                body = {
                    "payload": json.dumps(payload),
                    "signature": {
                    	"creator": did,
                    	"created": create_time,	
                    	"nonce": nonce,
                    	"signature_value": signature
                    }
                }
                _, resp = tc.withdraw_colored_token({}, body)
                self.assertEqual(resp["ErrCode"], 107)

    def test_withdraw_colored_token_with_sign_succ(self):
        """Test withdraw colored token with ed25519 signed body successfully returned. """

        mock_do_post = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response_succ)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                _, resp = tc.withdraw_colored_token_with_sign({}, did, create_time, secret_key_b64, payload)
                self.assertEqual(resp["ErrCode"], 0)

    def test_query_txn_logs_with_endpoint_succ(self):
        mock_do_get = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(return_value=json.dumps(response_succ))

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.get', mock_do_get):
                _, resp = tc.query_txn_logs_with_endpoint({}, "in", "endpoint001")
                self.assertEqual(resp["ErrCode"], 0)

    def test_query_txn_logs_with_endpoint_err(self):
        mock_do_get = mock.Mock(return_value=Response(401, server_cipher))
        mock_run_cmd = mock.Mock(return_value=json.dumps(response_fail))

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.get', mock_do_get):
                _, resp = tc.query_txn_logs_with_endpoint({}, "in", "endpoint001")
                self.assertEqual(resp["ErrCode"], 107)

    def test_query_txn_logs_with_id_succ(self):
        mock_do_get = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(return_value=json.dumps(response_succ))

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.get', mock_do_get):
                _, resp = tc.query_txn_logs_with_id({}, "in", "yourID")
                self.assertEqual(resp["ErrCode"], 0)

    def test_query_txn_logs_with_id_err(self):
        mock_do_get = mock.Mock(return_value=Response(401, server_cipher))
        mock_run_cmd = mock.Mock(return_value=json.dumps(response_fail))

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.get', mock_do_get):
                _, resp = tc.query_txn_logs_with_id({}, "in", "yourID")
                self.assertEqual(resp["ErrCode"], 107)

