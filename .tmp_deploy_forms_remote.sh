#!/usr/bin/env bash
set -euo pipefail
BASE=/opt/cuh-ctf
CH=$BASE/challenges
DOCS=$BASE/docs
PAGES=$DOCS/pages
SCR=$BASE/scripts
ART=$BASE/artifacts
API=$ART/ctfd_api_payloads
CLI=$ART/ctfcli
BACK=$ART/backups/$(date +%Y%m%d%H%M%S)_form_challenges
mkdir -p "$BACK" "$CH/registro_sin_servidor" "$CH/encuesta_confiada" "$PAGES" "$API" "$CLI/registro_sin_servidor" "$CLI/encuesta_confiada"
backup(){ [ -f "$1" ] && mkdir -p "$BACK$(dirname "$1")" && cp "$1" "$BACK$1" || true; }
write(){ local f="$1"; backup "$f"; mkdir -p "$(dirname "$f")"; cat > "$f"; }
sudowrite(){ local f="$1"; local t; t=$(mktemp); cat > "$t"; printf 'codex2026\n' | sudo -S -p '' mkdir -p "$(dirname "$f")"; [ -f "$f" ] && mkdir -p "$BACK$(dirname "$f")" && printf 'codex2026\n' | sudo -S -p '' cp "$f" "$BACK$f" || true; printf 'codex2026\n' | sudo -S -p '' cp "$t" "$f"; rm -f "$t"; }
write "$CH/registro_sin_servidor/server_registro_sin_servidor.py" <<'EOF'
#!/usr/bin/env python3
import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
HOST='0.0.0.0'
PORT=8084
FLAG='CUH{el_servidor_tambien_debe_validar}'
INDEX="""<!doctype html><html lang=\"es\"><head><meta charset=\"utf-8\"><title>Pre-registro de laboratorio CUH</title><style>body{font-family:Arial,sans-serif;margin:2rem auto;max-width:780px;line-height:1.5;color:#1c1c1c}form{border:1px solid #d0d0d0;padding:1.2rem;border-radius:8px;background:#fafafa}label{display:block;margin-top:.8rem;font-weight:bold}input,select,button{width:100%;padding:.6rem;margin-top:.25rem;font-size:1rem}.help{color:#555;font-size:.95rem}code{background:#f0f0f0;padding:.1rem .3rem}</style></head><body><h1>Pre-registro de laboratorio CUH</h1><p>Este formulario de laboratorio se utiliza solo dentro del entorno academico controlado del hackathon.</p><p class=\"help\">La interfaz del navegador aplica restricciones basicas para participantes. El formulario se envia a <code>/registro</code>.</p><form method=\"post\" action=\"/registro\" onsubmit=\"return validar();\"><label for=\"nombre\">Nombre</label><input id=\"nombre\" name=\"nombre\" required minlength=\"4\" maxlength=\"50\" placeholder=\"Nombre completo\"><label for=\"correo\">Correo institucional</label><input id=\"correo\" name=\"correo\" type=\"email\" required pattern=\".+@alumnos\\.cuh\\.edu\\.mx\" placeholder=\"usuario@alumnos.cuh.edu.mx\"><label for=\"matricula\">Matricula</label><input id=\"matricula\" name=\"matricula\" required pattern=\"[0-9]{8}\" maxlength=\"8\" placeholder=\"20261234\"><label for=\"area\">Area solicitada</label><select id=\"area\" name=\"area\"><option value=\"participantes\">Participantes</option><option value=\"soporte\">Soporte</option></select><input type=\"hidden\" name=\"perfil\" value=\"estudiante\"><input type=\"hidden\" name=\"modo\" value=\"publico\"><button type=\"submit\">Enviar pre-registro</button></form><script>function validar(){const correo=document.getElementById('correo').value;if(!correo.endsWith('@alumnos.cuh.edu.mx')){alert('Solo se aceptan correos de alumnos en esta vista publica.');return false;}return true;}</script></body></html>"""
class H(BaseHTTPRequestHandler):
    def s(self,code,body,ctype='text/html; charset=utf-8'):
        b=body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type',ctype)
        self.send_header('Content-Length',str(len(b)))
        self.end_headers()
        if self.command!='HEAD':
            self.wfile.write(b)
    def do_GET(self):
        if self.path!='/':
            return self.s(404,'<h1>404</h1>')
        self.s(200,INDEX)
    def do_POST(self):
        if self.path!='/registro':
            return self.s(404,'<h1>404</h1>')
        n=int(self.headers.get('Content-Length','0'))
        d=parse_qs(self.rfile.read(n).decode('utf-8'), keep_blank_values=True)
        nombre=html.escape(d.get('nombre',[''])[0])
        perfil=d.get('perfil',['estudiante'])[0]
        modo=d.get('modo',['publico'])[0]
        area=d.get('area',['participantes'])[0]
        if perfil=='coordinacion' and modo=='interno':
            return self.s(200,f'<!doctype html><html lang="es"><body><h1>Registro aceptado</h1><p>Se registro correctamente a {nombre or "usuario"} en el entorno interno.</p><p>area={html.escape(area)}</p><p>flag={FLAG}</p></body></html>')
        self.s(200,f'<!doctype html><html lang="es"><body><h1>Solicitud recibida</h1><p>Se registro a {nombre or "usuario"} para revision publica.</p><p class="help">perfil={html.escape(perfil)} modo={html.escape(modo)} area={html.escape(area)}</p></body></html>')
    def log_message(self, fmt, *args):
        print(f'[registro-sin-servidor] {self.address_string()} - {fmt % args}', flush=True)
