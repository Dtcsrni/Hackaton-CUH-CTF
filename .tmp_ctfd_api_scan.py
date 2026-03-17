from pathlib import Path
root = Path('/opt/CTFd/CTFd/api/v1')
for path in root.rglob('*.py'):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'challenge' in text.lower() and 'attempt' in text.lower():
        print('FILE', path)
        for idx, line in enumerate(text.splitlines(), start=1):
            if 'attempt' in line.lower() or 'solve' in line.lower() or 'fail' in line.lower():
                print(f'{idx}: {line}')
