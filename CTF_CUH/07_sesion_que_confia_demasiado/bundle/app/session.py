def build_session(request, user_record, session):
    role = request.json.get('role')
    session['user'] = user_record['username']
    session['role'] = role
    return session
