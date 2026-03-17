#!/usr/bin/env bash
set -euo pipefail
cd /tmp/cuh_ui_refresh
bash update_navbar_experience.sh
for target in \
  /opt/CTFd/CTFd/themes/core/templates/challenges.html \
  /opt/CTFd/CTFd/themes/core-beta/templates/challenges.html
 do
  if docker exec ctfd-ctfd-1 sh -lc "[ -f '$target' ]"; then
    docker cp challenges.html ctfd-ctfd-1:$target
  fi
 done
for target in \
  /opt/CTFd/CTFd/themes/core/templates/scoreboard.html \
  /opt/CTFd/CTFd/themes/core-beta/templates/scoreboard.html
 do
  if docker exec ctfd-ctfd-1 sh -lc "[ -f '$target' ]"; then
    docker cp scoreboard.html ctfd-ctfd-1:$target
  fi
 done
for target in \
  /opt/CTFd/CTFd/themes/core/templates/users/private.html \
  /opt/CTFd/CTFd/themes/core-beta/templates/users/private.html
 do
  if docker exec ctfd-ctfd-1 sh -lc "[ -f '$target' ]"; then
    docker cp private.html ctfd-ctfd-1:$target
  fi
 done
docker cp index.html ctfd-ctfd-1:/tmp/index_cuh_latest.html
cat >/tmp/cuh_ui_refresh/force_index.py <<'"'"'PY'"'"'
from pathlib import Path
from CTFd import create_app
from CTFd.cache import clear_pages
from CTFd.models import Pages, db
app = create_app()
with app.app_context():
    page = Pages.query.filter_by(route='index').first()
    if page is None:
        raise SystemExit('index page not found')
    page.content = Path('/tmp/index_cuh_latest.html').read_text(encoding='utf-8')
    db.session.commit()
    clear_pages()
    print('index forced')
PY
docker cp /tmp/cuh_ui_refresh/force_index.py ctfd-ctfd-1:/tmp/force_index.py
docker exec -e PYTHONPATH=/opt/CTFd ctfd-ctfd-1 python3 /tmp/force_index.py
docker restart ctfd-ctfd-1 >/dev/null
echo deployed
