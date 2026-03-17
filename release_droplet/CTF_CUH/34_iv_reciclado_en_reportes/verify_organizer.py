from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

root = Path(__file__).resolve().parent
bundle = root / "bundle"
solution = root / "solutions"
validator_name = "tests/validate_fix.py"
expected_flag = "CUH{iv_reciclado_detectado_en_reportes}"

with TemporaryDirectory() as tmp:
    workspace = Path(tmp) / "workspace"
    shutil.copytree(bundle, workspace)
    for path in solution.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(solution)
        target = workspace / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    proc = subprocess.run(
        [sys.executable, validator_name],
        cwd=workspace,
        text=True,
        capture_output=True,
        check=False,
    )
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)
    if expected_flag not in proc.stdout:
        print("La validación no devolvió la flag esperada.")
        raise SystemExit(1)
print("OK")
