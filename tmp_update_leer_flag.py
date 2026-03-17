from CTFd import create_app
from CTFd.models import Challenges, Flags, db
NEW_FLAG = 'CUH{leer_hasta_el_final_tiene_premio}'
app = create_app()
with app.app_context():
    chal = Challenges.query.filter_by(name='Leer también es hacking').first()
    if chal is None:
        raise SystemExit('challenge not found')
    flags = Flags.query.filter_by(challenge_id=chal.id).all()
    for f in flags:
        if hasattr(f, 'content'):
            f.content = NEW_FLAG
    db.session.commit()
    print({'challenge_id': chal.id, 'flag_count': len(flags), 'new_flag': NEW_FLAG})
