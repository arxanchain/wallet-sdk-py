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

import json
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
        print ">>>>>>>>>>>ip: {}".format(self.__client.get_ip())
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

    def create_poe(self, header, creator, created,
            privateB64, payload, nonce=""):
        """Create a POE with ed25519 signed body. """

        payload = json.dumps(payload)
        req_path = "poe/create"
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
                method,
                )

    def update_poe(self, header, creator,
            created, privateB64, payload, nonce=""):
        """Update a POE with ed25519 signed body."""

        payload = json.dumps(payload)
        req_path = "poe/update"
        method = self.__client.do_put
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

    def upload_poe(self, header, file_, poe_id):
        """Upload POE file. """
        req_path = "poe/upload"
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

        header = self.__set_header(header)
        header.update(prepared.headers)
        prepared.headers = header

        return self.__client.do_prepare(prepared)

    def __sign_txs(self, issuer, txs, params):
        print "***************issuer: {}, txs: {}".format(issuer, txs)
        for tx in txs:
            if tx["founder"] != issuer:
                # sign fee by platform private key
                params = self.__client.get_ent_params()
        return self.__sign_tx(tx, params)

    def __sign_tx(self, tx, params):
        if "txout" not in tx:
            raise Exception("'txout' must be set in tx")
        for i in range(len(tx["txout"])):
            if "script" not in tx["txout"][i] or tx["txout"][i]["script"] is None:
                raise Exception("no script field, no need to sign")
            utxo_sig = tx["txout"][i]["script"]
            if utxo_sig["publicKey"] is None:
                continue

            print "**************params: {!r}".format(params)
            sig_body = build_signature_body_base(
                    params["creator"],
                    params["created"],
                    params["nonce"],
                    params["privateB64"],
                    utxo_sig["publicKey"]
            )
            # utxo_sig["signature"] = sig_body["signature_value"]
            utxo_sig["signature"] = [ord(one) for one in sig_body["signature_value"]]
            utxo_sig["nonce"] = sig_body["nonce"]
            utxo_sig["creator"] = sig_body["creator"]
            print "*******************utxo_sig: {}".format(utxo_sig)
            tx["txout"][i]["script"] = json.dumps(utxo_sig)

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

        return time_dur_p+time_dur_t, result

    def process_tx(self, header, txs):
        """ process_tx transfer formally with signature TX. """
        if txs is None or len(txs) <= 0:
            raise Exception("txs should not be empty!")

        req_path = "process"
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
        req_path = "tokens/issue/prepare"
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
        payload = json.loads(result["payload"])

        return time_dur, payload

    def transfer_assets(self, header, payload, params):
        """Transfer assets."""

        # 1 send transfer proposal to get wallet.Tx
        time_dur_p, trans_pre_resp = self.transfer_assets_proposal(
                header,
                payload,
                params
        )
        if "txs" not in trans_pre_resp:
            raise Exception("transfer assets proposal failed: {}".format(trans_pre_resp))
        
        txs = trans_pre_resp["txs"]
        from_ = payload["from"]

        # 2 sign public key as signature
        txs = self.__sign_txs(from_, txs, params)

        # 3 call ProcessTx to transfer formally
        time_dur_t, result = self.process_tx(header, txs)

        return time_dur_p+time_dur_t, result


    def transfer_assets_proposal(self, header, payload, params):
        """ Transfer assets proposal."""
        
        payload = json.dumps(payload)
        req_path = "assets/transfer/prepare"
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
        time_dur_p, trans_pre_resp = self.transfer_ctoken_proposal(
                header,
                payload,
                params
        )
        print "***************time_dur, trans_pre_resp: {}, {}".format(time_dur_p, trans_pre_resp)
        if "txs" not in trans_pre_resp:
            raise Exception("transfer assets proposal failed: {}".format(trans_pre_resp))

        txs = trans_pre_resp["txs"]
        from_ = payload["from"]

        # 2 sign public key as signature
        txs = self.__sign_txs(from_, txs, params)

        # 3 call ProcessTx to transfer formally
        time_dur_t, result = self.process_tx(header, txs)

        return time_dur_p+time_dur_t, result
        

    def transfer_ctoken_proposal(self, header, payload, params):
        """ Transfer ctoken proposal."""
        
        payload = json.dumps(payload)
        req_path = "tokens/transfer/prepare"
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
        if "txs" not in issue_pre_resp:
            raise Exception("issue ctoken proposal failed: {}".format(issue_pre_resp))
        
        txs = issue_pre_resp["txs"]
        issuer = payload["issuer"]

        # 2 sign public key as signature
        txs = self.__sign_txs(issuer, txs, params)

        # 3 call ProcessTx to transfer formally
        time_dur_t, result = self.process_tx(header, txs)
        
        return time_dur_p+time_dur_t, result


    def issue_assets_proposal(self, header, payload, params):
        """ Issue assets proposal."""
        
        payload = json.dumps(payload)
        req_path = "assets/issue/prepare"
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
