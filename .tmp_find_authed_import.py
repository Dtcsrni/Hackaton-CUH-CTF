from pathlib import Path
for path in Path('/opt/CTFd/CTFd').rglob('*.py'):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'from CTFd.utils.user import' in text or 'import authed' in text:
        for idx,line in enumerate(text.splitlines(), start=1):
            if 'authed' in line and 'import' in line:
                print(f'{path}:{idx}: {line.strip()}')
