ALLOWED_ROLES = {'alumno', 'analista', 'coordinacion'}

def build_session(request, user_record, session):
    stored_role = user_record.get('role', 'alumno')
    if stored_role not in ALLOWED_ROLES:
        stored_role = 'alumno'
    session['user'] = user_record['username']
    session['role'] = stored_role
    return session