if __name__=='__main__':
    server=ThreadingHTTPServer((HOST,PORT),H)
    print(f'[*] Servicio de pre-registro escuchando en {HOST}:{PORT}', flush=True)
    server.serve_forever()
EOF
write "$CH/encuesta_confiada/server_encuesta_confiada.py" <<'EOF'
#!/usr/bin/env python3
import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
HOST='0.0.0.0'
PORT=8085
FLAG='CUH{nunca_confies_en_campos_ocultos}'
INDEX="""<!doctype html><html lang=\"es\"><head><meta charset=\"utf-8\"><title>Encuesta de satisfaccion del laboratorio</title><style>body{font-family:Arial,sans-serif;margin:2rem auto;max-width:780px;line-height:1.5;color:#202020}form{border:1px solid #d0d0d0;padding:1.2rem;border-radius:8px;background:#fafafa}label{display:block;margin-top:.7rem;font-weight:bold}input,select,textarea,button{width:100%;padding:.6rem;margin-top:.25rem;font-size:1rem}.help{color:#555;font-size:.95rem}</style></head><body><h1>Encuesta de satisfaccion del laboratorio</h1><p>Esta encuesta se comparte solo para fines de practica dentro del entorno academico autorizado.</p><p class=\"help\">La vista publica envia respuestas a <code>/evaluacion</code> y usa restricciones del lado del navegador.</p><form method=\"post\" action=\"/evaluacion\" onsubmit=\"return validarEncuesta();\"><label for=\"nombre\">Nombre</label><input id=\"nombre\" name=\"nombre\" required minlength=\"4\" maxlength=\"50\"><label for=\"equipo\">Equipo de trabajo</label><select id=\"equipo\" name=\"equipo\"><option value=\"azul\">Azul</option><option value=\"verde\">Verde</option><option value=\"naranja\">Naranja</option></select><label for=\"comentarios\">Comentarios</label><textarea id=\"comentarios\" name=\"comentarios\" minlength=\"10\" maxlength=\"150\" required></textarea><input type=\"hidden\" name=\"estado\" value=\"publico\"><input type=\"hidden\" name=\"revision\" value=\"estandar\"><button type=\"submit\">Enviar encuesta</button></form><script>function validarEncuesta(){const comentarios=document.getElementById('comentarios').value.trim();if(comentarios.length<10){alert('Se requieren al menos 10 caracteres en comentarios.');return false;}return true;}</script></body></html>"""
class H(BaseHTTPRequestHandler):
    def s(self,code,body,ctype='text/html; charset=utf-8'):
        b=body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type',ctype)
        self.send_header('Content-Length',str(len(b)))
        self.end_headers()
        if self.command!='HEAD':
            self.wfile.write(b)
    def do_GET(self):
        if self.path!='/':
            return self.s(404,'<h1>404</h1>')
        self.s(200,INDEX)
    def do_POST(self):
        if self.path!='/evaluacion':
            return self.s(404,'<h1>404</h1>')
        n=int(self.headers.get('Content-Length','0'))
        d=parse_qs(self.rfile.read(n).decode('utf-8'), keep_blank_values=True)
        nombre=html.escape(d.get('nombre',[''])[0])
        equipo=d.get('equipo',['azul'])[0]
        estado=d.get('estado',['publico'])[0]
        revision=d.get('revision',['estandar'])[0]
        if estado=='interno' and revision=='aprobada':
            return self.s(200,f'<!doctype html><html lang="es"><body><h1>Encuesta validada internamente</h1><p>Respuesta registrada para {nombre or "usuario"}.</p><p>equipo={html.escape(equipo)}</p><p>flag={FLAG}</p></body></html>')
        self.s(200,f'<!doctype html><html lang="es"><body><h1>Encuesta registrada</h1><p>Gracias por tu participacion, {nombre or "usuario"}.</p><p class="help">estado={html.escape(estado)} revision={html.escape(revision)} equipo={html.escape(equipo)}</p></body></html>')
    def log_message(self, fmt, *args):
        print(f'[encuesta-confiada] {self.address_string()} - {fmt % args}', flush=True)
