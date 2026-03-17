#!/usr/bin/env bash
set -euo pipefail

CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}

python3 - <<'PY'
from pathlib import Path
import json
import re

SCRIPT_PATHS = [
    Path('/opt/cuh-ctf/scripts/registrar_ctfd_via_internal.sh'),
    Path('/opt/cuh-ctf/scripts/registrar_cracking_via_internal.sh'),
    Path('/opt/cuh-ctf/scripts/registrar_formularios_via_internal.sh'),
    Path('/opt/cuh-ctf/scripts/registrar_jwt_via_internal.sh'),
    Path('/opt/cuh-ctf/scripts/registrar_frontend_via_internal.sh'),
    Path('/opt/cuh-ctf/scripts/registrar_cookies_via_internal.sh'),
    Path('/opt/cuh-ctf/scripts/registrar_bruteforce_via_internal.sh'),
]

HELPER_BLOCK_SPACED = """app = create_app()\n\n\
def hint_costs(category, total):\n\
    if category == 'Calentamiento':\n\
        return [0 for _ in range(total)]\n\
    return [(idx + 1) * 10 for idx in range(total)]\n"""

HELPER_BLOCK_TIGHT = """app=create_app()\n\n\
def hint_costs(category, total):\n\
    if category == 'Calentamiento':\n\
        return [0 for _ in range(total)]\n\
    return [(idx + 1) * 10 for idx in range(total)]\n"""

REPLACEMENTS = {
    "for hint_text in spec['hints']:\n            db.session.add(Hints(challenge_id=chal.id, type='standard', content=hint_text, cost=0, requirements=None))": (
        "hint_cost_list = hint_costs(spec['category'], len(spec['hints']))\n"
        "        for idx, hint_text in enumerate(spec['hints']):\n"
        "            db.session.add(Hints(challenge_id=chal.id, type='standard', content=hint_text, cost=hint_cost_list[idx], requirements=None))"
    ),
    "for hint_text in spec['hints']:\n            db.session.add(Hints(challenge_id=chal.id,type='standard',content=hint_text,cost=0,requirements=None))": (
        "hint_cost_list = hint_costs(spec['category'], len(spec['hints']))\n"
        "        for idx, hint_text in enumerate(spec['hints']):\n"
        "            db.session.add(Hints(challenge_id=chal.id,type='standard',content=hint_text,cost=hint_cost_list[idx],requirements=None))"
    ),
    "for hint in spec['hints']: db.session.add(Hints(challenge_id=challenge.id,content=hint,cost=0))": (
        "hint_cost_list = hint_costs(spec['category'], len(spec['hints']))\n"
        "    for idx, hint in enumerate(spec['hints']): db.session.add(Hints(challenge_id=challenge.id,content=hint,cost=hint_cost_list[idx]))"
    ),
}

for path in SCRIPT_PATHS:
    text = path.read_text(encoding='utf-8')
    original = text
    if "def hint_costs(category, total):" not in text:
        if "app = create_app()\n" in text:
            text = text.replace("app = create_app()\n", HELPER_BLOCK_SPACED, 1)
        elif "app=create_app()\n" in text:
            text = text.replace("app=create_app()\n", HELPER_BLOCK_TIGHT, 1)
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding='utf-8')

for path in Path('/opt/cuh-ctf/artifacts/ctfd_api_payloads').glob('hints_*.json'):
    data = json.loads(path.read_text(encoding='utf-8'))
    changed = False
    for idx, hint in enumerate(data):
        new_cost = (idx + 1) * 10
        if hint.get('cost') != new_cost:
            hint['cost'] = new_cost
            changed = True
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

for path in Path('/opt/cuh-ctf/artifacts/ctfcli').glob('*/challenge.yml'):
    lines = path.read_text(encoding='utf-8').splitlines()
    out = []
    in_hints = False
    hint_idx = 0
    for line in lines:
        stripped = line.strip()
        if stripped == 'hints:':
            in_hints = True
            hint_idx = 0
            out.append(line)
            continue
        if in_hints and re.match(r'^\s+cost:\s*\d+\s*$', line):
            hint_idx += 1
            indent = line.split('cost:')[0]
            out.append(f'{indent}cost: {hint_idx * 10}')
            continue
        if in_hints and stripped and not line.startswith('  -') and not line.startswith('    '):
            in_hints = False
        out.append(line)
    path.write_text('\n'.join(out) + '\n', encoding='utf-8')
PY

docker exec -i "${CTFD_CONTAINER}" python3 - <<'PY'
from CTFd import create_app
from CTFd.models import Challenges, Hints, db

app = create_app()

with app.app_context():
    for challenge in Challenges.query.order_by(Challenges.id).all():
        hints = Hints.query.filter_by(challenge_id=challenge.id).order_by(Hints.id).all()
        for idx, hint in enumerate(hints):
            hint.cost = 0 if challenge.category == 'Calentamiento' else (idx + 1) * 10
    db.session.commit()
    print('hint costs updated in database')
PY

bash /opt/cuh-ctf/scripts/registrar_ctfd_via_internal.sh

docker exec -i "${CTFD_CONTAINER}" python3 - <<'PY'
from CTFd import create_app
from CTFd.models import Challenges, Hints

app = create_app()

with app.app_context():
    bad = []
    for challenge in Challenges.query.order_by(Challenges.id).all():
        hints = Hints.query.filter_by(challenge_id=challenge.id).order_by(Hints.id).all()
        for idx, hint in enumerate(hints, start=1):
            expected = 0 if challenge.category == 'Calentamiento' else idx * 10
            if hint.cost != expected:
                bad.append((challenge.name, challenge.category, hint.id, hint.cost, expected))
    if bad:
        for row in bad:
            print('BAD|' + '|'.join(str(v) for v in row))
        raise SystemExit(1)
    print('hint cost policy verified')
PY
