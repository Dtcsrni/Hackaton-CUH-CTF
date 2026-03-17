import secrets
import time

RESET_STORE = {}

def issue_reset_token(username):
    token = secrets.token_urlsafe(24)
    expires_at = int(time.time()) + 900
    RESET_STORE[token] = {'username': username, 'expires_at': expires_at}
    return token

def validate_reset(username, token):
    now = int(time.time())
    token_record = RESET_STORE.get(token)
    if not token_record:
        return False
    if token_record['username'] != username:
        return False
    if token_record['expires_at'] < now:
        return False
    return True