if __name__=='__main__':
    server=ThreadingHTTPServer((HOST,PORT),H)
    print(f'[*] Servicio de encuesta escuchando en {HOST}:{PORT}', flush=True)
    server.serve_forever()
EOF
chmod +x "$CH/registro_sin_servidor/server_registro_sin_servidor.py" "$CH/encuesta_confiada/server_encuesta_confiada.py"
write "$CH/registro_sin_servidor/README_ORGANIZADOR.md" <<'EOF'
# Registro sin servidor

## Proposito didactico
Mostrar que un formulario con validaciones del lado del navegador no sustituye validaciones del lado del servidor dentro de un laboratorio academico controlado.
EOF
write "$CH/registro_sin_servidor/DATOS_CTFD.md" <<'EOF'
# Datos para CTFd: Registro sin servidor

## Name
Registro sin servidor

## Category
Web

## Value
230

## Type
standard

## State
visible

## Description
Existe un formulario de pre-registro de laboratorio en `http://45.55.49.111:8084` dentro de este entorno academico controlado y autorizado. La interfaz publica aplica restricciones para participantes, pero tu trabajo es verificar que realmente valida el servidor y no solo el navegador. Observa el formulario, revisa la peticion y reproduce manualmente un envio coherente para obtener la respuesta correcta.

## Flag
`CUH{el_servidor_tambien_debe_validar}`

## Hints
1. No confundas validacion de navegador con validacion de servidor.
2. Revisa que campos se envian realmente al hacer submit.
3. Una peticion manual con `curl` o un proxy local basta para resolverlo.
EOF
write "$CH/registro_sin_servidor/verificacion_local.md" <<'EOF'
# Verificacion local: Registro sin servidor

```bash
curl -fsS http://127.0.0.1:8084/
curl -fsS -X POST http://127.0.0.1:8084/registro \
  -d 'nombre=Prueba&correo=test@alumnos.cuh.edu.mx&matricula=20261234&area=soporte&perfil=coordinacion&modo=interno'
```
EOF
write "$CH/registro_sin_servidor/diagrama_flujo.md" <<'EOF'
# Diagrama de flujo: Registro sin servidor

```mermaid
flowchart LR
  A["Alumno"] --> B["Abrir formulario 8084"]
  B --> C["Inspeccionar HTML y campos enviados"]
  C --> D["Repetir POST a /registro"]
  D --> E["Modificar perfil y modo"]
  E --> F["Respuesta con flag"]
```
EOF
write "$CH/registro_sin_servidor/systemd_service_preview.txt" <<'EOF'
[Unit]
Description=CUH CTF - Registro sin servidor
After=network.target

