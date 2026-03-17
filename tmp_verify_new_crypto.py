
from CTFd import create_app
from CTFd.models import Challenges, Flags, Hints, ChallengeFiles
NAMES = [
    'CBC sin integridad',
    'IV reciclado en reportes',
    'HMAC truncado en gateway',
    'Semilla predecible',
    'Certificados a ciegas',
]
app = create_app()
with app.app_context():
    rows = []
    for name in NAMES:
        chal = Challenges.query.filter_by(name=name).first()
        rows.append((name, chal.category if chal else None, chal.value if chal else None,
                     Flags.query.filter_by(challenge_id=chal.id).count() if chal else 0,
                     Hints.query.filter_by(challenge_id=chal.id).count() if chal else 0,
                     ChallengeFiles.query.filter_by(challenge_id=chal.id).count() if chal else 0,
                     len((chal.description or '').strip()) if chal else 0))
    print('rows', rows)
    all_rows = Challenges.query.all()
    missing_flags = [c.name for c in all_rows if Flags.query.filter_by(challenge_id=c.id).count() == 0]
    print('challenge_count', len(all_rows))
    print('missing_flags', missing_flags)
