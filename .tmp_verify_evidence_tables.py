from CTFd import create_app
from CTFd.models import db
app = create_app()
with app.app_context():
    rows = db.session.execute(db.text("SHOW TABLES LIKE 'ctfcu_solve_evidence_%'" )).fetchall()
    print(rows)
    if rows:
        req = db.session.execute(db.text("SELECT status, COUNT(*) FROM ctfcu_solve_evidence_requirements GROUP BY status ORDER BY status" )).fetchall()
        print(req)