[Service]
Type=simple
User=codexdeploy
WorkingDirectory=/opt/cuh-ctf/challenges/registro_sin_servidor
ExecStart=/usr/bin/python3 /opt/cuh-ctf/challenges/registro_sin_servidor/server_registro_sin_servidor.py
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
EOF
write "$CH/encuesta_confiada/README_ORGANIZADOR.md" <<'EOF'
# Encuesta confiada

## Proposito didactico
Mostrar por que los campos ocultos y los valores de control del cliente no deben tratarse como fuente confiable cuando el servidor toma decisiones.
EOF
write "$CH/encuesta_confiada/DATOS_CTFD.md" <<'EOF'
# Datos para CTFd: Encuesta confiada

## Name
Encuesta confiada

## Category
Web

## Value
260

## Type
standard

## State
visible

## Description
Hay una encuesta de laboratorio disponible en `http://45.55.49.111:8085` dentro de este entorno academico controlado y autorizado. A simple vista parece una encuesta publica comun, pero la logica real depende de datos que el cliente envia al servidor. Tu objetivo es observar el formulario, identificar que parametros se envian y comprobar si el servidor confia demasiado en ellos.

## Flag
`CUH{nunca_confies_en_campos_ocultos}`

## Hints
1. Un campo oculto sigue siendo un campo controlado por el cliente.
2. El endpoint util no es la pagina inicial sino la ruta que recibe el formulario.
3. Repite la solicitud con valores alternativos y observa la respuesta completa.
EOF
write "$CH/encuesta_confiada/verificacion_local.md" <<'EOF'
# Verificacion local: Encuesta confiada

```bash
curl -fsS http://127.0.0.1:8085/
curl -fsS -X POST http://127.0.0.1:8085/evaluacion \
  -d 'nombre=Prueba&equipo=verde&comentarios=revision+controlada&estado=interno&revision=aprobada'
```
EOF
write "$CH/encuesta_confiada/diagrama_flujo.md" <<'EOF'
# Diagrama de flujo: Encuesta confiada

```mermaid
flowchart LR
  A["Alumno"] --> B["Abrir formulario 8085"]
  B --> C["Inspeccionar HTML y campos ocultos"]
  C --> D["Repetir POST a /evaluacion"]
  D --> E["Modificar estado y revision"]
  E --> F["Respuesta con flag"]
```
EOF
write "$CH/encuesta_confiada/systemd_service_preview.txt" <<'EOF'
[Unit]
Description=CUH CTF - Encuesta confiada
After=network.target

[Service]
Type=simple
User=codexdeploy
WorkingDirectory=/opt/cuh-ctf/challenges/encuesta_confiada
ExecStart=/usr/bin/python3 /opt/cuh-ctf/challenges/encuesta_confiada/server_encuesta_confiada.py
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
EOF
write "$SCR/validar_registro_sin_servidor.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
[ -f /etc/systemd/system/cuh-registro-sin-servidor.service ]
systemctl is-active --quiet cuh-registro-sin-servidor
ss -ltn | grep -q ':8084 '
curl -fsS http://127.0.0.1:8084/ | grep -q '/registro'
curl -fsS -X POST http://127.0.0.1:8084/registro -d 'nombre=Prueba&correo=test@alumnos.cuh.edu.mx&matricula=20261234&area=soporte&perfil=coordinacion&modo=interno' | grep -q 'CUH{el_servidor_tambien_debe_validar}'
echo 'Validacion de Registro sin servidor: OK'
EOF
write "$SCR/validar_encuesta_confiada.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
[ -f /etc/systemd/system/cuh-encuesta-confiada.service ]
systemctl is-active --quiet cuh-encuesta-confiada
ss -ltn | grep -q ':8085 '
curl -fsS http://127.0.0.1:8085/ | grep -q '/evaluacion'
curl -fsS -X POST http://127.0.0.1:8085/evaluacion -d 'nombre=Prueba&equipo=verde&comentarios=revision+controlada&estado=interno&revision=aprobada' | grep -q 'CUH{nunca_confies_en_campos_ocultos}'
echo 'Validacion de Encuesta confiada: OK'
EOF
chmod +x "$SCR/validar_registro_sin_servidor.sh" "$SCR/validar_encuesta_confiada.sh"
backup "$SCR/validar_todo_cuh_ctf.sh"
python3 - <<'PY'
from pathlib import Path
p=Path('/opt/cuh-ctf/scripts/validar_todo_cuh_ctf.sh')
lines=p.read_text().splitlines()
for req in ('/opt/cuh-ctf/scripts/validar_registro_sin_servidor.sh','/opt/cuh-ctf/scripts/validar_encuesta_confiada.sh'):
    if req not in lines:
        lines.append(req)
