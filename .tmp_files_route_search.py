from pathlib import Path
for path in Path('/opt/CTFd/CTFd').rglob('*.py'):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'url_for("views.files"' in text or 'route("/files/' in text or 'def files(' in text:
        print(path)
