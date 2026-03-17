import time

def validate_token(header, payload):
    now = int(time.time())
    if payload.get('exp', 0) < now:
        raise ValueError('token expirado')
    return payload
