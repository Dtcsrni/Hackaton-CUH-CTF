
from CTFd import create_app
from CTFd.models import Challenges, Hints
app = create_app()
with app.app_context():
    rows = Challenges.query.all()
    bad = []
    for c in rows:
        hints = Hints.query.filter_by(challenge_id=c.id).order_by(Hints.cost.asc()).all()
        if len(hints) != 3:
            bad.append((c.name, len(hints)))
    print('challenge_count', len(rows))
    print('bad_hint_counts', bad)
    for target in ['Puertas abiertas', 'Consulta concatenada', 'Prompt de soporte indiscreto', 'Bloques repetidos', 'Certificados a ciegas']:
        c = Challenges.query.filter_by(name=target).first()
        hints = Hints.query.filter_by(challenge_id=c.id).order_by(Hints.cost.asc()).all()
        print('---', target)
        for h in hints:
            print(h.cost, h.content)
