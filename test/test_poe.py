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
    "../"
    )
sys.path.append(ROOT_PATH)
from api.poe import POEClient
from rest.api.api import Client

class Response(object):
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

client_cipher = "client cipher"
IP = "http://127.0.0.1:9143"
APIKEY = "pWEzB4yMM1518346407"
cert_path = "./cert_path"
apikey = "pWEzB4yMM1518346407"