p.write_text('\n'.join(lines)+'\n')
PY
sudowrite /etc/systemd/system/cuh-registro-sin-servidor.service <<'EOF'
[Unit]
Description=CUH CTF - Registro sin servidor
After=network.target

[Service]
Type=simple
User=codexdeploy
WorkingDirectory=/opt/cuh-ctf/challenges/registro_sin_servidor
ExecStart=/usr/bin/python3 /opt/cuh-ctf/challenges/registro_sin_servidor/server_registro_sin_servidor.py
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
EOF
sudowrite /etc/systemd/system/cuh-encuesta-confiada.service <<'EOF'
[Unit]
Description=CUH CTF - Encuesta confiada
After=network.target

[Service]
Type=simple
User=codexdeploy
WorkingDirectory=/opt/cuh-ctf/challenges/encuesta_confiada
ExecStart=/usr/bin/python3 /opt/cuh-ctf/challenges/encuesta_confiada/server_encuesta_confiada.py
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
EOF
printf 'codex2026\n' | sudo -S -p '' systemctl daemon-reload
printf 'codex2026\n' | sudo -S -p '' systemctl enable --now cuh-registro-sin-servidor.service
printf 'codex2026\n' | sudo -S -p '' systemctl enable --now cuh-encuesta-confiada.service
printf 'codex2026\n' | sudo -S -p '' ufw allow 8084/tcp >/dev/null
printf 'codex2026\n' | sudo -S -p '' ufw allow 8085/tcp >/dev/null
write "$SCR/registrar_formularios_via_internal.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}
WORKDIR=/tmp/cuh_ctfd_forms
mkdir -p "$WORKDIR"
trap 'rm -rf "$WORKDIR"' EXIT
cat > "$WORKDIR/ctfd_sync.py" <<'PY'
from CTFd import create_app
from CTFd.models import db, Challenges, Flags, Hints
SPECS=[
{'name':'Registro sin servidor','category':'Web','value':230,'type':'standard','state':'visible','description':'Existe un formulario de pre-registro de laboratorio en `http://45.55.49.111:8084` dentro de este entorno academico controlado y autorizado. La interfaz publica aplica restricciones para participantes, pero tu trabajo es verificar que realmente valida el servidor y no solo el navegador. Observa el formulario, revisa la peticion y reproduce manualmente un envio coherente para obtener la respuesta correcta.\n\nRecurso interno opcional del laboratorio: [Notas internas sobre formularios](/formularios-lab).','flag':'CUH{el_servidor_tambien_debe_validar}','hints':['No confundas validacion de navegador con validacion de servidor.','Revisa que campos se envian realmente al hacer submit.','Una peticion manual con curl o un proxy local basta para resolverlo.']},
{'name':'Encuesta confiada','category':'Web','value':260,'type':'standard','state':'visible','description':'Hay una encuesta de laboratorio disponible en `http://45.55.49.111:8085` dentro de este entorno academico controlado y autorizado. A simple vista parece una encuesta publica comun, pero la logica real depende de datos que el cliente envia al servidor. Tu objetivo es observar el formulario, identificar que parametros se envian y comprobar si el servidor confia demasiado en ellos.\n\nRecurso interno opcional del laboratorio: [Notas internas sobre formularios](/formularios-lab).','flag':'CUH{nunca_confies_en_campos_ocultos}','hints':['Un campo oculto sigue siendo un campo controlado por el cliente.','El endpoint util no es la pagina inicial sino la ruta que recibe el formulario.','Repite la solicitud con valores alternativos y observa la respuesta completa.']}
]
app=create_app()
with app.app_context():
    for spec in SPECS:
        chal=Challenges.query.filter_by(name=spec['name']).first()
        if chal is None:
            chal=Challenges(); db.session.add(chal)
        chal.name=spec['name']; chal.category=spec['category']; chal.description=spec['description']; chal.value=spec['value']; chal.type=spec['type']; chal.state=spec['state']
        if hasattr(chal,'connection_info'):
            chal.connection_info=''
        db.session.flush()
        Flags.query.filter_by(challenge_id=chal.id).delete(); Hints.query.filter_by(challenge_id=chal.id).delete()
        db.session.add(Flags(challenge_id=chal.id,type='static',content=spec['flag'],data=''))
        for hint_text in spec['hints']:
            db.session.add(Hints(challenge_id=chal.id,type='standard',content=hint_text,cost=0,requirements=None))
        db.session.commit(); print(f'{chal.id}:{chal.name}')
