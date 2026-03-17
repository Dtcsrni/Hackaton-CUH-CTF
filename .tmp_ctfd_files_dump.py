from pathlib import Path
root = Path('/opt/CTFd/CTFd/api/v1/files.py')
text = root.read_text(encoding='utf-8', errors='ignore').splitlines()
for start in [1,90,110,150]:
    print('---', start)
    for i in range(start-1, min(start+90, len(text))):
        print(f'{i+1}: {text[i]}')
