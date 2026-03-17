#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST=${REMOTE_HOST:-45.55.49.111}
REMOTE_USER=${REMOTE_USER:-codexdeploy}
SSH_KEY=${SSH_KEY:-C:\Users\evega\.ssh\codex_ctfd_cuh}
REMOTE_BASE=/opt/cuh-ctf
CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}
PORT=${PORT:-8092}

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

cat > "$tmp_dir/server_sqli.py" <<'PY'
#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
import html
import sqlite3
from pathlib import Path

HOST = "0.0.0.0"
PORT = 8092
DB_PATH = Path("/opt/cuh-ctf/challenges/consulta_insegura/reportes.sqlite3")

INDEX = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Portal de reportes CUH</title>
  <style>
    body{font-family:Arial,sans-serif;background:#0d1c3c;color:#eef5ff;padding:36px}
    .panel{max-width:760px;margin:0 auto;padding:24px;border-radius:18px;background:#14284e;border:1px solid #29538d}
    h1{margin-top:0}
    label{display:block;margin:12px 0 6px}
    input{width:100%;padding:12px;border-radius:10px;border:1px solid #456b9a;background:#071223;color:#fff}
    button{margin-top:16px;padding:12px 18px;border:none;border-radius:10px;background:#72f4ff;color:#04131f;font-weight:700}
    .msg{margin-top:14px;padding:12px;border-radius:12px;background:#091625}
    .hint{margin-top:16px;color:#a9c6ee}
    code{background:#091625;padding:2px 6px;border-radius:6px}
  </style>
</head>
<body>
  <div class="panel">
    <h1>Portal de reportes internos</h1>
    <p>Acceso restringido a personal del laboratorio. Usa tus credenciales institucionales para consultar reportes.</p>
    <form method="post" action="/login">
      <label for="username">Usuario</label>
      <input id="username" name="username" autocomplete="off">
      <label for="password">Clave</label>
      <input id="password" name="password" type="password" autocomplete="off">
      <button type="submit">Entrar</button>
    </form>
    <p class="hint">Acceso de soporte temporal deshabilitado desde la migración de SQLite.</p>
  </div>
</body>
</html>"""

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS usuarios")
    cur.execute("CREATE TABLE usuarios (username TEXT, password TEXT, reporte TEXT)")
    cur.executemany(
        "INSERT INTO usuarios(username, password, reporte) VALUES(?, ?, ?)",
        [
            ("analista", "reporte2026", "Reporte de área: sin hallazgos críticos."),
            ("soporte", "temporal", "Pendiente de normalización del portal."),
            ("admin", "n0_visible", "CUH{sqli_en_portal_de_reportes}"),
        ],
    )
    conn.commit()
    conn.close()

def vulnerable_lookup(username, password):
    query = f"SELECT reporte FROM usuarios WHERE username = '{username}' AND password = '{password}'"
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
      row = cur.execute(query).fetchone()
    except sqlite3.Error as exc:
      conn.close()
      return "error", f"Consulta inválida: {exc}"
    conn.close()
    if row:
      return "ok", row[0]
    return "fail", "Credenciales inválidas o sin permisos sobre reportes."

class Handler(BaseHTTPRequestHandler):
    server_version = "CUHSQLi/1.0"

    def _send(self, body, code=200):
        payload = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_response(404)
            self.end_headers()
            return
        self._send(INDEX)

    def do_POST(self):
        if self.path != "/login":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8", errors="ignore")
        params = parse_qs(raw)
        username = params.get("username", [""])[0]
        password = params.get("password", [""])[0]
        status, message = vulnerable_lookup(username, password)
        title = {
            "ok": "Acceso concedido",
            "fail": "Acceso rechazado",
            "error": "Error en consulta",
        }[status]
        body = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{title}</title></head>
<body style="font-family:Arial,sans-serif;background:#0d1c3c;color:#eef5ff;padding:36px">
<div style="max-width:760px;margin:0 auto;padding:24px;border-radius:18px;background:#14284e;border:1px solid #29538d">
<h1>{title}</h1>
<p class="msg">{html.escape(message)}</p>
<p><a href="/" style="color:#72f4ff">Volver al portal</a></p>
</div></body></html>"""
        self._send(body)

    def log_message(self, fmt, *args):
        return

if __name__ == "__main__":
    init_db()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"[cuh-sqli] listening on {HOST}:{PORT}")
    server.serve_forever()
PY

cat > "$tmp_dir/cuh-sqli.service" <<'EOF'
[Unit]
Description=CUH SQLi challenge
After=network.target

[Service]
User=codexdeploy
WorkingDirectory=/opt/cuh-ctf/challenges/consulta_insegura
ExecStart=/usr/bin/python3 /opt/cuh-ctf/challenges/consulta_insegura/server_sqli.py
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
EOF

cat > "$tmp_dir/deploy_remote.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
BASE=/opt/cuh-ctf
CHAL=$BASE/challenges/consulta_insegura
CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}
mkdir -p "$CHAL"
cp /tmp/server_sqli.py "$CHAL/server_sqli.py"
chmod +x "$CHAL/server_sqli.py"
printf 'codex2026\n' | sudo -S -p '' cp /tmp/cuh-sqli.service /etc/systemd/system/cuh-sqli.service
printf 'codex2026\n' | sudo -S -p '' systemctl daemon-reload
printf 'codex2026\n' | sudo -S -p '' systemctl enable --now cuh-sqli.service
printf 'codex2026\n' | sudo -S -p '' ufw allow 8092/tcp >/dev/null || true

cat >/tmp/upsert_page.py <<'PY'
from pathlib import Path
from CTFd import create_app
from CTFd.cache import clear_pages
from CTFd.models import db, Pages
app = create_app()
with app.app_context():
    route = 'sqli-lab'
    content = Path('/tmp/sqli-lab.html').read_text(encoding='utf-8')
    page = Pages.query.filter_by(route=route).first()
    if page is None:
        page = Pages(title='Guía de SQL Injection', route=route, content=content, draft=False, hidden=True, auth_required=False)
        db.session.add(page)
    else:
        page.title = 'Guía de SQL Injection'
        page.content = content
        page.hidden = True
        page.auth_required = False
        page.draft = False
    db.session.commit()
    clear_pages()
    print('page updated')
PY
docker cp /tmp/upsert_page.py "$CTFD_CONTAINER:/tmp/upsert_page.py"
docker cp /tmp/sqli-lab.html "$CTFD_CONTAINER:/tmp/sqli-lab.html"
docker exec -e PYTHONPATH=/opt/CTFd "$CTFD_CONTAINER" python3 /tmp/upsert_page.py

cat >/tmp/upsert_challenge.py <<'PY'
from CTFd import create_app
from CTFd.models import Challenges, Flags, Hints, db
from CTFd.cache import clear_challenges

SPEC = {
    'name': 'Consulta insegura',
    'category': 'Web',
    'value': 360,
    'type': 'standard',
    'state': 'visible',
    'description': (
        'Existe un portal de reportes internos en `http://45.55.49.111:8092/` dentro de este entorno académico controlado y autorizado. '
        'El acceso depende de una consulta SQL construida de forma insegura. Tu objetivo es revisar el formulario, observar cómo responde '
        'la autenticación y conseguir acceso a un reporte que no debería quedar expuesto con una consulta bien construida.\\n\\n'
        'Material de apoyo relacionado: [Guía interna de SQL Injection](/sqli-lab).'
    ),
    'flag': 'CUH{sqli_en_portal_de_reportes}',
    'hints': [
        (15, 'No empieces por automatizar. Primero mira el formulario, la ruta exacta del POST y cómo cambia la respuesta cuando falla.'),
        (25, 'Si una consulta mezcla texto del usuario con comillas simples, intenta razonar qué parte de la cláusula WHERE puedes alterar.'),
        (35, 'La autenticación usa dos campos, pero no necesariamente necesitas que ambos sigan participando en la lógica original de la consulta.'),
    ],
}

app = create_app()
with app.app_context():
    chal = Challenges.query.filter_by(name=SPEC['name']).first()
    if chal is None:
        chal = Challenges()
        db.session.add(chal)
        db.session.flush()
    chal.name = SPEC['name']
    chal.category = SPEC['category']
    chal.value = SPEC['value']
    chal.description = SPEC['description']
    chal.type = SPEC['type']
    chal.state = SPEC['state']
    Flags.query.filter_by(challenge_id=chal.id).delete()
    Hints.query.filter_by(challenge_id=chal.id).delete()
    db.session.add(Flags(challenge_id=chal.id, type='static', content=SPEC['flag'], data='case_insensitive'))
    for cost, content in SPEC['hints']:
        db.session.add(Hints(challenge_id=chal.id, type='standard', content=content, cost=cost, requirements=None))
    db.session.commit()
    clear_challenges()
    print({'challenge_id': chal.id, 'name': chal.name})
PY
docker cp /tmp/upsert_challenge.py "$CTFD_CONTAINER:/tmp/upsert_challenge.py"
docker exec -e PYTHONPATH=/opt/CTFd "$CTFD_CONTAINER" python3 /tmp/upsert_challenge.py

systemctl is-active --quiet cuh-sqli.service
ss -ltn | grep -q ':8092 '
curl -fsS http://127.0.0.1:8092/ | grep -q 'Portal de reportes internos'
curl -fsS -X POST http://127.0.0.1:8092/login -d 'username=visitante&password=temporal' | grep -q 'Acceso rechazado'
curl -fsS -X POST http://127.0.0.1:8092/login --data-urlencode \"username=admin' -- \" --data-urlencode 'password=x' | grep -q 'CUH{sqli_en_portal_de_reportes}'
EOF
chmod +x "$tmp_dir/deploy_remote.sh"

scp -i "$SSH_KEY" -o StrictHostKeyChecking=no "$tmp_dir/server_sqli.py" "${REMOTE_USER}@${REMOTE_HOST}:/tmp/server_sqli.py"
scp -i "$SSH_KEY" -o StrictHostKeyChecking=no "$tmp_dir/cuh-sqli.service" "${REMOTE_USER}@${REMOTE_HOST}:/tmp/cuh-sqli.service"
scp -i "$SSH_KEY" -o StrictHostKeyChecking=no "$tmp_dir/deploy_remote.sh" "${REMOTE_USER}@${REMOTE_HOST}:/tmp/deploy_sqli_remote.sh"
scp -i "$SSH_KEY" -o StrictHostKeyChecking=no "O:\\Descargas\\hackaton\\refresh_assets\\pages\\sqli-lab.html" "${REMOTE_USER}@${REMOTE_HOST}:/tmp/sqli-lab.html"
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "${REMOTE_USER}@${REMOTE_HOST}" "chmod +x /tmp/deploy_sqli_remote.sh && /tmp/deploy_sqli_remote.sh"
