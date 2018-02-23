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
from api.wallet import WalletClient
import httpretty

class WalletTest(unittest.TestCase):
    """Wallet test. """
    def setUp(self):
        pass

    def test_register_succ(self):
        """ Test register successfully returned. """
        ## response:
        ## {
        ##     "ErrCode": 0,
        ##     "ErrMessage": "",
        ##     "Method": "",
        ##     "Payload": "{\"code\":0,\"message\":\"\",\"id\":\"did:axn:84161949-9184-409f-996b-e72e6f722e50\",\"endpoint\":\"9a8db40dbc5e9fcf08796e757d50b6bf59adf0590c6a6529789e518fd9e2053f\",\"key_pair\":{\"private_key\":\"nySv70wbzRts1Tl9eou24I8ug8zBH0GfekqGF8EfOyA925gEDULoVJbMZHw0pIp18OFlG+m4Oa16yaZa1xvSCg==\",\"public_key\":\"PduYBA1C6FSWzGR8NKSKdfDhZRvpuDmtesmmWtcb0go=\"},\"created\":1519726473,\"coin_id\":\"\",\"transaction_ids\":[\"01ee2d3a69d11d0f14f7f289d787240be689086ab7527a81045b61d864c55717\",\"d99dcad2f0e14cdb47f5f80a4a0df6b18aacaf266f5802fabdd5178afd3b9887\",\"eb9eded92d59e22065e41ac7a69b711718f158fb1c7094535678725ec9a28c14\"]}"
        ## } 
	resp = "BNpIn3NMn5u3OOKFXKbRTaf/G2uvVKzAz0WyG6k7u8iyJ7DWGngWSDoXYAiuxx42E27ODBuybtEsk15UnZThiJU3L++3te0AbkUfot9cv6I5MdQbu4wFkTOA02V956ZrGCUmwe8XAWbuyBJMuzBCKEE5HeLbk+VLfSeF6mx1eQgXk0E4+/TNvs5VgxAFYI/J873vcirPU09t3Z2LRpMaFbZlFwCrQL1sGwD1fgbwuv2GuvycOzt7VG8PDaohfCE/r89ah/fxqeWh5tojdaeD2yYoDdyRfMeMJuuinPUQQ5BDd3xfkSTdj1pAt/46LEd4bysIujhjDDoJ3AeAObR85lfAIN1nWKNSt0yNUF5Dagk5g6BcqBhyEgTjiTl5bB1XNz6tZ39fxteZpwiz0SIetvLwYdTDcGCooze/qPCuvVDBqhlJAwkZPSEFEdTbn+PheK5H3+BeW3gGE8uO6+DDlwWRN6s2179B17dVD34bjvP3GAhv0XxF/KtDcitHZgOV6+kGQ10HOtXFD7Z8PFoe0rbvg3mQQUfvJ/UW1PVNQSs3uj4d4qHIlkOWjBOFcR6chI6pxq8880MV6YCSbb+k1JhYpkXSirH9yeMznnuOmXtctDLESxEOWv3U5V9qvdiegyk5U7qwwx7g7nqQu/Uze/3W4uWOkhf8t9VhHzbU2+NplZUQ49caNkSpGtk5GDWa0sIpzKeTLq6zjEEcclbbw1OjuOHukXUfnRSrAubM11Zkf8fdCMH6q9U+zM9y+RLh3B4wpvHsITW0uPa2LwJlspV0VDpqrbDDeYS+M/lANl9nTHykGTl0DWR/N+JVNXjKaQyDjkuktBT/cTxPz8nKj5gbyfo4Dgv4kV3Iyw3OYEq+PzxSS/3C+4uLzsVxgEzjd+nlG7YolVq89MCOIkKA0f/CTBFXjxtglNwQeC2mwY8RqbTh26hiMWElgeDDu3ZKoMBhb+RKM+fuOvkFYrWbBk4VUeEjcXs7paC5b6mGZk6A6Xt7yqOx8+Sc+9+p8j26gFqACYodPcZNxdnjH02IELlaA5WtOl/vGkckf7IMlpMREnDHrgotgskzjAdirA44H93EUw8Jt81nGqQw0Yf+W4RZk4CMFl9Mvdk/A4CN0rXGqK3yXaEJu3O5vmRzOccc1zgS7A3VteDly7Cq+3OqjxmlhLs4U92z/rf9H19S3gVBJ+zsIsZzLZ3sOYp9fzDdMmBrFty79HjUmddh2WT2oKJYlCPqfnyKy8+bNSWc+H8htBTA3aitW5opopfAjc+Fn6uXYv+nvhK58orJWDAaiUvmoSyCOzVCJV3Ka5vbMeg26gdNKjDCEwIC8XtJrMaOljB+kpZ267Inwl0IkWi8e9r0p2la+Qk/LdFtBFqCfxz+f0NBjS/d5u5k/WFt5IuihDsYHSS6Pl64qZIGgcPlWBmCFe89WDqB8PfGB6NIkuBQiOXJgAINMViOjLsxAQ5rm7i2Btx/CESvSi5r70eu8c5NNuA1+Lvl1s0c4yiGJOzEz3Q="
        httpretty.enable()
        httpretty.register_uri(
            httpretty.POST,
            "http://127.0.0.1:9143/v1/wallet/register",
            body=resp
            )
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
        httpretty.disable()
        httpretty.reset()

    def test_register_sub(self):
        """ Test register sub wallet successfully returned. """
        ## response:
        ## {
        ##     "ErrCode": 0,
        ##     "ErrMessage": "",
        ##     "Method": "",
        ##     "Payload": "{\"code\":0,\"message\":\"\",\"id\":\"did:axn:769de30d-2170-453d-81ce-b8f566be1e7a#Organization\",\"endpoint\":\"d9f0f47af158609ef97399a7c38cf7885a0c32da5b4145706361ff6c7a3520e3\",\"key_pair\":{\"private_key\":\"QU9T6vN3g4q3MLAUL8YJxK90bBWvOw+QW4zONXSR1acNCG8tblPVcK/jzKFA/QRyQ+4lv3KN5JfMJRzek05NNw==\",\"public_key\":\"DQhvLW5T1XCv48yhQP0EckPuJb9yjeSXzCUc3pNOTTc=\"},\"created\":1519702836,\"coin_id\":\"\",\"transaction_ids\":[\"1e0edec693c1a22656d5db23d66b91ab9df0dcefef025dd293228e324fc8de4c\",\"bf6e2be1ab2fb0b66be2ee67732c885853524416e4904b6124cc9c5d2b1736d0\"]}"
        ## }
        resp = "BLAA7vB31SPsbQf18zb3Y80NeHfLQk00QZmLKU2T0r/z45xPKelbqvM9C15hKLWaJwlNSLdmjwnVhSeaaYWG/ao80rRHAvEA9nkw1WdOcfC0fAwF4NdHMwz2wuAw+QL5IYAmHOu2fXoiubF6Ay1Hdw0oN6W+RNa+1zFHD9SVdengCT5V7q0mcgUXbmd4YsKHfGG5Pyd17D38E6OIDdUy6skVk2xNSRKehmQ1AS4g2+nMbJS+XvPZzm26WCzT+0zhec7wE8yqzpXR9F45rHZaz5WYcxCTddyPJ31K+wrc7X/Y4UHhjuBuVeU5QJQagoJNuYqeWS3luwN+TVZpBI8sByXc5C+M0vNdJPiiuzD4DUrqusqbso6+J7L4YVF6rgg97q7iuUKQvnmQzsktrdofugbKm6xxdfqp2oiLOmCWf43K+05/wxv1d9iMyBBDy37OGHkwkSzXDtf9sRysW9lKb9rk+9PGdnDnQvmIUBlUYGLue0LcYxqc3dZIAvCvWFrK3FmvV3K6+3reAHx5+Ym7yuQPu721llgaJkhoVdnUJpBCZhxj4oe/t249WnI3t565e6AsFB13IrFaRQd62b+HTAYKHmIRg7aV9VbZHWUEg212R0UWPm5g2ghZ1AcIDBx2zDXDSPSonweNS3OWCEQ+KRTCyo2E3U8Fi0Ob2WIr6WKUiwPubKm101rWfTxKNqqT6uEVW0eVW1syfz8mHztnyZcHU8cfZ7xXNCr38IRpw6+1iUlOCDeWQYn8F5xchmRJ7A8LDf9OTmxZZ+tdj4jjLDBm1K+iI83/QqYk4tVCYBxYrwtb6uWqldaBjRP+5MXuIdkA785nB5kRuzwhF1jxdZJoDIIWDQH+1t1tZN3Z3WCACRRwVGnnK5UgZOrp7Qs/+FNh4C64yiG7X+R+BmbfM1N0frbQb/qK9d1HTi2pAVeGJ49c15EzeVJUuEdRgDUyNRtwYTxioVAZrBOcis2EbcOg2vzzHmUHYE87N08Fm1zrm0dRauTKaghvN+6+uRgj6UF26tl4xsxE2PUQ5OIiVWSTbT8zWSuq9QIVpuEGDh2k42adGXFaz4En36e/OXUPgv1fMDpgDwQFq3KOoIl/U5ZIsyv+tIKNM8998MQpXrDbGoq6yKpt0dGPxC2sc+eeXqXhV0gumB0EhPBzOdJhfdqhn8uCMqS3khcbNkERk5FI+Yw9FDcLVSVfESMdAeZBTT27fDb/QpByQzNm2s6fC7WxKATBZbH+Y0vohxSv1RqXBsQRj8roHiQ+aarEk4R5aTDU2sPvLb3jzAFyPqvnM6hZChQ5i3gS50A1yvAPEwKzEB4vdzUtst1ADpCEpPoF24bgpeYtMELhXBqxgJJl7pPEy+UaDNVlJLXAwszVbhZoyAVVAAL+dxJajJ6N/E3VQKSwMet3DO4myBg="
        httpretty.enable()
        httpretty.register_uri(
            httpretty.POST,
            "http://127.0.0.1:9143/v1/wallet/register/subwallet",
            body=resp
            )
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
        httpretty.disable()
        httpretty.reset()

    def test_update_password(self):
        """ Test update password successfully returned. """
        pass

    def test_create_payment_password(self):
        pass

    def test_update_payment_password(self):
        pass

    def test_query_wallet_infos(self):
        pass

    def test_query_wallet_balance(self):
        pass
