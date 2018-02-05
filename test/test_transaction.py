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
from rest.api.api import require_ok
import cryption
print help(cryption)
from cryption.crypto import sign
ROOT_PATH = os.path.join(os.path.dirname(__file__),
        "..")
IMPORT_PATH = os.path.join(ROOT_PATH,
        "api")
sys.path.append(IMPORT_PATH)
from transaction import Transaction

class TransactionTest(unittest.TestCase):
    """Transaction test. """
    def setUp(self):
        pass

    def test_transfer_asset(self):
        url = "http://172.16.13.2:9143"
        apikey = "alice"
        secret_key_b64 = "0lxEFzMQhn68vY2F0f+nOwP7kl5zjahjPcfyMAJVmzn0HNQssIIYh+c2CgCKEHeUvxqCu6W/sJKqKt2DLJnKpw=="
        nonce = "nonce"
        did = "did:ara:8uQhQMGzWxR8vw5P3UWH1j"
        cert_path = "./cert_path"
        create_time = "1517818060"
        payload = {
            "from": did,
            "to": "did:axn:21tDAKCERh95uGgKbJNHYp",
            "asset_id": "1f38a7a1-2c79-465e-a4c0-0038e25c7edg",
            "coins": [
            	{
            	    "coin_id": "1f38a7a1-2c79-465e-a4c0-0038e25c7edg",
            	    "amount": 5
            	}
            ],
            "fees": {
            	"accounts": [
            	    did
            	],
            	"coins": [
            	    {
            	    	"coin_id": "1f38a7a1-2c79-465e-a4c0-0038e25c7edg",
            	    	"amount": 5
            	    }
            	]
            }
        }

        tc = Transaction(url, apikey, cert_path)
        signature = sign(json.dumps(payload), secret_key_b64, did, nonce)
        body = {
            "payload": json.dumps(payload),
            "signature": {
            	"creator": did,
            	"created": create_time,	
            	"nonce": nonce,
            	"signatureValue": signature
            }
        }

        resp = {
	    "Method": "",
	    "ErrCode": 0,
	    "ErrMessage": "",
	    "Payload":{
	    	"transaction_ids": [
	    	    "xx-xxx-xxx"
	    	]
	    }
	}


        succ_sender = mock.Mock(return_value=(0.01, resp))
        tc.transfer_assets = succ_sender
        _, resp = tc.transfer_assets({}, body)
        self.assertEqual(resp["ErrCode"], 0)

    def test_transfer_colored_tokens(self):
        pass
