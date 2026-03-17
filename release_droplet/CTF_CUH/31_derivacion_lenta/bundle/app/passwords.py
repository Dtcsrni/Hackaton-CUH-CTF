import hashlib

salt = b'cuh-static'

def derive_secret(password):
    return hashlib.sha1(password.encode('utf-8') + salt).hexdigest()
