import hashlib
import hmac
import json

SECRET = b'cuh-cookie-role'
ALLOWED_ROLES = {'alumno', 'analista', 'coordinacion'}

def extract_role(cookie_value):
    payload_raw, signature = cookie_value.rsplit('|', 1)
    expected = hmac.new(SECRET, payload_raw.encode('utf-8'), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        return 'alumno'
    payload = json.loads(payload_raw)
    role = payload.get('role', 'alumno')
    return role if role in ALLOWED_ROLES else 'alumno'
