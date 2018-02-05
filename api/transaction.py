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

from rest.api.api import do_post, do_request
from wallet import VERSION, APIKEYHEADER, FABIOROUTETAGHEADER, ROUTETAG

class Transaction(object):
    """A transaction client implementation."""

    def __init__(self, url, api_key, cert_path):
        """Init transaction client with url, api_key, signing_key.

        :param url: request url
        :param apikey: api key generated from server
        :param nonce: nonce
        :param did: did
        """

        self.__route_tag = "wallet-ng"
        self.__path = "transaction"
        self.__url = url
        self.__api_key = api_key
        self.__cert_path = cert_path

    def __set_header(self, header):
        """Set wallet client header"""

        if APIKEYHEADER not in header:
            header[APIKEYHEADER] = self.__api_key
        if ROUTETAG not in header:
            header[ROUTETAG] = self.__route_tag
        if FABIOROUTETAGHEADER not in header:
            header[FABIOROUTETAGHEADER] = self.__route_tag

        return header

    def __set_params(self, header, body, req_dir):
        header = self.__set_header(header)
        request_url = "/".join([
            self.__url,
            VERSION,
            self.__path,
            req_dir
            ])
        req_params = {
            "url": request_url,
            "body": body,
            "headers": header
            }
        return req_params

    def transfer_assets(self, header, body):
        """Transfer assets."""

        req_dir = "assets/transfer"
        method = do_post
        req_params = self.__set_params(header, body, req_dir)
        return do_request(
            req_params,
            self.__api_key,
            self.__cert_path,
            method)

    def transfer_colored_tokens(self, header, body):
        """Transfer colored token. """

        req_dir = "tokens/transfer"
        method = do_post
        req_params = self.__set_params(header, body, req_dir)
        return do_request(
            req_params,
            self.__api_key,
            self.__cert_path,
            method)
