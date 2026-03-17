from pathlib import Path
p = Path('/opt/CTFd/CTFd/api/v1/challenges.py')
lines = p.read_text(encoding='utf-8', errors='ignore').splitlines()
for i in range(608-1, min(980, len(lines))):
    print(f'{i+1}: {lines[i]}')
