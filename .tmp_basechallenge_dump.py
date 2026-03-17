from pathlib import Path
p = Path('/opt/CTFd/CTFd/plugins/challenges/__init__.py')
lines = p.read_text(encoding='utf-8', errors='ignore').splitlines()
for start in [55,180,190,243]:
    print('---', start)
    for i in range(start-1, min(start+90, len(lines))):
        print(f'{i+1}: {lines[i]}')
