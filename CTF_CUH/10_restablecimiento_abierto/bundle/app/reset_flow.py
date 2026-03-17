def issue_reset_token(username):
    return f"reset-{username}"

def validate_reset(username, token):
    return token == f"reset-{username}"
