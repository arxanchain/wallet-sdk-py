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
import requests
from rest.api.api import do_post, do_request, \
        do_put, do_get, do_prepare
from common import VERSION, APIKEYHEADER, \
        FABIOROUTETAGHEADER, ROUTETAG, build_signature_body

class POEClient(object):
    """A POE client."""

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

    def __set_url(self, req_path, url_params={}):
        request_url = ""
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
        return request_url

    def __set_params(self, header, req_path, url_params={}, body={}):
        header = self.__set_header(header)
        request_url = self.__set_url(req_path, url_params)

        req_params = {
                "url": request_url,
                "body": body,
                "headers": header
                }
        return req_params

    def create(self, header, body):
        """Create a POE."""

        req_path= "create"
        method = do_post
        req_params = self.__set_params(
                header,
                req_path, 
                body=body
                )
        return do_request(
                req_params,
                self.__api_key,
                self.__cert_path,
                method,
                )

    def create_with_sign(self, header, creator, created,
            privateB64, payload, nonce=""):
        """Create a POE with ed25519 signed body. """

        payload = json.dumps(payload)
        req_path = "create"
        method = do_post
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
        return do_request(
                req_params,
                self.__api_key,
                self.__cert_path,
                method,
                )

    def update(self, header, body):
        """Update a POE."""

        req_path = "update"
        method = do_put
        req_params = self.__set_params(
                header,
                req_path,
                body=body
                )
        return do_request(
                req_params,
                self.__api_key,
                self.__cert_path,
                method,
                )

    def update_with_sign(self, header, creator,
            created, privateB64, payload, nonce=""):
        """Update a POE with ed25519 signed body."""

        payload = json.dumps(payload)
        req_path = "update"
        method = do_put
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
        return do_request(
                req_params,
                self.__api_key,
                self.__cert_path,
                method,
                )

    def query(self, header, id_):
        """Query a POE."""

        params= {"id": id_}
        method = do_get
        req_params = self.__set_params(
                header,
                "",
                url_params=params
                )
        return do_request(
                req_params,
                self.__api_key,
                self.__cert_path,
                method,
                )

    def upload(self, header, file_, poe_id):
        """Upload POE file. """
        req_path = "upload"
        poefile = "application/octet-stream"
        poeid_filepart = (
                '',
                poe_id,
                )

        filepart = (
                file_,
                open(file_, 'rb'),
                poefile
                )
        files = {
                "poe_id": poeid_filepart,
                "poe_file": filepart
                }

        req_url = self.__set_url(req_path)
        prepared = requests.Request(
                "POST",
                url=req_url,
                files=files
                ).prepare()
        body = prepared.body
        header = self.__set_header(header)
        header.update(prepared.headers)
        prepared.headers = header

        return do_prepare(
                prepared,
                self.__api_key,
                self.__cert_path,
                )

