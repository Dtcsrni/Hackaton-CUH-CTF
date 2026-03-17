#!/usr/bin/env bash
set -euo pipefail
CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}
BACKUP_ROOT=/opt/cuh-ctf/artifacts/backups
STAMP=$(date -u +%Y%m%d%H%M%S)
BACKUP_DIR="${BACKUP_ROOT}/reset_leer_${STAMP}"
mkdir -p "$BACKUP_DIR"

docker exec -e PYTHONPATH=/opt/CTFd "$CTFD_CONTAINER" python3 - <<'PY' > "${BACKUP_DIR}/snapshot.json"
import json
from CTFd import create_app
from CTFd.models import Challenges, Solves, Fails

app = create_app()
with app.app_context():
    chal = Challenges.query.filter_by(name='Leer también es hacking').first()
    if chal is None:
        raise SystemExit('challenge not found')
    solves = Solves.query.filter_by(challenge_id=chal.id).all()
    fails = Fails.query.filter_by(challenge_id=chal.id).all()
    print(json.dumps({
        'challenge_id': chal.id,
        'challenge_name': chal.name,
        'solve_count': len(solves),
        'fail_count': len(fails),
        'solves': [
            {
                'id': s.id,
                'account_id': getattr(s, 'account_id', None),
                'user_id': getattr(s, 'user_id', None),
                'team_id': getattr(s, 'team_id', None),
                'date': s.date.isoformat() if getattr(s, 'date', None) else None,
            }
            for s in solves
        ],
        'fails': [
            {
                'id': f.id,
                'account_id': getattr(f, 'account_id', None),
                'user_id': getattr(f, 'user_id', None),
                'team_id': getattr(f, 'team_id', None),
                'date': f.date.isoformat() if getattr(f, 'date', None) else None,
            }
            for f in fails
        ],
    }, ensure_ascii=False, indent=2))
PY

docker exec -e PYTHONPATH=/opt/CTFd "$CTFD_CONTAINER" python3 - <<'PY'
from CTFd import create_app
from CTFd.models import Challenges, Solves, Fails, db

app = create_app()
with app.app_context():
    chal = Challenges.query.filter_by(name='Leer también es hacking').first()
    if chal is None:
        raise SystemExit('challenge not found')
    solves = Solves.query.filter_by(challenge_id=chal.id).all()
    fails = Fails.query.filter_by(challenge_id=chal.id).all()
    for row in solves:
        db.session.delete(row)
    for row in fails:
        db.session.delete(row)
    db.session.commit()
    print({'challenge_id': chal.id, 'deleted_solves': len(solves), 'deleted_fails': len(fails)})
PY

echo "$BACKUP_DIR"
