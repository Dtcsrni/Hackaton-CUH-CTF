#!/usr/bin/env bash
set -euo pipefail

# Fix: MutationObserver infinite loop freezing the challenges page
# Copies the patched challenges.html to the CTFd container and restarts

REMOTE_HOST=${REMOTE_HOST:-45.55.49.111}
REMOTE_USER=${REMOTE_USER:-root}
SSH_KEY=${SSH_KEY:-C:\\Users\\evega\\.ssh\\codex_ctfd_cuh}
CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}

LOCAL_FILE="O:\\Descargas\\hackaton\\refresh_assets\\templates\\challenges.html"

echo "==> Uploading patched challenges.html to remote host..."
scp -i "$SSH_KEY" -o StrictHostKeyChecking=no "$LOCAL_FILE" "${REMOTE_USER}@${REMOTE_HOST}:/tmp/challenges_fixed.html"

echo "==> Copying into CTFd container themes..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "${REMOTE_USER}@${REMOTE_HOST}" bash -s <<'REMOTE'
CTFD_CONTAINER=ctfd-ctfd-1
for target in \
  /opt/CTFd/CTFd/themes/core/templates/challenges.html \
  /opt/CTFd/CTFd/themes/core-beta/templates/challenges.html
do
  if docker exec "$CTFD_CONTAINER" sh -lc "[ -f '$target' ]"; then
    docker cp /tmp/challenges_fixed.html "$CTFD_CONTAINER:$target"
    echo "  copied to $target"
  else
    echo "  skipped $target (not found)"
  fi
done
echo "==> Restarting CTFd..."
docker restart "$CTFD_CONTAINER" > /dev/null
echo "==> Done. CTFd restarted."
REMOTE

echo "==> Deploy complete. Refresh https://45.55.49.111/challenges to verify."
