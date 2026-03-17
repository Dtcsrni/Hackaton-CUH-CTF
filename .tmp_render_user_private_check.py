
from CTFd import create_app
from flask import render_template
from CTFd.models import Users
app = create_app()
with app.app_context():
    user = Users.query.order_by(Users.id.asc()).first()
    with app.test_request_context('/user'):
        html = render_template('users/private.html', user=user, account=user)
        for token in ['Resumen util del recorrido','Hints comprados','Categorias dominadas','Actividad reciente']:
            print(token, token in html)
        print('premios_old', 'Premios y reconocimientos' in html)
