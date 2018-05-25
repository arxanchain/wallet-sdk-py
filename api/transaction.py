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
from rest.api.common import APIKEYHEADER, FABIOROUTETAGHEADER, \
        ROUTETAG, build_signature_body, build_signature_body_base
from common import VERSION

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

    def __sign_txs(self, issuer, txs, params):
        
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
            sig_body = build_signature_body_base(
                    params["creator"],
                    params["created"],
                    params["nonce"],
                    params["privateB64"],
                    utxo_sig["publicKey"]
            )
            utxo_sig["signature"] = sig_body["signature_value"]
            utxo_sig["nonce"] = sig_body["nonce"]
            utxo_sig["creator"] = sig_body["creator"]
            tx["txout"][i]["script"] = json.dumps(utxo_sig)

        return tx


    def issue_colored_token(self, header, payload, params):
        """Issue colored token with sign. """

        # 1 send transfer proposal to get wallet.Tx
        _, issue_pre_resp = self.issue_ctoken_proposal(
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
        return self.process_tx(header, txs)


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
        result = self.__client.do_request(
                req_params,
                method
                )
        payload = json.loads(result["payload"])
        return payload

    def transfer_assets(self, header, payload, params):
        """Transfer assets."""

        # 1 send transfer proposal to get wallet.Tx
        _, trans_pre_resp = self.transfer_assets_proposal(
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
        return self.process_tx(header, txs)


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
        result = self.__client.do_request(
                req_params,
                method
                )
        payload = json.loads(result["payload"])
        return payload


    def transfer_colored_tokens(self, header, payload, params):
        """Transfer colored token. """

        # 1 send transfer proposal to get wallet.Tx
        _, trans_pre_resp = self.transfer_ctoken_proposal(
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
        return self.process_tx(header, txs)
        

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
        result = self.__client.do_request(
                req_params,
                method
                )
        payload = json.loads(result["payload"])
        return payload

    def issue_asset(self, header, payload, params):
        """Issue asset. """

         # 1 send transfer proposal to get wallet.Tx
        _, issue_pre_resp = self.issue_assets_proposal(
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
        return self.process_tx(header, txs)


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
        result = self.__client.do_request(
                req_params,
                method
                )
        payload = json.loads(result["payload"])
        return payload


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
