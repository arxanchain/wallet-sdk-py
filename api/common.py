from cryption.crypto import sign

VERSION = "v1"
APIKEYHEADER = "API-Key"
FABIOROUTETAGHEADER = "Host"
ROUTETAG = "Route-Tag"
InvokeModeSync = "sync"
InvokeModeAsync = "async"

InvokeModeHeader = "BC-Invoke-Mode"

def build_signature_body(creator, created, nonce, privateB64, payload):
    """Build signature body dict.

    :param creator: creator string to be signed
    :param created: created timestamp
    :param nonce: nonce
    :param privateB64: secret key used for ed25519 signature
    :param payload: payload dict to be signed
    :Returns: signed body dict
    """
    
    signature = sign(payload, privateB64, creator, nonce)
    result = {
        "creator": creator,
        "created": created,
        "nonce": nonce,
        "signature_value": signature
        }
    return result

