from pathlib import Path

BASE_DIR = Path('public').resolve()

def read_public_file(requested_path):
    candidate = (BASE_DIR / requested_path).resolve()
    if BASE_DIR not in candidate.parents and candidate != BASE_DIR:
        raise ValueError("ruta fuera de alcance")
    return candidate.read_text(encoding="utf-8")
