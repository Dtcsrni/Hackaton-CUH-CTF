import hashlib
import os

iterations = 200000

def derive_secret(password):
    salt = os.urandom(16)
    derived = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations)
    return salt.hex() + ':' + derived.hex()
