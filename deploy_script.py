import subprocess
from pathlib import Path

KEY = Path(r"C:\Users\evega\.ssh\codex_ctfd_cuh")
REMOTE = "codexdeploy@45.55.49.111"
LOCAL_FILE = r"o:\Descargas\hackaton\refresh_assets\scoreboard.html"

def run(cmd):
    print("Running:", " ".join(cmd))
    res = subprocess.run(cmd)
    if res.returncode != 0:
        raise Exception(f"Command failed with {res.returncode}")

try:
    print("Uploading...")
    run(["scp", "-i", str(KEY), "-o", "StrictHostKeyChecking=no", LOCAL_FILE, f"{REMOTE}:/tmp/scoreboard_fixed.html"])
    
    print("Copying and restarting...")
    remote_cmd = """
    CTFD_CONTAINER=ctfd-ctfd-1
    for target in /opt/CTFd/CTFd/themes/core/templates/scoreboard.html /opt/CTFd/CTFd/themes/core-beta/templates/scoreboard.html
    do
      if docker exec "$CTFD_CONTAINER" sh -lc "[ -f '$target' ]"; then
        docker cp /tmp/scoreboard_fixed.html "$CTFD_CONTAINER:$target"
        echo "  copied to $target"
      fi
    done
    docker restart "$CTFD_CONTAINER"
    """
    run(["ssh", "-i", str(KEY), "-o", "StrictHostKeyChecking=no", REMOTE, remote_cmd])
    print("Done")
except Exception as e:
    print("Error:", e)
