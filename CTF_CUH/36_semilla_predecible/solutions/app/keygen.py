import secrets

def build_key():
    key = secrets.token_bytes(32)
    return key.hex()
