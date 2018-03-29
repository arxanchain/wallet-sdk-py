# Status

[![Build Status](https://travis-ci.org/arxanchain/wallet-sdk-py.svg?branch=master)](https://travis-ci.org/arxanchain/wallet-sdk-py)

## wallet-sdk-python
Blockchain Wallet SDK includes APIs for the management of wallet accounts(DID),
digital assets(POE), colored tokens etc.

You need not care about how the backend blockchain runs or the unintelligible
techniques, such as consensus, endorsement and decentralization. Simply use
the SDK we provide to implement your business logics, we will handle the caching,
tagging, compressing, encrypting and high availability.

## Contributions

Welcome for any kind of contributions, such as open issues, fix bugs and improve documentation

## Install

The following command will install wallet-sdk-py in your python environment

```sh
$ pip install -r requirements.txt # install requirements
$ python setup.py install # install wallet-sdk-py
```

## Usage

**Note:** Before using the wallet-sdk-python in your operating system, 
you need to configure your installed py-common package,
for more details please refer to [usage of py-common](https://github.com/arxanchain/py-common#usage)

### Run unit test

The following command will run unit test

```sh
$ pytest
```

### Wallet Platform API
Details of Wallet APIs please refer to 
[Wallet APIs Documentation](http://www.arxanfintech.com/infocenter/html/development/wallet.html#wallet-platform-ref)

### Register a Wallet Client

To invoke the SDK API, you first have to create a wallet client as follows:

```python
>>> from api.wallet import WalletClient
>>> url = "http://127.0.0.1:9143"
>>> apikey = "pWEzB4yMM1518346407"
>>> cert_path = "/usr/local/lib/python2.7/site-packages/py_common-1.5.0-py2.7.egg/cryption/ecc/certs"
>>> wallet = WalletClient(
...     url,
...     apikey,
...     cert_path
...     )
```

* At building the client configuration, the **url** and **apikey** fields must
be set. The **url** is set to the http address of wasabi service, and the
**apikey** is set to the API access key applied on `ChainConsole` management page.

### Register wallet account

After creating wallet client, you can use this client to register wallet account
as follows:

```python
>>> header = {}
>>> body = {
...     "id": "",
...     "type": "Organization",
...     "access": "username001",
...     "secret": "User001Pass", ##8-16 characters including upper case, lower case and digits
...     "public_key":  {
...         "usage": "",
...         "key_type": "",
...         "public_key_data": ""
...     }
... }
>>> _, resp = wallet.register(header, body)
>>> print resp
```

* `Callback-Url` in http header is optional. If you want to receive blockchain transaction
event, you need to set `Callback-Url` in header; if not, you don't have to set it.

### Create POE digital asset

After creation wallet account, you can create POE asset for this account as follows:

```python
>>> from api.poe import POEClient
>>> poe = POEClient(url, apikey, cert_path)
>>> creator = "wallet ID"
>>> created = "123456" ## timestamp when poe is created
>>> privateB64 = "base64 formatted private key"
>>> payload = {
...     "id": "",
...     "name": "name",
...     "parent_id": "parent-poe-id",
...     "owner": "owner did",
...     "hash": "metadata-hash",
...     "metadata": '{
...         "address": "xxx",
...         "telephone": "xxx",
...         ...
...     }'
... }
>>> params = {
...     "header": {},
...     "creator": creator,
...     "created": created,
...     "privateB64": privateB64,
...     "payload": payload
...     }
>>> _, resp = poe.create_with_sign(**params)
>>> print resp
```

* At creating POE asset, the **name** and **owner** fields must be set, and the
**owner** field must be set to the wallet account ID.

* At building the signature parameter, using the ed25519 private key returned
by regiser wallet API to do ed25519 signature.

### Upload POE file

After creation POE, you can upload POE file for this account as follows:

```python
>>> filename = "file path"
>>> poeid = "poeid"
>>> _, resp = poe.upload({}, filename, poeid)
>>> print resp
```

* `upload` API uploads the file to **Offchain** storage, and generates SHA256
hash value for this file, then saves this hash value into blockchain.

### Issue colored token using digital asset

Once you have specified asset, you can use this specified asset to issue colored
token as follows:

```python
>>> from api.transaction import Transaction
>>> txn = Transaction(url, apikey, cert_path)
>>> creator = "creator"
>>> created = 12345
>>> privateB64 = "base64 formatted private key"
>>> payload = {
...     "issuer": "issuer did",
...     "owner": "owner did",
...     "asset_id": "asset did",
...     "amount": 1000,
...     "fees": {
...         "accounts": [
...             "accounts did"
...         ],
...         "coins": [
...             {
...                 "coin_id": "coin id",
...                 "amount": 5
...             }
...         ]
...     }
... }
>>> params = {
...     "header": {},
...     "creator": creator,
...     "created": created,
...     "privateB64": privateB64,
...     "payload": payload
...     }
>>> _, resp = txn.issue_colored_token_with_sign(**params)
```

* At issuing colored token, you need to specify an issuer(one wallet account ID),
an asset to be used to issue token, and the owner(another wallet account ID) who
has the asset.

### Transfer colored tokens

After issuing colored token, the asset owner's wallet account will have these
colored tokens, and can transfer some of them to other wallet account.

```python
>>> payload = {
...     "from": "from did",
...     "to": "to did",
...     "asset_id": "asset id",
...     "coins": [
...         {
...             "coin_id": "coin id",
...             "amount": 5
...         }
...     ],
...     "fees": {
...         "accounts": [
...             "account did"
...         ],
...         "coins": [
...             {
...                 "coin_id": "coin id",
...                 "amount": 5
...             }
...         ]
...     }
... }
>>> params = {
...     "header": {},
...     "creator": creator,
...     "created": created,
...     "privateB64": privateB64,
...     "payload": payload
...     }
>>> _, resp = txn.transfer_assets_with_sign(**params)
>>> print resp
```

### Query colored token balance

You can use the `query_wallet_balance` API to get the balance of the specified wallet
account as follows:

```python
>>> id_ = "wallet id"
>>> _, resp = wallet.query_wallet_balance({}, id_)
>>> print resp
```

### Using callback URL to receive blockchain transaction event
Each of the APIs for invoking blockchain has two invoking modes, one is `sync`
mode, the other is `async` mode.

The default invoking mode is asynchronous, it will return without waiting for
blockchain transaction confirmation. In asynchronous mode, you should set
'Callback-Url' in http header used to receive blockchain transaction event.

The blockchain transaction event structure is defined as follows:

```code
import google_protobuf "github.com/golang/protobuf/ptypes/timestamp

// Blockchain transaction event payload
type BcTxEventPayload struct {
    BlockNumber   uint64                     `json:"block_number"`   // Block number
    BlockHash     []byte                     `json:"block_hash"`     // Block hash
    ChannelId     string                     `json:"channel_id"`     // Channel ID
    ChaincodeId   string                     `json:"chaincode_id"`   // Chaincode ID
    TransactionId string                     `json:"transaction_id"` // Transaction ID
    Timestamp     *google_protobuf.Timestamp `json:"timestamp"`      // Transaction timestamp
    IsInvalid     bool                       `json:"is_invalid"`     // Is transaction invalid
    Payload       interface{}                `json:"payload"`        // Transaction Payload
}
```

One blockchain transaction event sample as follows:

```code
{
    "block_number":63,
    "block_hash":"vTRmfHZ3aaecbbw2A5zPcuzekUC42Lid3w+i6dOU5C0=",
    "channel_id":"pubchain",
    "chaincode_id":"pubchain-c4:",
    "transaction_id":"243eaa6e695cc4ce736e765395a64b8b917ff13a6c6500a11558b5e94e02556a",
    "timestamp":{
        "seconds":1521189855,
        "nanos":192203115
    },
    "is_invalid":false,
    "payload":{
        "id":"4debe20b-ca00-49b0-9130-026a1aefcf2d",
        "metadata": '{
            "member_id_value":"3714811988020512",
            "member_mobile":"6666",
            "member_name":"8777896121269017",
            "member_truename":"Tony"
        }'
    }
}
```

If you want to switch to synchronous invoking mode, set 'Bc-Invoke-Mode' header
to 'sync' value. In synchronous mode, it will not return until the blockchain
transaction is confirmed.

```python
>>> header = {
...     "Bc-Invoke-Mode": "sync"
... }
>>> body = {
...     ...
...     }
... }
>>> _, resp = wallet.register(header, body)
>>> print resp
```
