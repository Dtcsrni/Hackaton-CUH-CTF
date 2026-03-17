from pathlib import Path
p = Path('/opt/CTFd/CTFd/utils/user/__init__.py')
lines = p.read_text(encoding='utf-8', errors='ignore').splitlines()
for i in range(120, 190):
    print(f'{i+1}: {lines[i]}')