PY
docker cp "$WORKDIR/ctfd_sync.py" "$CTFD_CONTAINER:/tmp/ctfd_sync.py"
docker exec -e PYTHONPATH=/opt/CTFd "$CTFD_CONTAINER" python3 /tmp/ctfd_sync.py
EOF
chmod +x "$SCR/registrar_formularios_via_internal.sh"
backup "$SCR/registrar_ctfd_via_internal.sh"
python3 - <<'PY'
from pathlib import Path
p=Path('/opt/cuh-ctf/scripts/registrar_ctfd_via_internal.sh')
text=p.read_text()
line='bash /opt/cuh-ctf/scripts/registrar_formularios_via_internal.sh\n'
if line not in text:
    hook='bash /opt/cuh-ctf/scripts/registrar_cracking_via_internal.sh\n'
    text=text.replace(hook, hook+line) if hook in text else text+'\n'+line
p.write_text(text)
PY
write "$API/challenge_registro_sin_servidor.json" <<'EOF'
{"name":"Registro sin servidor","category":"Web","value":230,"type":"standard","state":"visible","description":"Existe un formulario de pre-registro de laboratorio en `http://45.55.49.111:8084` dentro de este entorno academico controlado y autorizado. La interfaz publica aplica restricciones para participantes, pero tu trabajo es verificar que realmente valida el servidor y no solo el navegador. Observa el formulario, revisa la peticion y reproduce manualmente un envio coherente para obtener la respuesta correcta.\n\nRecurso interno opcional del laboratorio: [Notas internas sobre formularios](/formularios-lab)."}
EOF
write "$API/flag_registro_sin_servidor.json" <<'EOF'
{"type":"static","content":"CUH{el_servidor_tambien_debe_validar}","data":""}
EOF
write "$API/hints_registro_sin_servidor.json" <<'EOF'
[{"type":"standard","content":"No confundas validacion de navegador con validacion de servidor.","cost":0},{"type":"standard","content":"Revisa que campos se envian realmente al hacer submit.","cost":0},{"type":"standard","content":"Una peticion manual con curl o un proxy local basta para resolverlo.","cost":0}]
EOF
write "$API/challenge_encuesta_confiada.json" <<'EOF'
{"name":"Encuesta confiada","category":"Web","value":260,"type":"standard","state":"visible","description":"Hay una encuesta de laboratorio disponible en `http://45.55.49.111:8085` dentro de este entorno academico controlado y autorizado. A simple vista parece una encuesta publica comun, pero la logica real depende de datos que el cliente envia al servidor. Tu objetivo es observar el formulario, identificar que parametros se envian y comprobar si el servidor confia demasiado en ellos.\n\nRecurso interno opcional del laboratorio: [Notas internas sobre formularios](/formularios-lab)."}
EOF
write "$API/flag_encuesta_confiada.json" <<'EOF'
{"type":"static","content":"CUH{nunca_confies_en_campos_ocultos}","data":""}
EOF
write "$API/hints_encuesta_confiada.json" <<'EOF'
[{"type":"standard","content":"Un campo oculto sigue siendo un campo controlado por el cliente.","cost":0},{"type":"standard","content":"El endpoint util no es la pagina inicial sino la ruta que recibe el formulario.","cost":0},{"type":"standard","content":"Repite la solicitud con valores alternativos y observa la respuesta completa.","cost":0}]
EOF
write "$CLI/registro_sin_servidor/challenge.yml" <<'EOF'
name: "Registro sin servidor"
category: "Web"
description: |
  Existe un formulario de pre-registro de laboratorio en `http://45.55.49.111:8084` dentro de este entorno academico controlado y autorizado. La interfaz publica aplica restricciones para participantes, pero tu trabajo es verificar que realmente valida el servidor y no solo el navegador. Observa el formulario, revisa la peticion y reproduce manualmente un envio coherente para obtener la respuesta correcta.

  Recurso interno opcional del laboratorio: [Notas internas sobre formularios](/formularios-lab).
