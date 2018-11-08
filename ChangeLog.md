# WALLET-SDK-PY Changelog

## v2.0.1

* Wrap class POEClient, Transaction into WalletClient
* Replace function create_poe_with_sign into create_poe
* Issue_ctoken, transfer_ctoken, issue_asset, transfer_asset were splitted into two steps separately.

## v2.1.2

* Implements get_tx_logs/get_tx_utxo/get_tx_stxo APIs

## v3.0

* Update crypto mode from sign && encrypt into two-way HTTPs
* Update version of transaction APIs from `v1` to `v2`
* Expose ``sign_txs`` to client
