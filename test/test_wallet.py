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
from rest.api.api import require_ok
ROOT_PATH = os.path.join(os.path.dirname(__file__),
        "..")
IMPORT_PATH = os.path.join(ROOT_PATH,
        "api")
sys.path.append(IMPORT_PATH)
from wallet import WalletClient

class WalletTest(unittest.TestCase):
    """Wallet test. """
    def setUp(self):
        pass
    
    def test_register_succ(self):
        """ Test register successfully returned. """
        wc = WalletClient("http://127.0.0.1:9143", "alice", "")
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
	resp = {
	    "Method": "",
	    "ErrCode": 0,
	    "ErrMessage": "",
	    "Payload":{
		"id": "did:axn:8uQhQMGzWxR8vw5P3UWH1j",
		"endpoint": "xxxxx",
		"key_pair": {
		    "private_key": "cHJpdmF0ZSBrZXk=",
		    "public_key": "cHVibGljIGtleQ=="
		},
		"created": "xxxx"
	}
	}
        succ_sender = mock.Mock(return_value=(0.01, resp))
        wc.register = succ_sender
        _, resp = wc.register({}, body)
        self.assertEqual(resp["ErrCode"], 0)

    def test_register_sub(self):
        pass
    
    def test_update_password(self):
        pass

    def test_create_payment_password(self):
        pass

    def test_update_payment_password(self):
        pass

    def test_query_wallet_infos(self):
        pass

    def test_query_wallet_balance(self):
        pass
