from pathlib import Path
p = Path('/opt/CTFd/CTFd/utils/uploads/__init__.py')
print(p.exists(), p)
if p.exists():
    lines = p.read_text(encoding='utf-8', errors='ignore').splitlines()
    for i,line in enumerate(lines, start=1):
        if 'def upload_file' in line or 'def delete_file' in line or 'location=' in line:
            print(f'{i}: {line}')
    for start in [1,60,120,180]:
        print('---', start)
        for i in range(start-1, min(start+90, len(lines))):
            print(f'{i+1}: {lines[i]}')
