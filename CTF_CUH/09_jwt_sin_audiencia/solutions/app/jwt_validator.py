import time

ALLOWED_ALGORITHMS = {'HS256'}

def validate_token(header, payload):
    now = int(time.time())
    expected_issuer = 'cuh-auth'
    expected_audience = 'panel-interno'
    if header.get('alg') not in ALLOWED_ALGORITHMS:
        raise ValueError('algoritmo no permitido')
    if payload.get('iss') != expected_issuer:
        raise ValueError('issuer invalido')
    if payload.get('aud') != expected_audience:
        raise ValueError('audiencia invalida')
    if payload.get('exp', 0) < now:
        raise ValueError('token expirado')
    return payload
