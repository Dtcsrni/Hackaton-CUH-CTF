from CTFd import create_app
app = create_app()
print(app.config.get('REVERSE_PROXY'))
