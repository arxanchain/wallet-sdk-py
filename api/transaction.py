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

import json
from common import VERSION, APIKEYHEADER, \
    FABIOROUTETAGHEADER, ROUTETAG, build_signature_body

class Transaction(object):
    """A transaction client implementation."""

    def __init__(self, client):
        """Init transaction client with Client.
        """

        self.__route_tag = "wallet-ng"
        self.__path = "transaction"
        self.__client = client

    def __set_header(self, header):
        """Set wallet client header"""

        if APIKEYHEADER not in header:
            header[APIKEYHEADER] = self.__client.get_apikey()
        if ROUTETAG not in header:
            header[ROUTETAG] = self.__route_tag
        if FABIOROUTETAGHEADER not in header:
            header[FABIOROUTETAGHEADER] = self.__route_tag

        return header

    def __set_params(self, header, req_path, url_params={}, body={}):
        header = self.__set_header(header)
        if req_path:
            request_url = "/".join([
                    self.__client.get_ip(),
                    VERSION,
                    self.__path,
                    req_path 
                    ])
        else:
            request_url = "/".join([
                    self.__client.get_ip(),
                    VERSION,
                    self.__path,
                    ])

        if url_params:
            params = "&".join("{}={}".format(x, url_params[x]) \
                    for x in url_params)
            request_url = "?".join([request_url, params])

        self.__client.set_url(request_url)
        req_params = {
                "body": body,
                "headers": header
                }
        return req_params

    def transfer_assets(self, header, body):
        """Transfer assets."""

        req_path = "assets/transfer"
        method = self.__client.do_post
        req_params = self.__set_params(
                header,
                req_path,
                body=body
                )
        return self.__client.do_request(
                req_params,
                method
                )

    def transfer_assets_with_sign(self, header, creator,
            created, privateB64, payload, nonce=""):
        """Transfer assets with edd25519 signed body. """

        payload = json.dumps(payload)
        req_path = "assets/transfer"
        method = self.__client.do_post
        signature = build_signature_body(
                creator,
                created,
                nonce,
                privateB64,
                payload
                )
        body = {
                "payload": payload,
                "signature": signature
                }
        req_params = self.__set_params(
                header,
                req_path,
                body=body
                )
        return self.__client.do_request(
                req_params,
                method
                )

    def transfer_colored_tokens(self, header, body):
        """Transfer colored token. """

        req_path= "tokens/transfer"
        method = self.__client.do_post
        req_params = self.__set_params(
                header,
                req_path,
                body=body
                )
        return self.__client.do_request(
                req_params,
                method
                )

    def transfer_colored_tokens_with_sign(self, header, creator,
            created, privateB64, payload, nonce=""):
        """Transfer colored token with ed25519 signed body. """

        payload = json.dumps(payload)
        req_path= "tokens/transfer"
        method = self.__client.do_post
        signature = build_signature_body(
                creator,
                created,
                nonce,
                privateB64,
                payload
                )
        body = {
                "payload": payload,
                "signature": signature
                }
        req_params = self.__set_params(
                header,
                req_path,
                body=body
                )
        return self.__client.do_request(
                req_params,
                method
                )

    def issue_colored_token(self, header, body):
        """Issue colored token. """

        req_path = "tokens/issue"
        method = self.__client.do_post
        req_params = self.__set_params(
                header,
                req_path, 
                body=body
                )
        return self.__client.do_request(
                req_params,
                method
                )

    def issue_colored_token_with_sign(self, header, creator,
            created, privateB64, payload, nonce=""):
        """Issue colored token with sign. """

        payload = json.dumps(payload)
        req_path = "tokens/issue"
        method = self.__client.do_post
        signature = build_signature_body(
                creator,
                created,
                nonce,
                privateB64,
                payload
                )
        body = {
                "payload": payload,
                "signature": signature
                }
        req_params = self.__set_params(
                header,
                req_path, 
                body=body
                )
        return self.__client.do_request(
                req_params,
                method
                )

    def issue_asset(self, header, body):
        """Issue asset. """

        req_path= "assets/issue"
        method = self.__client.do_post
        req_params = self.__set_params(
                header,
                req_path, 
                body=body
                )
        return self.__client.do_request(
                req_params,
                method
                )

    def issue_asset_with_sign(self, header, creator,
            created, privateB64, payload, nonce=""):
        """Issue asset with ed25519 signed body. """

        payload = json.dumps(payload)
        req_path= "assets/issue"
        method = self.__client.do_post
        signature = build_signature_body(
                creator,
                created,
                nonce,
                privateB64,
                payload
                )
        body = {
                "payload": payload,
                "signature": signature
                }
        req_params = self.__set_params(
                header,
                req_path,
                body=body
                )
        return self.__client.do_request(
                req_params,
                method
                )

    def withdraw_colored_token(self, header, body):
        """Withdraw colored token. """

        req_path = "tokens/withdraw"
        method = self.__client.do_post
        req_params = self.__set_params(
                header,
                req_path, 
                body=body
                )
        return self.__client.do_request(
                req_params,
                method
                )

    def withdraw_colored_token_with_sign(self, header, creator,
            created, privateB64, payload, nonce=""):
        """Withdraw colored token with ed25519 signed body. """

        payload = json.dumps(payload)
        req_path = "tokens/withdraw"
        method = self.__client.do_post
        signature = build_signature_body(
                creator,
                created,
                nonce,
                privateB64,
                payload
                )
        body = {
                "payload": payload,
                "signature": signature
                }
        req_params = self.__set_params(
                header,
                req_path,
                body=body
                )
        return self.__client.do_request(
                req_params,
                method
                )

    def query_txn_logs_with_endpoint(self, header, type_, endpoint):
        """Query transactions logs. """

        req_path = "logs"
        method = self.__client.do_get
        params = {
                "type": type_,
                "endpoin": endpoint
                }

        req_params = self.__set_params(
            header,
            req_path, 
            params
            )
        return self.__client.do_request(
            req_params,
            method
            )

    def query_txn_logs_with_id(self, header, type_, id_):
        """Query transactions logs with param id. """

        req_path = "logs"
        method = self.__client.do_get
        params = {
                "type": type_,
                "id": id_
                }

        req_params = self.__set_params(
            header,
            req_path, 
            params
            )
        return self.__client.do_request(
            req_params,
            method
            )
