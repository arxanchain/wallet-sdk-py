# Status

[![Build Status](https://travis-ci.org/arxanchain/wallet-sdk-py.svg?branch=master)](https://travis-ci.org/arxanchain/wallet-sdk-py)

## wallet-sdk-python
Blockchain Wallet SDK includes APIs for managing wallet accounts(Decentralized Identifiers, DID),
digital assets(Proof of Existence, POE), colored tokens etc.

You need not care about how the backend blockchain runs or the unintelligible
techniques, such as consensus, endorsement and decentralization. Simply use
the SDK we provide to implement your business logics, we will handle the caching,
tagging, compressing, encrypting and high availability.

## Contributions

We appreciate all kinds of contributions, such as opening issues, fixing bugs and improving documentation.

## Install

The following command will install wallet-sdk-py in your python environment.

```sh
$ python setup.py install
```

## Usage

**Note:** Before using the wallet-sdk-python in your application, 
you need to configure your installed py-common package.
For more details please refer to [the usage of py-common](https://github.com/arxanchain/py-common#usage)

### Run unit test

The following command will run unit test

```sh
$ pytest
```

### Wallet Platform API
For details of Wallet APIs please refer to 
[Wallet APIs Documentation](http://www.arxanfintech.com/infocenter/html/development/wallet.html#wallet-platform-ref)

### Init a Client
A client is used to wrap all the encryption/decryption details, any API that visits via
the BAAS service need to use this object, you can register a client object as follows:

```python
>>> from rest.api.api import Client
>>> apikey = "pWEzB4yMM1518346407"
>>> cert_path = "/usr/local/lib/python2.7/site-packages/py_common-2.0-py2.7.egg/cryption/ecc/certs"
>>> ip_addr = "http://127.0.0.1:9143"
>>> client = Client(apikey, cert_path, ip_addr)
```

Param **apikey** is set to the API access key applied on `ChainConsole` management page,
param **cert_path** is the path of your private key file and tls certificate,
and **ip_addr** is the IP address of the BAAS server entrance. 
If you want to visit the BAAS service bypass the wasabi service,
you need to add param enable_crypto=False.

### Register a Wallet Client

To invoke the SDK API, you first have to create a wallet client as follows:

```python
>>> from api.wallet import WalletClient
>>> wallet = WalletClient(client)
```

* When building the wallet client configuration, **client** fields must
be set.

### Register wallet account

After creating the wallet client, you can use it to register a wallet account
as follows:

```python
>>> header = {}
>>> body = {
...     "id": "",
...     "type": "Organization",
...     "access": "username001",
...     "secret": "User001Pass", ## 8-16 characters including upper case, lower case and digits
...     "public_key":  {
...         "usage": "",
...         "key_type": "",
...         "public_key_data": ""
...     }
... }
>>> _, resp = wallet.register(header, body)
>>> print resp
```

* `Callback-Url` in the http header is optional. Set it only if you want to receive
events.

### Create POE digital asset

After creating the wallet account, you can create POE assets with this account as follows:

```python
>>> from api.poe import POEClient
>>> poe = POEClient(client)
>>> creator = "wallet ID"
>>> created = "123456" ## timestamp when poe is created
>>> privateB64 = "base64 formatted private key"
>>> payload = {
...     "id": "",
...     "name": "name",
...     "parent_id": "parent-poe-id",
...     "owner": "owner did",
...     "hash": "metadata-hash",
...     "metadata": map(ord, '{"address": "xxx", "telephone": "xxx", ...}')
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

* When creating a POE asset, the **name** and **owner** fields must be set, with
**owner** being the wallet account ID.

* When building the signature parameter `privateB64`, use the Base64 encoded
ED25519 private key returned by [the regisering API](https://github.com/arxanchain/wallet-sdk-py#register-a-wallet-client).

### Upload POE file

After creating POE, you can upload the POE file for this account as follows:

```python
>>> filename = "file path"
>>> poeid = "poeid"
>>> _, resp = poe.upload({}, filename, poeid)
>>> print resp
```

* The `upload` API uploads the file to **Offchain** storage, generates an SHA256
hash value, and saves this hash value into blockchain.

### Issue colored token using digital asset

Once you have possessed an asset, you can use this specific asset to issue colored
tokens as follows:

```python
>>> from api.transaction import Transaction
>>> txn = Transaction(client)
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

* When issuing colored tokens, you need to specify an issuer(a wallet account ID),
an asset to issue tokens, and the owner(another wallet account ID).

### Transfer colored tokens

After issuing colored tokens, the asset owner's wallet account will have these
tokens, and can transfer some of them to other wallet accounts.

```python
>>> payload = {
...     "from": "from did",
...     "to": "to did",
...     "asset_id": "asset id",
...     "tokens": [
...         {
...             "token_id": "token id",
...             "amount": 5
...         }
...     ],
...     "fee": {
...         "amount": 5,
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

### Use callback URL to receive blockchain transaction events
Each of the APIs to invoke blockchain has two invoking modes: - `sync` and `async`.

The default invoking mode is asynchronous, it will return without waiting for
blockchain transaction confirmation. In asynchronous mode, you should set
'Callback-Url' in the http header to receive blockchain transaction events.

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

A blockchain transaction event sample as follows:

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

If you want to switch to synchronous invoking mode, set the 'Bc-Invoke-Mode' header
to 'sync'. In synchronous mode, it will not return until the blockchain
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
