from pathlib import Path
for path in Path('/opt/CTFd/CTFd').rglob('*.py'):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if '/files/' in text and 'route' in text:
        print('FILE', path)
        for idx,line in enumerate(text.splitlines(), start=1):
            if '/files/' in line or 'views.files' in line or 'def files' in line:
                print(f'{idx}: {line}')
