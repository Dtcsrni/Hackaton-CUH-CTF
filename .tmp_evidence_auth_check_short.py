from CTFd import create_app
app = create_app()
with app.test_client() as client:
    with client.session_transaction() as sess:
        sess['id'] = 3
    resp = client.get('/plugins/solve_evidence_guard/api/status')
    print('status', resp.status_code)
    payload = resp.get_json() or {}
    print('blocked', payload.get('data', {}).get('blocked'))
    print('pending_count', len(payload.get('data', {}).get('pending_requirements', [])))
    page = client.get('/user')
    html = page.get_data(as_text=True)
    print('user_status', page.status_code)
    print('user_has_guard', 'ctfcu-user-evidence-guard' in html)
