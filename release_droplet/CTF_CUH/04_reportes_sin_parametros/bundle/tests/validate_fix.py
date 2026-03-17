import json
import re
import sys
from pathlib import Path

spec = json.loads(Path("challenge.json").read_text(encoding="utf-8"))
errors = []

for rule in spec.get("checks", []):
    rel = rule["path"]
    target = Path(rel)
    if not target.exists():
        errors.append(f"[missing-file] {rel}")
        continue
    content = target.read_text(encoding="utf-8")
    for token in rule.get("required", []):
        if token not in content:
            errors.append(f"[missing] {rel}: {token}")
    for token in rule.get("forbidden", []):
        if token in content:
            errors.append(f"[forbidden] {rel}: {token}")
    for pattern in rule.get("required_regex", []):
        if re.search(pattern, content, re.MULTILINE) is None:
            errors.append(f"[missing-regex] {rel}: {pattern}")
    for pattern in rule.get("forbidden_regex", []):
        if re.search(pattern, content, re.MULTILINE):
            errors.append(f"[forbidden-regex] {rel}: {pattern}")

if errors:
    print("VALIDACION FALLIDA")
    for item in errors:
        print(item)
    sys.exit(1)
print(spec["flag"])