value: 230
type: "standard"
state: "visible"
flags:
  - "CUH{el_servidor_tambien_debe_validar}"
hints:
  - "No confundas validacion de navegador con validacion de servidor."
  - "Revisa que campos se envian realmente al hacer submit."
  - "Una peticion manual con curl o un proxy local basta para resolverlo."
EOF
write "$CLI/encuesta_confiada/challenge.yml" <<'EOF'
name: "Encuesta confiada"
category: "Web"
description: |
  Hay una encuesta de laboratorio disponible en `http://45.55.49.111:8085` dentro de este entorno academico controlado y autorizado. A simple vista parece una encuesta publica comun, pero la logica real depende de datos que el cliente envia al servidor. Tu objetivo es observar el formulario, identificar que parametros se envian y comprobar si el servidor confia demasiado en ellos.

  Recurso interno opcional del laboratorio: [Notas internas sobre formularios](/formularios-lab).
value: 260
type: "standard"
state: "visible"
flags:
  - "CUH{nunca_confies_en_campos_ocultos}"
hints:
  - "Un campo oculto sigue siendo un campo controlado por el cliente."
  - "El endpoint util no es la pagina inicial sino la ruta que recibe el formulario."
  - "Repite la solicitud con valores alternativos y observa la respuesta completa."
EOF
write "$PAGES/formularios-lab.html" <<'EOF'
<section>
  <h1>Notas internas sobre formularios</h1>
  <p>Estas notas forman parte del laboratorio academico controlado del hackathon CUH. Su objetivo es reforzar una idea basica: los valores que envia el navegador no deben considerarse confiables por si solos.</p>
  <ul>
    <li>Revisa la ruta exacta a la que se envia el formulario.</li>
    <li>Identifica nombres y valores de todos los campos, incluidos los ocultos.</li>
    <li>Comprueba si el servidor acepta valores distintos a los mostrados por la interfaz.</li>
    <li>Repite la solicitud de manera manual solo dentro de este entorno autorizado.</li>
  </ul>
</section>
EOF
backup "$SCR/actualizar_paginas_ctfd.sh"
python3 - <<'PY'
from pathlib import Path
p=Path('/opt/cuh-ctf/scripts/actualizar_paginas_ctfd.sh')
text=p.read_text()
ins='    {"route": "formularios-lab", "title": "Notas internas sobre formularios", "hidden": True, "html": (pages_dir / "formularios-lab.html").read_text(encoding="utf-8")},\n'
marker='    {"route": "panel-interno"'
if 'formularios-lab' not in text and marker in text:
    text=text.replace(marker, ins+marker)
p.write_text(text)
PY
backup "$DOCS/FAQ_PARTICIPANTES_CTFD.html"
python3 - <<'PY'
from pathlib import Path
p=Path('/opt/cuh-ctf/docs/FAQ_PARTICIPANTES_CTFD.html')
text=p.read_text()
for item in ['<li><code>http://45.55.49.111:8084</code> para <strong>Registro sin servidor</strong>.</li>','<li><code>http://45.55.49.111:8085</code> para <strong>Encuesta confiada</strong>.</li>']:
    if item not in text:
        text=text.replace('</ul>\n<p><strong>Herramientas recomendadas</strong>', item+'\n</ul>\n<p><strong>Herramientas recomendadas</strong>', 1)
