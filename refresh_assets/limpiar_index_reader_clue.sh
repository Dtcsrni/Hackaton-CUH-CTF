#!/usr/bin/env bash
set -euo pipefail
CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}
WORKDIR=/tmp/cuh_clear_index_reader
mkdir -p "$WORKDIR"
trap 'rm -rf "$WORKDIR"' EXIT
cat > "$WORKDIR/clear_index_reader.py" <<'PY'
import re
from CTFd import create_app
from CTFd.models import Configs, db

def strip_block(value, start, end):
    return re.sub(re.escape(start) + r'.*?' + re.escape(end), '', str(value), flags=re.S).strip()

app = create_app()
with app.app_context():
    header = Configs.query.filter_by(key='theme_header').first()
    footer = Configs.query.filter_by(key='theme_footer').first()
    header.value = strip_block(header.value, '<!-- CTFCU_INDEX_READER_STYLE_START -->', '<!-- CTFCU_INDEX_READER_STYLE_END -->')
    footer.value = strip_block(footer.value, '<!-- CTFCU_INDEX_READER_SCRIPT_START -->', '<!-- CTFCU_INDEX_READER_SCRIPT_END -->')
    db.session.commit()
    print('index reader clue cleared')
PY
docker cp "$WORKDIR/clear_index_reader.py" "$CTFD_CONTAINER:/tmp/clear_index_reader.py"
docker exec -e PYTHONPATH=/opt/CTFd "$CTFD_CONTAINER" python3 /tmp/clear_index_reader.py
