from CTFd import create_app
app = create_app()
with app.test_client() as client:
    with client.session_transaction() as sess:
        sess['id'] = 3
    resp = client.post('/api/v1/challenges/attempt', json={'challenge_id': 21, 'submission': 'CUH{dummy}'})
    print('status', resp.status_code)
    print(resp.get_data(as_text=True)[:1000])
