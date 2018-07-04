# -*- coding: utf-8 -*-

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

from rest.api.common import APIKEYHEADER, FABIOROUTETAGHEADER, ROUTETAG
from common import VERSION

class WalletClient(object):
    """A wallet client implementation."""

    def __init__(self, client):
        """Init wallet client with Client. """

        self.__route_tag = "wallet-ng"
        self.__path = "wallet"
        self.__client= client 

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

        # self.__client.set_url(request_url)
        req_params = {
                "url": request_url,
                "body": body,
                "headers": header
                }
        return req_params

    def register(self, header, body):
        """Register user wallet."""
        req_dir = "register"
        method = self.__client.do_post

        req_params = self.__set_params(
                header,
                req_dir,
                body=body
                )
        return self.__client.do_request(
                req_params,
                method,
                )

    def register_sub_wallet(self, header, body):
        """Register a sub wallet."""
        req_dir = "register/subwallet"
        method = self.__client.do_post

        req_params = self.__set_params(
                header,
                req_dir,
                body=body
                )
        return self.__client.do_request(
                req_params,
                method,
                )

    def update_password(self, header, body):
        """Update wallet password."""

        req_dir = "password"
        method = self.__client.do_put
        req_params = self.__set_params(
                header,
                req_dir,
                body=body
                )
        return self.__client.do_request(
                req_params,
                method,
                )

    def create_payment_password(self, header, body):
        """Create wallet payment password."""

        req_dir = "payment_passwd"
        method = self.__client.do_post
        req_params = self.__set_params(
                header,
                req_dir,
                body=body
                )
        return self.__client.do_request(
                req_params,
                method,
                )

    def update_payment_password(self, header, body):
        """Update payment password."""

        req_dir = "payment_passwd"
        method = self.__client.do_put
        req_params = self.__set_params(
                header,
                req_dir,
                body=body
                )
        return self.__client.do_request(
                req_params,
                method,
                )

    def query_wallet_infos(self, header, id_):
        """Query wallet infos."""

        req_dir = "info"
        req_dir = "?".join([req_dir, "id={}".format(id_)])
        method = self.__client.do_get
        req_params = self.__set_params(header, req_dir)
        return self.__client.do_request(
                req_params,
                method,
                )

    def query_wallet_balance(self, header, id_):
        """Query wallet balalce"""

        req_dir = "balance"
        params = {"id": id_}
        method = self.__client.do_get
        req_params = self.__set_params(
                header,
                url_params=params,
                req_path=req_dir
                )
        return self.__client.do_request(
                req_params,
                method,
                )
