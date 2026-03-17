#!/usr/bin/env bash
set -euo pipefail
BASE=/tmp/cuh_first_blood
CONTAINER=ctfd-ctfd-1

docker exec "$CONTAINER" mkdir -p /opt/CTFd/CTFd/plugins/first_blood_bonus
docker cp "$BASE/plugin/__init__.py" "$CONTAINER:/opt/CTFd/CTFd/plugins/first_blood_bonus/__init__.py"
for target in \
  /opt/CTFd/CTFd/themes/core/templates/challenges.html \
  /opt/CTFd/CTFd/themes/core-beta/templates/challenges.html
 do
  if docker exec "$CONTAINER" sh -lc "[ -f '$target' ]"; then
    docker cp "$BASE/templates/challenges.html" "$CONTAINER:$target"
  fi
 done
docker restart "$CONTAINER" >/dev/null
echo deployed
