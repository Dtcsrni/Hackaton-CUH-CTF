import ssl

def build_context():
    context = ssl.create_default_context(cafile='certs/cuh_root_ca.pem')
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    return context
