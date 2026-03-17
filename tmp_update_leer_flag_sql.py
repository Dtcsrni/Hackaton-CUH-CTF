from sqlalchemy import text
from CTFd import create_app
from CTFd.models import Challenges, db
NEW_FLAG = 'CUH{leer_hasta_el_final_tiene_premio}'
app = create_app()
with app.app_context():
    chal = Challenges.query.filter_by(name='Leer también es hacking').first()
    if chal is None:
        raise SystemExit('challenge not found')
    db.session.execute(text('UPDATE flags SET content = :flag WHERE challenge_id = :cid'), {'flag': NEW_FLAG, 'cid': chal.id})
    db.session.commit()
    row = db.session.execute(text('SELECT content FROM flags WHERE challenge_id = :cid'), {'cid': chal.id}).fetchall()
    print({'challenge_id': chal.id, 'rows': [r[0] for r in row]})
