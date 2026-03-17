from pathlib import Path
root = Path('/opt/CTFd/CTFd/api/v1/files.py')
text = root.read_text(encoding='utf-8', errors='ignore').splitlines()
for i,line in enumerate(text, start=1):
    if 'class FileList' in line or 'class FileDetail' in line or 'post(' in line or 'route(' in line:
        print(f'{i}: {line}')
