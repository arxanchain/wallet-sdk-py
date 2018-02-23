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

from rest.api.api import do_post, do_request, do_put, do_get
from wallet import VERSION, APIKEYHEADER, FABIOROUTETAGHEADER, ROUTETAG

class POEClient(object):
    """A POE clinet."""

    def __init__(self, url, api_key, cert_path):
        """Init POE client with url, api key and crypto lib. """

        self.__route_tag = "wallet-ng"
        self.__path = "poe"
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

    def __set_params(self, header, req_dir, url_params="", body={}):
        header = self.__set_header(header)
        if req_dir:
            request_url = "/".join([
                self.__url,
                VERSION,
                self.__path,
                req_dir
                ])
        else:
            request_url = "/".join([
                self.__url,
                VERSION,
                self.__path,
                ])

        if url_params:
            request_url = "?".join([request_url, url_params])
        req_params = {
            "url": request_url,
            "body": body,
            "headers": header
            }
        return req_params

    def create(self, header, body):
        """Create a POE."""

        req_dir = "create"
        method = do_post
        req_params = self.__set_params(header, req_dir, body=body)
        return do_request(
            req_params,
            self.__api_key,
            self.__cert_path,
            method,
            )

    def update(self, header, body):
        """Update a POE."""

        req_dir = "update"
        method = do_put
        req_params = self.__set_params(header, req_dir, body=body)
        return do_request(
            req_params,
            self.__api_key,
            self.__cert_path,
            method,
            )

    def delete(self, header, body):
        """Delete a POE."""

        req_dir = "delete"
        method = do_put
        req_params = self.__set_params(header, req_dir, body=body)
        return do_request(
            req_params,
            self.__api_key,
            self.__cert_path,
            method,
            )

    def query(self, header, id_):
        """Query a POE."""

        req_dir = "id={}".format(id_)
        method = do_get
        req_params = self.__set_params(header, "", url_params=req_dir)
        return do_request(
            req_params,
            self.__api_key,
            self.__cert_path,
            method,
            )

    def issue(self, header, body):
        """Issue a POE."""

        req_dir = "issue"
        method = do_post
        req_params = self.__set_params(header, req_dir, body=body)
        return do_request(
            req_params,
            self.__api_key,
            self.__cert_path,
            method,
            )

    def withdraw(self, header, body):
        """Withdraw a POE."""

        req_dir = "withdraw"
        method = do_post
        req_params = self.__set_params(header, req_dir, body=body)
        return do_request(
            req_params,
            self.__api_key,
            self.__cert_path,
            method,
            )
