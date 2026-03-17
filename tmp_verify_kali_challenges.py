
from CTFd import create_app
from CTFd.models import Challenges, Flags, Hints, ChallengeFiles
NAMES = [
    'Traza en PCAP',
    'Firmware en capas',
    'Metadatos en cascada',
    'Carving de evidencias',
    'Diccionario de laboratorio',
]
app = create_app()
with app.app_context():
    rows = []
    all_rows = Challenges.query.all()
    missing_flags = [c.name for c in all_rows if Flags.query.filter_by(challenge_id=c.id).count() == 0]
    for name in NAMES:
        chal = Challenges.query.filter_by(name=name).first()
        rows.append((name, chal.category if chal else None, chal.value if chal else None,
                     Flags.query.filter_by(challenge_id=chal.id).count() if chal else 0,
                     Hints.query.filter_by(challenge_id=chal.id).count() if chal else 0,
                     ChallengeFiles.query.filter_by(challenge_id=chal.id).count() if chal else 0))
    print('rows', rows)
    print('challenge_count', len(all_rows))
    print('missing_flags', missing_flags)
