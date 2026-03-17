import hmac
import hashlib

SECRET = b'cuh-gateway-shared'

def valid_signature(body, signature):
    expected = hmac.new(SECRET, body.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature[:8] == expected[:8]
