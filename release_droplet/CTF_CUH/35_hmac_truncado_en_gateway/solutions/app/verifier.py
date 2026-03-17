import hmac
import hashlib

SECRET = b'cuh-gateway-shared'

def valid_signature(body, signature):
    expected = hmac.new(SECRET, body.encode('utf-8'), hashlib.sha256).hexdigest()
    return len(signature) == 64 and hmac.compare_digest(signature, expected)
