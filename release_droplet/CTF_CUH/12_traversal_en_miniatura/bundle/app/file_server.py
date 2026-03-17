from pathlib import Path

BASE_DIR = Path("public")

def read_public_file(requested_path):
    target = BASE_DIR / requested_path
    return target.read_text(encoding="utf-8")
