#!/usr/bin/env bash
set -euo pipefail
CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}
WORKDIR=/tmp/cuh_ctfd_index_reader
mkdir -p "$WORKDIR"
trap 'rm -rf "$WORKDIR"' EXIT
cat > "$WORKDIR/apply_index_reader.py" <<'PY'
import re
from CTFd import create_app
from CTFd.models import Configs, db

STYLE = r'''<!-- CTFCU_INDEX_READER_STYLE_START --><style id="ctfcu-index-reader-style">.cuhv-index-reader-clue{display:inline-flex;width:fit-content;margin-top:8px;padding:6px 10px;border-radius:999px;font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:.66rem;letter-spacing:.08em;color:rgba(236,245,255,.12);background:rgba(5,12,24,.14);border:1px solid rgba(173,214,255,.08);backdrop-filter:blur(6px);user-select:text}.cuhv-index-reader-clue[data-mounted="1"]{animation:ctfcuReaderPulse 5s ease-in-out infinite}@keyframes ctfcuReaderPulse{0%{opacity:.28}50%{opacity:.92}100%{opacity:.34}}@media (max-width:680px){.cuhv-index-reader-clue{margin-top:10px}}</style><!-- CTFCU_INDEX_READER_STYLE_END -->'''

SCRIPT = r'''<!-- CTFCU_INDEX_READER_SCRIPT_START --><script id="ctfcu-index-reader-script">(()=>{const mount=()=>{if(window.location.pathname!=='/'){return;}if(document.querySelector('.cuhv-index-reader-clue[data-mounted=\"1\"]')){return;}const target=document.querySelector('.cuhv-cover-shell figcaption,.cuhv-logo-badge span:last-child,.cuhv-hero-copy p:last-of-type');if(!target){return;}const clue=document.createElement('span');clue.className='cuhv-index-reader-clue';clue.dataset.mounted='1';clue.textContent=['sello-interno=CUH{leer','_tambien','_es_','hacking}'].join('');target.appendChild(clue);};document.addEventListener('DOMContentLoaded',mount);window.addEventListener('load',mount);new MutationObserver(mount).observe(document.documentElement,{childList:true,subtree:true});})();</script><!-- CTFCU_INDEX_READER_SCRIPT_END -->'''

def upsert(value, start, end, block):
    value = re.sub(re.escape(start) + r'.*?' + re.escape(end), '', str(value), flags=re.S).strip()
    return (value + '\n' if value else '') + block + '\n'

app = create_app()
with app.app_context():
    header = Configs.query.filter_by(key='theme_header').first()
    footer = Configs.query.filter_by(key='theme_footer').first()
    header.value = upsert(header.value, '<!-- CTFCU_INDEX_READER_STYLE_START -->', '<!-- CTFCU_INDEX_READER_STYLE_END -->', STYLE)
    footer.value = upsert(footer.value, '<!-- CTFCU_INDEX_READER_SCRIPT_START -->', '<!-- CTFCU_INDEX_READER_SCRIPT_END -->', SCRIPT)
    db.session.commit()
    print('index reader clue synced')
PY
docker cp "$WORKDIR/apply_index_reader.py" "$CTFD_CONTAINER:/tmp/apply_index_reader.py"
docker exec -e PYTHONPATH=/opt/CTFd "$CTFD_CONTAINER" python3 /tmp/apply_index_reader.py
