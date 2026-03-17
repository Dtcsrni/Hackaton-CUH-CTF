#!/usr/bin/env bash
set -euo pipefail
BASE=/opt/cuh-ctf
CHALLENGES=$BASE/challenges
SCRIPTS=$BASE/scripts
mkdir -p "$CHALLENGES/acceso_por_defecto" "$CHALLENGES/formulario_de_acceso/materiales" "$SCRIPTS"

cat > "$CHALLENGES/acceso_por_defecto/server_basic_auth.py" <<'PY'
#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import base64
HOST='0.0.0.0'
PORT=8090
VALID_USER='operador'
VALID_PASS='laboratorio'
FLAG='CUH{la_fuerza_bruta_tambien_es_contexto}'
REALM='CUH Lab Basic Auth'
class Handler(BaseHTTPRequestHandler):
    server_version='CUHBasicAuth/1.0'
    def _unauth(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', f'Basic realm="{REALM}"')
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'Acceso restringido al laboratorio.\n')
    def do_GET(self):
        if self.path not in ('/','/panel','/panel/'):
            self.send_response(404); self.end_headers(); return
        auth=self.headers.get('Authorization','')
        if not auth.startswith('Basic '):
            return self._unauth()
        try:
            raw=base64.b64decode(auth.split(' ',1)[1]).decode('utf-8')
            user,password=raw.split(':',1)
        except Exception:
            return self._unauth()
        if user!=VALID_USER or password!=VALID_PASS:
            return self._unauth()
        self.send_response(200)
        self.send_header('Content-Type','text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(f'Panel de laboratorio activo\nflag={FLAG}\n'.encode())
    def log_message(self, *args):
        return
if __name__=='__main__':
    httpd=ThreadingHTTPServer((HOST,PORT),Handler)
    print(f'[cuh-basic-auth] listening on {HOST}:{PORT}')
    httpd.serve_forever()
PY
chmod +x "$CHALLENGES/acceso_por_defecto/server_basic_auth.py"

cat > "$CHALLENGES/acceso_por_defecto/README_ORGANIZADOR.md" <<'EOF'
# Acceso por defecto

Reto de fuerza bruta controlada con autenticación HTTP Basic.

- URL: `http://45.55.49.111:8090/panel`
- Usuario válido: `operador`
- Objetivo didáctico: identificar Basic Auth y usar `hydra` con el módulo correcto en un entorno autorizado.
EOF

cat > "$CHALLENGES/acceso_por_defecto/DATOS_CTFD.md" <<'EOF'
Name: Acceso por defecto
Category: Cracking
Value: 260
Type: standard
State: visible
Description:
Existe un panel HTTP de laboratorio en `http://45.55.49.111:8090/panel` dentro de este entorno académico controlado y autorizado. La autenticación es débil y suficiente para practicar fuerza bruta con herramientas estándar de Kali Linux. Antes de automatizar, identifica qué tipo de autenticación usa el servicio y luego prueba una lista razonable de contraseñas en el endpoint correcto.
Flag: CUH{la_fuerza_bruta_tambien_es_contexto}
Hints:
- Primero identifica si el servicio usa Basic Auth o formulario.
- Si el usuario ya está definido, concentra la prueba en la contraseña.
- Hydra puede resolver esto con el módulo HTTP adecuado.
EOF

cat > "$CHALLENGES/acceso_por_defecto/verificacion_local.md" <<'EOF'
# Verificación local
- `curl -i http://127.0.0.1:8090/panel`
- `curl -i -u operador:laboratorio http://127.0.0.1:8090/panel`
- `hydra -l operador -P claves.txt 45.55.49.111 http-get /panel`
EOF

cat > "$CHALLENGES/acceso_por_defecto/systemd_service_preview.txt" <<'EOF'
[Unit]
Description=CUH Basic Auth challenge
After=network.target

[Service]
User=codexdeploy
WorkingDirectory=/opt/cuh-ctf/challenges/acceso_por_defecto
ExecStart=/usr/bin/python3 /opt/cuh-ctf/challenges/acceso_por_defecto/server_basic_auth.py
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
EOF

cat > /tmp/cuh-basic-auth.service <<'EOF'
[Unit]
Description=CUH Basic Auth challenge
After=network.target

[Service]
User=codexdeploy
WorkingDirectory=/opt/cuh-ctf/challenges/acceso_por_defecto
ExecStart=/usr/bin/python3 /opt/cuh-ctf/challenges/acceso_por_defecto/server_basic_auth.py
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
EOF
printf 'codex2026\n' | sudo -S -p '' cp /tmp/cuh-basic-auth.service /etc/systemd/system/cuh-basic-auth.service

cat > "$CHALLENGES/formulario_de_acceso/server_form_login.py" <<'PY'
#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
HOST='0.0.0.0'
PORT=8091
VALID_USER='analista'
VALID_PASS='cuh2026'
FLAG='CUH{hydra_tambien_necesita_precision}'
FAIL='Credenciales invalidas'
HTML = """<!doctype html><html><head><meta charset='utf-8'><title>Formulario de acceso</title></head><body><h1>Ingreso de laboratorio</h1><p>Ruta interna para personal autorizado.</p><form method='post' action='/login'><label>Usuario <input name='username'></label><br><label>Clave <input name='password' type='password'></label><br><button type='submit'>Entrar</button></form></body></html>"""
class Handler(BaseHTTPRequestHandler):
    server_version='CUHFormLogin/1.0'
    def _send(self, body):
        self.send_response(200)
        self.send_header('Content-Type','text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(body.encode())
    def do_GET(self):
        if self.path not in ('/','/login'):
            self.send_response(404); self.end_headers(); return
        self._send(HTML)
    def do_POST(self):
        if self.path != '/login':
            self.send_response(404); self.end_headers(); return
        length=int(self.headers.get('Content-Length','0'))
        params=parse_qs(self.rfile.read(length).decode('utf-8',errors='ignore'))
        username=params.get('username',[''])[0]
        password=params.get('password',[''])[0]
        if username==VALID_USER and password==VALID_PASS:
            self._send(f"<html><body><h1>Acceso concedido</h1><p>flag={FLAG}</p></body></html>")
        else:
            self._send(f"<html><body><h1>{FAIL}</h1><p>Intenta de nuevo.</p></body></html>")
    def log_message(self, *args):
        return
if __name__=='__main__':
    httpd=ThreadingHTTPServer((HOST,PORT),Handler)
    print(f'[cuh-form-login] listening on {HOST}:{PORT}')
    httpd.serve_forever()
PY
chmod +x "$CHALLENGES/formulario_de_acceso/server_form_login.py"

cat > "$CHALLENGES/formulario_de_acceso/materiales/README.txt" <<'EOF'
Material auxiliar para el reto Formulario de acceso.
El usuario válido del laboratorio es analista.
La contraseña se encuentra dentro de un conjunto pequeño de candidatos deliberadamente débiles para práctica controlada.
EOF
cat > "$CHALLENGES/formulario_de_acceso/materiales/usuario.txt" <<'EOF'
analista
EOF
cat > "$CHALLENGES/formulario_de_acceso/materiales/claves.txt" <<'EOF'
laboratorio
analisis
cuh2026
password
welcome
EOF
(cd "$CHALLENGES/formulario_de_acceso" && rm -f bruteforce_materiales.zip && zip -rq bruteforce_materiales.zip materiales)

cat > "$CHALLENGES/formulario_de_acceso/README_ORGANIZADOR.md" <<'EOF'
# Formulario de acceso

Reto de fuerza bruta controlada contra formulario POST.

- URL: `http://45.55.49.111:8091/`
- Ruta de login: `/login`
- Usuario válido: `analista`
- Objetivo didáctico: identificar parámetros y cadena de fallo para `hydra http-post-form`.
EOF

cat > "$CHALLENGES/formulario_de_acceso/DATOS_CTFD.md" <<'EOF'
Name: Formulario de acceso
Category: Cracking
Value: 320
Type: standard
State: visible
Description:
Se ha publicado un formulario de login de laboratorio en `http://45.55.49.111:8091/` dentro de este entorno académico controlado y autorizado. El material adjunto contiene una pista operativa suficiente para acotar la prueba. Antes de automatizar, revisa el formulario, identifica los nombres reales de los campos y determina cuál es la cadena de error que devuelve el sitio cuando el acceso falla.
Flag: CUH{hydra_tambien_necesita_precision}
Hints:
- No uses el módulo de Basic Auth: aquí hay un formulario POST.
- Necesitas usuario, parámetros y cadena de fallo correctos.
- Una wordlist pequeña es suficiente en este laboratorio.
EOF

cat > "$CHALLENGES/formulario_de_acceso/verificacion_local.md" <<'EOF'
# Verificación local
- `curl -s http://127.0.0.1:8091/`
- `curl -s -d 'username=analista&password=cuh2026' http://127.0.0.1:8091/login`
- `hydra -l analista -P claves.txt 45.55.49.111 http-post-form "/login:username=^USER^&password=^PASS^:Credenciales invalidas"`
EOF

cat > "$CHALLENGES/formulario_de_acceso/systemd_service_preview.txt" <<'EOF'
[Unit]
Description=CUH Form Login challenge
After=network.target

[Service]
User=codexdeploy
WorkingDirectory=/opt/cuh-ctf/challenges/formulario_de_acceso
ExecStart=/usr/bin/python3 /opt/cuh-ctf/challenges/formulario_de_acceso/server_form_login.py
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
EOF

cat > /tmp/cuh-form-login.service <<'EOF'
[Unit]
Description=CUH Form Login challenge
After=network.target

[Service]
User=codexdeploy
WorkingDirectory=/opt/cuh-ctf/challenges/formulario_de_acceso
ExecStart=/usr/bin/python3 /opt/cuh-ctf/challenges/formulario_de_acceso/server_form_login.py
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
EOF
printf 'codex2026\n' | sudo -S -p '' cp /tmp/cuh-form-login.service /etc/systemd/system/cuh-form-login.service
printf 'codex2026\n' | sudo -S -p '' systemctl daemon-reload
printf 'codex2026\n' | sudo -S -p '' systemctl enable --now cuh-basic-auth.service cuh-form-login.service
printf 'codex2026\n' | sudo -S -p '' ufw allow 8090/tcp >/dev/null || true
printf 'codex2026\n' | sudo -S -p '' ufw allow 8091/tcp >/dev/null || true

cat > "$SCRIPTS/validar_acceso_por_defecto.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
systemctl is-active --quiet cuh-basic-auth.service
ss -ltn | grep -q ':8090 '
curl -s -o /tmp/cuh_unauth.txt -w '%{http_code}' http://127.0.0.1:8090/panel | grep -q '^401$'
curl -s -u operador:laboratorio http://127.0.0.1:8090/panel | grep -q 'CUH{la_fuerza_bruta_tambien_es_contexto}'
echo OK
EOF
chmod +x "$SCRIPTS/validar_acceso_por_defecto.sh"

cat > "$SCRIPTS/validar_formulario_de_acceso.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
systemctl is-active --quiet cuh-form-login.service
ss -ltn | grep -q ':8091 '
curl -s http://127.0.0.1:8091/ | grep -q "name='username'"
curl -s -d 'username=analista&password=cuh2026' http://127.0.0.1:8091/login | grep -q 'CUH{hydra_tambien_necesita_precision}'
unzip -l /opt/cuh-ctf/challenges/formulario_de_acceso/bruteforce_materiales.zip | grep -q 'materiales/claves.txt'
echo OK
EOF
chmod +x "$SCRIPTS/validar_formulario_de_acceso.sh"

python3 - <<'PY'
from pathlib import Path
p=Path('/opt/cuh-ctf/scripts/validar_todo_cuh_ctf.sh')
text=p.read_text(encoding='utf-8')
for line in ['/opt/cuh-ctf/scripts/validar_acceso_por_defecto.sh','/opt/cuh-ctf/scripts/validar_formulario_de_acceso.sh']:
    if line not in text:
        text = text.rstrip() + '\n' + line + '\n'
p.write_text(text, encoding='utf-8')
PY

python3 - <<'PY'
from pathlib import Path
p=Path('/opt/cuh-ctf/scripts/actualizar_paginas_ctfd.sh')
text=p.read_text(encoding='utf-8')
if 'bruteforce-lab' not in text:
    text=text.replace('for page in index reglas faq cronograma panel-interno inicio-rapido guia-herramientas inventario-lab analisis-archivos credenciales-legado formularios-lab jwt-lab frontend-lab cookies-lab cracking-lab laboratorio-visual mapa-retos; do','for page in index reglas faq cronograma panel-interno inicio-rapido guia-herramientas inventario-lab analisis-archivos credenciales-legado formularios-lab jwt-lab frontend-lab cookies-lab cracking-lab laboratorio-visual mapa-retos bruteforce-lab; do')
    text=text.replace("'cracking-lab': {'title': 'Notas internas sobre cracking', 'hidden': True, 'auth_required': False},","'cracking-lab': {'title': 'Notas internas sobre cracking', 'hidden': True, 'auth_required': False},\n  'bruteforce-lab': {'title': 'Notas internas sobre fuerza bruta', 'hidden': True, 'auth_required': False},")
    text=text.replace("'Cookie firmada debil': ('cookies-lab', 'Notas internas sobre cookies'),","'Cookie firmada debil': ('cookies-lab', 'Notas internas sobre cookies'),\n  'Acceso por defecto': ('bruteforce-lab', 'Notas internas sobre fuerza bruta'),\n  'Formulario de acceso': ('bruteforce-lab', 'Notas internas sobre fuerza bruta'),")
p.write_text(text, encoding='utf-8')
PY

cat > "$SCRIPTS/registrar_bruteforce_via_internal.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}
WORKDIR=/tmp/cuh_ctfd_bruteforce
mkdir -p "$WORKDIR/files"
trap 'rm -rf "$WORKDIR"' EXIT
cp "/opt/cuh-ctf/challenges/formulario_de_acceso/bruteforce_materiales.zip" "$WORKDIR/files/bruteforce_materiales.zip"
cat > "$WORKDIR/sync.py" <<'PY'
from CTFd import create_app
from CTFd.models import db, Challenges, Flags, Hints
from CTFd.utils.uploads import upload_file, delete_file, ChallengeFiles
from werkzeug.datastructures import FileStorage
SPECS=[
 {'name':'Acceso por defecto','category':'Cracking','value':260,'type':'standard','state':'visible','description':'Existe un panel HTTP de laboratorio en `http://45.55.49.111:8090/panel` dentro de este entorno académico controlado y autorizado. La autenticación es débil y suficiente para practicar fuerza bruta con herramientas estándar de Kali Linux. Antes de automatizar, identifica qué tipo de autenticación usa el servicio y luego prueba una lista razonable de contraseñas en el endpoint correcto.','flag':'CUH{la_fuerza_bruta_tambien_es_contexto}','hints':['Primero identifica si el servicio usa Basic Auth o formulario.','Si el usuario ya está definido, concentra la prueba en la contraseña.','Hydra puede resolver esto con el módulo HTTP adecuado.'],'attachment':None},
 {'name':'Formulario de acceso','category':'Cracking','value':320,'type':'standard','state':'visible','description':'Se ha publicado un formulario de login de laboratorio en `http://45.55.49.111:8091/` dentro de este entorno académico controlado y autorizado. El material adjunto contiene una pista operativa suficiente para acotar la prueba. Antes de automatizar, revisa el formulario, identifica los nombres reales de los campos y determina cuál es la cadena de error que devuelve el sitio cuando el acceso falla.','flag':'CUH{hydra_tambien_necesita_precision}','hints':['No uses el módulo de Basic Auth: aquí hay un formulario POST.','Necesitas usuario, parámetros y cadena de fallo correctos.','Una wordlist pequeña es suficiente en este laboratorio.'],'attachment':'/opt/cuh-ctf/challenges/formulario_de_acceso/bruteforce_materiales.zip'}]
app=create_app()
with app.app_context():
  for spec in SPECS:
    challenge=Challenges.query.filter_by(name=spec['name']).first()
    if challenge is None:
      challenge=Challenges(name=spec['name'],category=spec['category'],value=spec['value'],description=spec['description'],type=spec['type'],state=spec['state'])
      db.session.add(challenge); db.session.flush()
    else:
      challenge.category=spec['category']; challenge.value=spec['value']; challenge.description=spec['description']; challenge.type=spec['type']; challenge.state=spec['state']
    Flags.query.filter_by(challenge_id=challenge.id).delete()
    for h in Hints.query.filter_by(challenge_id=challenge.id).all(): db.session.delete(h)
    for cf in ChallengeFiles.query.filter_by(challenge_id=challenge.id).all():
      try: delete_file(cf.location)
      except Exception: pass
      db.session.delete(cf)
    db.session.flush()
    db.session.add(Flags(challenge_id=challenge.id,type='static',content=spec['flag'],data='case_insensitive'))
    for hint in spec['hints']: db.session.add(Hints(challenge_id=challenge.id,content=hint,cost=0))
    if spec['attachment']:
      with open(spec['attachment'],'rb') as fp:
        fs=FileStorage(stream=fp,filename=spec['attachment'].split('/')[-1])
        loc=upload_file(file_obj=fs, challenge_id=challenge.id)
        db.session.add(ChallengeFiles(type='challenge',location=loc,challenge_id=challenge.id,page_id=None))
    db.session.commit()
    print(f"{challenge.id}:{challenge.name}:ok")
PY
docker cp "$WORKDIR/sync.py" "$CTFD_CONTAINER:/tmp/sync.py"
docker exec -e PYTHONPATH=/opt/CTFd "$CTFD_CONTAINER" python3 /tmp/sync.py
EOF
chmod +x "$SCRIPTS/registrar_bruteforce_via_internal.sh"

python3 - <<'PY'
from pathlib import Path
p=Path('/opt/cuh-ctf/scripts/registrar_ctfd_via_internal.sh')
text=p.read_text(encoding='utf-8')
line='bash /opt/cuh-ctf/scripts/registrar_bruteforce_via_internal.sh\n'
if line not in text:
    text=text.rstrip()+'\n'+line
p.write_text(text, encoding='utf-8')
PY

bash "$SCRIPTS/actualizar_paginas_ctfd.sh"
bash "$SCRIPTS/registrar_bruteforce_via_internal.sh"
EOF
