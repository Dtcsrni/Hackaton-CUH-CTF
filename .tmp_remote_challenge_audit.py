from CTFd import create_app
from CTFd.models import Challenges, Flags, Hints, ChallengeFiles
import json
app = create_app()
with app.app_context():
    rows = []
    for c in Challenges.query.order_by(Challenges.id.asc()).all():
        desc = c.description or ""
        rows.append({
            "id": c.id,
            "name": c.name,
            "category": c.category,
            "value": c.value,
            "description_len": len(desc),
            "has_attachment_words": any(word in desc.lower() for word in ["archivo", "adjunto", "bundle", "zip", "material"]),
            "flags": Flags.query.filter_by(challenge_id=c.id).count(),
            "hints": Hints.query.filter_by(challenge_id=c.id).count(),
            "files": ChallengeFiles.query.filter_by(challenge_id=c.id).count(),
        })
    print(json.dumps(rows, ensure_ascii=False))
