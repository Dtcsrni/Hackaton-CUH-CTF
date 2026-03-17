from pathlib import Path
p = Path('/opt/cuh-ctf/scripts/registrar_bruteforce_via_internal.sh')
text = p.read_text(encoding='utf-8')
text = text.replace("'attachment':'/opt/cuh-ctf/challenges/formulario_de_acceso/bruteforce_materiales.zip'", "'attachment':'/tmp/bruteforce_materiales.zip'")
needle = 'docker cp "$WORKDIR/sync.py" "$CTFD_CONTAINER:/tmp/sync.py"'
insert = 'docker cp "$WORKDIR/files/bruteforce_materiales.zip" "$CTFD_CONTAINER:/tmp/bruteforce_materiales.zip"\n' + needle
if 'docker cp "$WORKDIR/files/bruteforce_materiales.zip" "$CTFD_CONTAINER:/tmp/bruteforce_materiales.zip"' not in text:
    text = text.replace(needle, insert)
p.write_text(text, encoding='utf-8')
print('patched registrar_bruteforce_via_internal.sh')
