from pathlib import Path
import re
p = Path('/opt/cuh-ctf/docs/FAQ_PARTICIPANTES_CTFD.html')
text = p.read_text(encoding='utf-8')
text = re.sub(r'<span class=.*?cuh-code.*?>', '<span class="cuh-code">', text)
p.write_text(text, encoding='utf-8')
