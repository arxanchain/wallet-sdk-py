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

from rest.api.api import do_post, do_put, \
    do_get, do_request
from common import VERSION, APIKEYHEADER, \
    FABIOROUTETAGHEADER, ROUTETAG

class WalletClient(object):
    """A wallet client implementation."""

    def __init__(self, url, api_key, cert_path):
        """Init wallet client with url, api key and crypto lib. """

        self.__route_tag = "wallet-ng"
        self.__path = "wallet"
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

    def __set_params(self, header, req_path, url_params={}, body={}):
        header = self.__set_header(header)
        if req_path:
            request_url = "/".join([
                self.__url,
                VERSION,
                self.__path,
                req_path
                ])
        else:
            request_url = "/".join([
                self.__url,
                VERSION,
                self.__path,
                ])

        if url_params:
            params = "&".join("{}={}".format(x, url_params[x]) \
                for x in url_params)
            request_url = "?".join([request_url, params])
        req_params = {
            "url": request_url,
            "body": body,
            "headers": header
            }
        return req_params

    def register(self, header, body):
        """Register user wallet."""
        req_dir = "register"
        method = do_post

        req_params = self.__set_params(
            header,
            req_dir,
            body=body
            )
        return do_request(
            req_params,
            self.__api_key,
            self.__cert_path,
            method,
            )

    def register_sub_wallet(self, header, body):
        """Register a sub wallet."""
        req_dir = "register/subwallet"
        method = do_post

        req_params = self.__set_params(
            header,
            req_dir,
            body=body
            )
        return do_request(
            req_params,
            self.__api_key,
            self.__cert_path,
            method,
            )

    def update_password(self, header, body):
        """Update wallet password."""

        req_dir = "password"
        method = do_put
        req_params = self.__set_params(
            header,
            req_dir,
            body=body
            )
        return do_request(
            req_params,
            self.__api_key,
            self.__cert_path,
            method,
            )

    def create_payment_password(self, header, body):
        """Create wallet payment password."""

        req_dir = "payment_passwd"
        method = do_post
        req_params = self.__set_params(
            header,
            req_dir,
            body=body
            )
        return do_request(
            req_params,
            self.__api_key,
            self.__cert_path,
            method,
            )

    def update_payment_password(self, header, body):
        """Update payment password."""

        req_dir = "payment_passwd"
        method = do_put
        req_params = self.__set_params(
            header,
            req_dir,
            body=body
            )
        return do_request(
            req_params,
            self.__api_key,
            self.__cert_path,
            method,
            )

    def query_wallet_infos(self, header, id_):
        """Query wallet infos."""

        req_dir = "info"
        req_dir = "?".join([req_dir, "id={}".format(id_)])
        method = do_get
        req_params = self.__set_params(header, req_dir)
        return do_request(
            req_params,
            self.__api_key,
            self.__cert_path,
            method,
            )

    def query_wallet_balance(self, header, id_):
        """Query wallet balalce"""

        req_dir = "balance"
        req_dir = "?".join([req_dir, "id={}".format(id_)])
        params = {"id": id_}
        method = do_get
        req_params = self.__set_params(
            header,
            url_params=params,
            req_path=req_dir
            )
        return do_request(
            req_params,
            self.__api_key,
            self.__cert_path,
            method,
            )
