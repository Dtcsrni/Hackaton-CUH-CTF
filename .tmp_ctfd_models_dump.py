from pathlib import Path
root = Path('/opt/CTFd/CTFd/models/__init__.py')
text = root.read_text(encoding='utf-8', errors='ignore').splitlines()
for start in [180,236,925,957,1006]:
    print('---', start)
    for i in range(start-1, min(start+70, len(text))):
        print(f'{i+1}: {text[i]}')
