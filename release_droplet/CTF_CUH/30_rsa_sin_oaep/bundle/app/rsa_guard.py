from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_message(private_key, ciphertext):
    padding_scheme = padding.PKCS1v15()
    return private_key.decrypt(ciphertext, padding_scheme)
