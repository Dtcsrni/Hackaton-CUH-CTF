from pathlib import Path
from uuid import uuid4

PRIVATE_UPLOAD_DIR = Path("private/uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "pdf"}
MAX_BYTES = 2 * 1024 * 1024

def store_upload(upload):
    original_name = upload.filename
    extension = original_name.rsplit(".", 1)[-1].lower()
    size = len(upload.read())
    upload.seek(0)
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("extension no permitida")
    if size > MAX_BYTES:
        raise ValueError("archivo demasiado grande")
    server_name = f"{uuid4().hex}.{extension}"
    target = PRIVATE_UPLOAD_DIR / server_name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(upload.read())
    return target
