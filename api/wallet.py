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

import base64
import json
import collections
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from rest.api.common import APIKEYHEADER, FABIOROUTETAGHEADER, ROUTETAG, \
        build_signature_body, build_signature_body_base
from common import VERSION

class WalletClient(object):
    """A wallet client implementation."""

    def __init__(self, client):
        """Init wallet client with Client. """

        self.__route_tag = "wallet-ng"
        # self.__path = "wallet"
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

    def __set_url(self, req_path, url_params={}):
        request_url = ""
        if req_path:
            request_url = "/".join([
                    self.__client.get_ip(),
                    VERSION,
                    # self.__path,
                    req_path
                    ])
        else:
            request_url = "/".join([
                    self.__client.get_ip(),
                    VERSION
                    # self.__path,
                    ])
        if url_params:
            params = "&".join("{}={}".format(x, url_params[x]) \
                for x in url_params)
            request_url = "?".join([request_url, params])

        # self.__client.set_url(request_url)

        return request_url

    def __set_params(self, header, req_path, url_params={}, body={}):
        header = self.__set_header(header)
        request_url = self.__set_url(req_path, url_params)

        # self.__client.set_url(request_url)
        req_params = {
                "url": request_url,
                "body": body,
                "headers": header
                }
        return req_params

    def register(self, header, body):
        """Register user wallet."""
        req_dir = "wallet/register"
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
        req_dir = "wallet/register/subwallet"
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

        req_dir = "wallet/password"
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

        req_dir = "wallet/payment_passwd"
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

        req_dir = "wallet/payment_passwd"
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

        req_dir = "wallet/info"
        req_dir = "?".join([req_dir, "id={}".format(id_)])
        method = self.__client.do_get
        req_params = self.__set_params(header, req_dir)
        return self.__client.do_request(
                req_params,
                method,
                )

    def query_wallet_balance(self, header, id_):
        """Query wallet balalce"""

        req_dir = "wallet/balance"
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

    def create_poe(self, header, payload, params):
        """Create a POE with ed25519 signed body. """

        payload = json.dumps(payload)
        req_path = "poe/create"
        method = self.__client.do_post
        params["payload"] = payload
        signature = build_signature_body(**params)
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
                method,
                )

    def update_poe(self, header, payload, params):
        """Update a POE with ed25519 signed body."""

        payload = json.dumps(payload)
        req_path = "poe/update"
        method = self.__client.do_put
        params["payload"] = payload
        signature = build_signature_body(**params)
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
                method,
                )

    def query_poe(self, header, id_):
        """Query a POE."""

        params= {"id": id_}
        req_path="poe"
        method = self.__client.do_get
        req_params = self.__set_params(
                header,
                req_path,
                url_params=params
                )
        return self.__client.do_request(
                req_params,
                method,
                )

    def upload_poe(self, header, file_, poe_id, readonly):
        """Upload POE file. """
        req_path = "poe/upload"
        poefile = "application/octet-stream"
        filepart = (
                file_,
                open(file_, 'rb'),
                poefile
                )
        files = {
                "poe_file" : filepart
        }
        data = {
                "poe_id": poe_id,
                "read_only": readonly
        }

        req_url = self.__set_url(req_path)
        prepared = requests.Request(
                "POST",
                url=req_url,
                files=files,
                data=data
                ).prepare()

        header = self.__set_header(header)
        header.update(prepared.headers)
        prepared.headers = header

        return self.__client.do_prepare(prepared)

    def __sign_txs(self, issuer, txs, params):
        for i, tx in enumerate(txs):
            if tx["founder"] != issuer:
                # sign fee by platform private key
                params = self.__client.get_ent_params()
            txs[i] = self.__sign_tx(tx, params)
        return txs

    def __sign_tx(self, tx, params):
        if "txout" not in tx:
            raise Exception("'txout' must be set in tx")
        for i in range(len(tx["txout"])):
            if "script" not in tx["txout"][i] or tx["txout"][i]["script"] is None:
                raise Exception("no script field, no need to sign")

            utxo_sig = json.loads(base64.b64decode(tx["txout"][i]["script"]))
            if utxo_sig["publicKey"] is None:
                continue

            public_key = base64.b64decode(utxo_sig["publicKey"])
            sig_body = build_signature_body_base(
                    params["creator"],
                    params["created"],
                    params["nonce"],
                    params["privateB64"],
                    public_key
                    
            )
            utxo_sig["signature"] = base64.b64encode(sig_body["signature_value"])
            utxo_sig["nonce"] = params["nonce"]
            utxo_sig["creator"] = params["creator"]
            b64_utxo_sig = json.dumps(utxo_sig)
            tx["txout"][i]["script"] = base64.b64encode(b64_utxo_sig)

        return tx


    def issue_colored_token(self, header, payload, params):
        """Issue colored token with sign. """

        # 1 send transfer proposal to get wallet.Tx
        time_dur_p, issue_pre_resp = self.issue_ctoken_proposal(
                header,
                payload,
                params
        )
        if "txs" not in issue_pre_resp:
            raise Exception("issue ctoken proposal failed: {}".format(issue_pre_resp))
        
        txs = issue_pre_resp["txs"]
        issuer = payload["issuer"]

        # 2 sign public key as signature
        txs = self.__sign_txs(issuer, txs, params)

        # 3 call ProcessTx to transfer formally
        time_dur_t, result = self.process_tx(header, txs)
        payload = json.loads(result["Payload"])
        payload["token_id"] = issue_pre_resp["token_id"]
        result["Payload"] = json.dumps(payload)

        return time_dur_p+time_dur_t, result

    def process_tx(self, header, txs):
        """ process_tx transfer formally with signature TX. """
        if txs is None or len(txs) <= 0:
            raise Exception("txs should not be empty!")

        req_path = "transaction/process"
        body = {"txs": txs}
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


    def issue_ctoken_proposal(self, header, payload, params):
        """ Issue ctoken proposal."""
        
        payload = json.dumps(payload)
        req_path = "transaction/tokens/issue/prepare"
        method = self.__client.do_post
        params["payload"] = payload
        signature = build_signature_body(**params)
        body = {
                "payload": payload,
                "signature": signature
                }
        req_params = self.__set_params(
                header,
                req_path,
                body=body
                )
        time_dur, result = self.__client.do_request(
                req_params,
                method
                )
        payload = json.loads(result["Payload"])

        return time_dur, payload

    def transfer_assets(self, header, payload, params):
        """Transfer assets."""

        # 1 send transfer proposal to get wallet.Tx
        time_dur_p, trans_pre_resp = self.transfer_assets_proposal(
                header,
                payload,
                params
        )

        from_ = payload["from"]

        # 2 sign public key as signature
        txs = self.__sign_txs(from_, trans_pre_resp, params)

        # 3 call ProcessTx to transfer formally
        time_dur_t, result = self.process_tx(header, txs)

        return time_dur_p+time_dur_t, result


    def transfer_assets_proposal(self, header, payload, params):
        """ Transfer assets proposal."""
        
        payload = json.dumps(payload)
        req_path = "transaction/assets/transfer/prepare"
        method = self.__client.do_post
        params["payload"] = payload
        signature = build_signature_body(**params)
        body = {
                "payload": payload,
                "signature": signature
                }
        req_params = self.__set_params(
                header,
                req_path,
                body=body
                )
        time_dur, result = self.__client.do_request(
                req_params,
                method
                )
        payload = json.loads(result["Payload"])

        return time_dur, payload


    def transfer_colored_tokens(self, header, payload, params):
        """Transfer colored token. """

        # 1 send transfer proposal to get wallet.Tx
        time_dur_p, txs = self.transfer_ctoken_proposal(
                header,
                payload,
                params
        )
        from_ = payload["from"]

        # 2 sign public key as signature
        txs = self.__sign_txs(from_, txs, params)

        # 3 call ProcessTx to transfer formally
        time_dur_t, result = self.process_tx(header, txs)

        return time_dur_p+time_dur_t, result
        

    def transfer_ctoken_proposal(self, header, payload, params):
        """ Transfer ctoken proposal."""
        
        payload = json.dumps(payload)
        req_path = "transaction/tokens/transfer/prepare"
        method = self.__client.do_post
        params["payload"] = payload
        signature = build_signature_body(**params)
        body = {
                "payload": payload,
                "signature": signature
                }
        req_params = self.__set_params(
                header,
                req_path,
                body=body
                )
        time_dur, result = self.__client.do_request(
                req_params,
                method
                )
        payload = json.loads(result["Payload"])

        return time_dur, payload


    def issue_asset(self, header, payload, params):
        """Issue asset. """

         # 1 send transfer proposal to get wallet.Tx
        time_dur_p, issue_pre_resp = self.issue_assets_proposal(
                header,
                payload,
                params
        )
        issuer = payload["issuer"]

        # 2 sign public key as signature
        txs = self.__sign_txs(issuer, issue_pre_resp, params)

        # 3 call ProcessTx to transfer formally
        time_dur_t, result = self.process_tx(header, txs)
        
        return time_dur_p+time_dur_t, result


    def issue_assets_proposal(self, header, payload, params):
        """ Issue assets proposal."""
        
        payload = json.dumps(payload)
        req_path = "transaction/assets/issue/prepare"
        method = self.__client.do_post
        params["payload"] = payload
        signature = build_signature_body(**params)
        body = {
                "payload": payload,
                "signature": signature
                }
        req_params = self.__set_params(
                header,
                req_path,
                body=body
                )
        time_dur, result = self.__client.do_request(
                req_params,
                method
                )
        payload = json.loads(result["Payload"])
        return time_dur, payload


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

    def set_index(self, header, id_, indexs):
        """Set the index for did """
        req_path = "index/set"
        method = self.__client.do_post
        body = {
            "id": id_,
            "indexs": indexs
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

    def get_index(self, header, indexs):
        """Get the did by index"""
        req_path = "index/get"
        method = self.__client.do_post
        body = {
            "indexs": indexs
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