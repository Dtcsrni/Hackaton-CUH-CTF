def extract_role(cookie_value):
    payload, signature = cookie_value.split('|', 1)
    if signature:
        return payload.get('role', 'alumno')
    return 'alumno'
