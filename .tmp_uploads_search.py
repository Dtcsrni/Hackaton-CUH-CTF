from pathlib import Path
for path in Path('/opt/CTFd/CTFd').rglob('*.py'):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'upload_file(' in text and 'utils.uploads' in text:
        print(path)
