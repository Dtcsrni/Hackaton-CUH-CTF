from pathlib import Path
import os
root = Path('/opt/CTFd/CTFd')
needles = ['class BaseChallenge', 'def attempt', 'def solve', '/attempt', 'class Awards', 'class Solves', 'class Fails', 'class Hints', 'class Tracking']
for path in root.rglob('*.py'):
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    for idx, line in enumerate(text.splitlines(), start=1):
        for needle in needles:
            if needle in line:
                print(f'{path}:{idx}: {line.strip()}')
