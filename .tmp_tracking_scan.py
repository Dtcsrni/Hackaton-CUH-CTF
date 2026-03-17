from pathlib import Path
for path in Path('/opt/CTFd/CTFd').rglob('*.py'):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'Tracking(' in text or 'class' in text and 'Tracking' in text:
        for idx,line in enumerate(text.splitlines(), start=1):
            if 'Tracking(' in line or 'Tracking.' in line or 'class ' in line and 'Tracking' in line:
                print(f'{path}:{idx}: {line.strip()}')
