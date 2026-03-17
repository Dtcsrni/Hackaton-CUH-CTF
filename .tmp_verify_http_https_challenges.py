from pathlib import Path
import json
from CTFd import create_app
from CTFd.models import Challenges, Hints, Flags, ChallengeFiles, Pages
names = [
    'Portal sin redirección segura',
    'HSTS pendiente',
    'Cookie de sesión sin Secure',
    'Contenido mixto heredado',
    'Credenciales expuestas en tránsito',
]
app = create_app()
with app.app_context():
    rows = []
    for name in names:
        chal = Challenges.query.filter_by(name=name).first()
        rows.append((
            name,
            chal.category if chal else None,
            chal.value if chal else None,
            Flags.query.filter_by(challenge_id=chal.id).count() if chal else None,
            Hints.query.filter_by(challenge_id=chal.id).count() if chal else None,
            ChallengeFiles.query.filter_by(challenge_id=chal.id).count() if chal else None,
        ))
    page_routes = [
        'portal-sin-redireccion-segura',
        'hsts-pendiente',
        'cookie-de-sesion-sin-secure',
        'contenido-mixto-heredado',
        'credenciales-expuestas-en-transito',
    ]
    page_rows = [(route, Pages.query.filter_by(route=route).count()) for route in page_routes]
    print(rows)
    print(page_rows)