extra='<li>En los retos de formularios puede ser necesario repetir una solicitud POST manualmente y modificar campos enviados por el navegador.</li>'
if extra not in text:
    text=text.replace('</ul>\n<p><strong>Que implica cada reto de cracking</strong>', extra+'\n</ul>\n<p><strong>Que implica cada reto de cracking</strong>', 1)
p.write_text(text)
PY
backup "$DOCS/README_GENERAL_ORGANIZADOR.md"
python3 - <<'PY'
from pathlib import Path
p=Path('/opt/cuh-ctf/docs/README_GENERAL_ORGANIZADOR.md')
text=p.read_text()
line='- Retos de formularios web en `8084` y `8085` para practicar observacion de campos ocultos y repeticion manual de solicitudes.\n'
if line not in text:
    text += '\n'+line
p.write_text(text)
PY
backup "$DOCS/CTFD_COPY_PASTE.md"
python3 - <<'PY'
from pathlib import Path
p=Path('/opt/cuh-ctf/docs/CTFD_COPY_PASTE.md')
text=p.read_text()
block='''\n## Registro sin servidor\n- Name: Registro sin servidor\n- Category: Web\n- Value: 230\n- Type: standard\n- State: visible\n- Description: Existe un formulario de pre-registro de laboratorio en `http://45.55.49.111:8084` dentro de este entorno academico controlado y autorizado. La interfaz publica aplica restricciones para participantes, pero tu trabajo es verificar que realmente valida el servidor y no solo el navegador. Observa el formulario, revisa la peticion y reproduce manualmente un envio coherente para obtener la respuesta correcta.\n- Flag: `CUH{el_servidor_tambien_debe_validar}`\n- Hints:\n  - No confundas validacion de navegador con validacion de servidor.\n  - Revisa que campos se envian realmente al hacer submit.\n  - Una peticion manual con curl o un proxy local basta para resolverlo.\n- Servicio asociado: `http://45.55.49.111:8084`\n\n## Encuesta confiada\n- Name: Encuesta confiada\n- Category: Web\n- Value: 260\n- Type: standard\n- State: visible\n- Description: Hay una encuesta de laboratorio disponible en `http://45.55.49.111:8085` dentro de este entorno academico controlado y autorizado. A simple vista parece una encuesta publica comun, pero la logica real depende de datos que el cliente envia al servidor. Tu objetivo es observar el formulario, identificar que parametros se envian y comprobar si el servidor confia demasiado en ellos.\n- Flag: `CUH{nunca_confies_en_campos_ocultos}`\n- Hints:\n  - Un campo oculto sigue siendo un campo controlado por el cliente.\n  - El endpoint util no es la pagina inicial sino la ruta que recibe el formulario.\n  - Repite la solicitud con valores alternativos y observa la respuesta completa.\n- Servicio asociado: `http://45.55.49.111:8085`\n'''
if '## Registro sin servidor' not in text:
    text += block
p.write_text(text)
PY
printf 'codex2026\n' | sudo -S -p '' bash /opt/cuh-ctf/scripts/actualizar_paginas_ctfd.sh
printf 'codex2026\n' | sudo -S -p '' bash /opt/cuh-ctf/scripts/actualizar_faq_ctfd.sh
bash "$SCR/registrar_formularios_via_internal.sh"
docker exec -i ctfd-ctfd-1 python3 - <<'PY'
from CTFd import create_app
from CTFd.models import Pages, Challenges
app=create_app()
with app.app_context():
    p=Pages.query.filter_by(route='formularios-lab').first()
    print('formularios-lab', bool(p), getattr(p,'hidden',None))
    for name in ('Registro sin servidor','Encuesta confiada'):
        c=Challenges.query.filter_by(name=name).first()
        print(name, getattr(c,'id',None))
PY
bash "$SCR/validar_registro_sin_servidor.sh"
bash "$SCR/validar_encuesta_confiada.sh"
bash "$SCR/validar_todo_cuh_ctf.sh"
printf 'codex2026\n' | sudo -S -p '' systemctl is-active cuh-registro-sin-servidor
printf 'codex2026\n' | sudo -S -p '' systemctl is-active cuh-encuesta-confiada
