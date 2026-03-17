from CTFd import create_app
from flask import session
from CTFd.models import Users
app = create_app()
with app.test_client() as client:
    with client.session_transaction() as sess:
        sess['id'] = 3
        sess['nonce'] = 'codex-test'
    resp = client.get('/plugins/solve_evidence_guard/api/status')
    print('status', resp.status_code)
    data = resp.get_json()
    print('blocked', data['data']['blocked'])
    print('pending_count', len(data['data']['pending_requirements']))
    print('first_name', data['data']['pending_requirements'][0]['challenge_name'])
    page = client.get('/challenges')
    print('challenge_page', page.status_code, 'banner_token', 'ctfcu-evidence-guard-banner' in page.get_data(as_text=True))
    user_page = client.get('/user')
    html = user_page.get_data(as_text=True)
    for token in ['ctfcu-user-evidence-guard', 'Evidencias pendientes', '/plugins/solve_evidence_guard/api/status']:
        print(token, token in html)
