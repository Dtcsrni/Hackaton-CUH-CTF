#!/usr/bin/env bash
set -euo pipefail
CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}
HOST_HTML=${1:-/tmp/index_cuh_latest.html}
WORKDIR=/tmp/cuh_force_index
mkdir -p "$WORKDIR"
trap 'rm -rf "$WORKDIR"' EXIT

if [[ ! -f "$HOST_HTML" ]]; then
  echo "HTML source not found: $HOST_HTML" >&2
  exit 1
fi

docker cp "$HOST_HTML" "$CTFD_CONTAINER:/tmp/index_cuh_latest.html"

cat > "$WORKDIR/force_index.py" <<'PY'
from pathlib import Path
from CTFd import create_app
from CTFd.models import Pages, db

app = create_app()
with app.app_context():
    page = Pages.query.filter_by(route='index').first()
    if page is None:
        raise SystemExit('index page not found')
    page.content = Path('/tmp/index_cuh_latest.html').read_text(encoding='utf-8')
    db.session.commit()
    print('index page forced')
PY

docker cp "$WORKDIR/force_index.py" "$CTFD_CONTAINER:/tmp/force_index.py"
docker exec -e PYTHONPATH=/opt/CTFd "$CTFD_CONTAINER" python3 /tmp/force_index.py
