from pathlib import Path

PUBLIC_DIR = Path("public/uploads")

def store_upload(upload):
    filename = upload.filename
    target = PUBLIC_DIR / filename
    target.write_bytes(upload.read())
    return target
