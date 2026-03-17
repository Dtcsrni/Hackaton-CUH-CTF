from CTFd import create_app
from CTFd.models import db
app = create_app()
with app.app_context():
    rows = db.session.execute(db.text("SELECT u.id, u.name, COUNT(r.id) AS pending FROM ctfcu_solve_evidence_requirements r JOIN users u ON u.id = r.user_id WHERE r.status='pending' GROUP BY u.id, u.name ORDER BY pending DESC, u.id ASC" )).fetchall()
    print(rows)
    top = db.session.execute(db.text("SELECT u.name, c.name, c.value, TIMESTAMPDIFF(SECOND, r.opened_at, r.solved_at) AS elapsed, r.reason FROM ctfcu_solve_evidence_requirements r JOIN users u ON u.id = r.user_id JOIN challenges c ON c.id = r.challenge_id ORDER BY r.solved_at ASC LIMIT 20" )).fetchall()
    print(top)
