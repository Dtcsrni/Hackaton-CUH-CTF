from CTFd import create_app
from CTFd.models import Challenges, Solves
import json
app = create_app()
with app.app_context():
    rows = []
    for c in Challenges.query.order_by(Challenges.id.asc()).all():
        rows.append({
            "id": c.id,
            "name": c.name,
            "value": c.value,
            "solves": Solves.query.filter_by(challenge_id=c.id).count(),
        })
    print(json.dumps(rows, ensure_ascii=False))
