from CTFd import create_app
app = create_app()
with app.test_client() as client:
    with client.session_transaction() as sess:
        sess['id'] = 3
    resp = client.post('/api/v1/challenges/attempt', json={'challenge_id': 21, 'submission': 'CUH{dummy}'})
    print('status', resp.status_code)
    payload = resp.get_json() or {}
    print('api_status', payload.get('data', {}).get('status'))
    print('message', payload.get('data', {}).get('message'))
