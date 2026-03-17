import json
import sys
from pathlib import Path

spec = json.loads(Path("challenge.json").read_text(encoding="utf-8"))
target = Path(spec["answer_file"])
if not target.exists():
    print(f"Falta el archivo {target}")
    sys.exit(1)
current = target.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
expected = "\n".join(spec["expected_lines"]).strip()
if current != expected:
    print("VALIDACION FALLIDA")
    print(current)
    sys.exit(1)
print(spec["flag"])
