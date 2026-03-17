from pathlib import Path
for path in Path('/opt/CTFd/CTFd').rglob('*.py'):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'def authed' in text:
        print(path)
        for idx,line in enumerate(text.splitlines(), start=1):
            if 'def authed' in line:
                print(f'{idx}: {line}')
