from CTFd import create_app
from CTFd.models import Challenges, Solves, Fails, db

app = create_app()
with app.app_context():
    chal = Challenges.query.filter_by(name="Leer también es hacking").first()
    if chal is None:
        raise SystemExit("challenge not found")
    solves = Solves.query.filter_by(challenge_id=chal.id).all()
    fails = Fails.query.filter_by(challenge_id=chal.id).all()
    for row in solves:
        db.session.delete(row)
    for row in fails:
        db.session.delete(row)
    db.session.commit()
    print({"challenge_id": chal.id, "deleted_solves": len(solves), "deleted_fails": len(fails)})
