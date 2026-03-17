from pathlib import Path
p = Path('/opt/CTFd/CTFd/views.py')
lines = p.read_text(encoding='utf-8', errors='ignore').splitlines()
for i in range(388, 430):
    print(f'{i+1}: {lines[i]}')
