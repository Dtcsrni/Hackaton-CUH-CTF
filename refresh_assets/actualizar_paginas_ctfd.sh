#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PAGES_DIR="${SCRIPT_DIR}/pages"
EXTRA_PAGES_JSON="${SCRIPT_DIR}/generated_safe_pages.json"
CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}
WORKDIR=/tmp/cuh_ctfd_pages
mkdir -p "$WORKDIR"
trap 'rm -rf "$WORKDIR"' EXIT

if [[ ! -d "$PAGES_DIR" ]]; then
  echo "Pages directory not found: $PAGES_DIR" >&2
  exit 1
fi

docker exec "${CTFD_CONTAINER}" mkdir -p /tmp/cuh-pages
for page_file in "${PAGES_DIR}"/*.html; do
  [[ -e "$page_file" ]] || continue
  docker cp "$page_file" "${CTFD_CONTAINER}:/tmp/cuh-pages/$(basename "$page_file")"
done
if [[ -f "$EXTRA_PAGES_JSON" ]]; then
  docker cp "$EXTRA_PAGES_JSON" "${CTFD_CONTAINER}:/tmp/generated_safe_pages.json"
fi

cat > "$WORKDIR/apply_pages.py" <<'PY'
from pathlib import Path
import json
import re
from CTFd import create_app
from CTFd.cache import clear_pages
from CTFd.models import db, Pages, Challenges
PAGES = {
  'index': {'title': 'Hackatón OSINT + CTF CUH 2026', 'hidden': False, 'auth_required': False},
  'reglas': {'title': 'Reglas', 'hidden': False, 'auth_required': False},
  'faq': {'title': 'Preguntas Frecuentes', 'hidden': False, 'auth_required': False},
  'cronograma': {'title': 'Cronograma', 'hidden': False, 'auth_required': False},
  'inicio-rapido': {'title': 'Inicio rápido', 'hidden': False, 'auth_required': False},
  'guia-herramientas': {'title': 'Guía de herramientas', 'hidden': False, 'auth_required': False},
  'laboratorio-visual': {'title': 'Laboratorio visual', 'hidden': False, 'auth_required': False},
  'mapa-retos': {'title': 'Mapa de retos', 'hidden': False, 'auth_required': False},
  'panel-interno': {'title': 'Panel Interno', 'hidden': True, 'auth_required': False},
  'bruteforce-lab': {'title': 'Guía de fuerza bruta', 'hidden': True, 'auth_required': False},
  'sqli-lab': {'title': 'Guía de SQL Injection', 'hidden': True, 'auth_required': False},
  'inventario-lab': {'title': 'Inventario del laboratorio', 'hidden': True, 'auth_required': False},
  'analisis-archivos': {'title': 'Análisis de archivos', 'hidden': True, 'auth_required': False},
  'credenciales-legado': {'title': 'Credenciales heredadas', 'hidden': True, 'auth_required': False},
  'formularios-lab': {'title': 'Notas internas sobre formularios', 'hidden': True, 'auth_required': False},
  'jwt-lab': {'title': 'Notas internas sobre JWT', 'hidden': True, 'auth_required': False},
  'frontend-lab': {'title': 'Notas internas sobre frontend', 'hidden': True, 'auth_required': False},
  'cookies-lab': {'title': 'Notas internas sobre cookies', 'hidden': True, 'auth_required': False},
  'cracking-lab': {'title': 'Notas internas sobre cracking', 'hidden': True, 'auth_required': False},
}
LINKS = {
  'Calentamiento - Bienvenida': ('inicio-rapido', 'Inicio rápido del laboratorio'),
  'Leer también es hacking': ('inicio-rapido', 'Inicio rápido del laboratorio'),
  'Robots curiosos': ('guia-herramientas', 'Guía de herramientas'),
  'Base64 no es cifrado': ('cracking-lab', 'Notas internas sobre cracking'),
  'César escolar': ('cracking-lab', 'Notas internas sobre cracking'),
  'Puertas abiertas': ('inventario-lab', 'Inventario interno del laboratorio'),
  'Metadatos indiscretos': ('analisis-archivos', 'Guía interna de análisis de archivos'),
  'Cabeceras del laboratorio': ('inventario-lab', 'Inventario interno del laboratorio'),
  'JSON de prueba': ('inventario-lab', 'Inventario interno del laboratorio'),
  'Comandos Linux - búsqueda básica': ('analisis-archivos', 'Guía interna de análisis de archivos'),
  'Logo en observación': ('analisis-archivos', 'Guía interna de análisis de archivos'),
  'Portada con pista': ('analisis-archivos', 'Guía interna de análisis de archivos'),
  'Bitácora del proxy': ('analisis-archivos', 'Guía interna de análisis de archivos'),
  'Hash filtrado': ('cracking-lab', 'Notas internas sobre cracking'),
  'ZIP bajo llave': ('cracking-lab', 'Notas internas sobre cracking'),
  'Acceso heredado': ('credenciales-legado', 'Notas internas sobre credenciales heredadas'),
  'Acceso por defecto': ('bruteforce-lab', 'Guía interna de fuerza bruta'),
  'Formulario de acceso': ('bruteforce-lab', 'Guía interna de fuerza bruta'),
  'Consulta insegura': ('sqli-lab', 'Guía interna de SQL Injection'),
  'Registro sin servidor': ('formularios-lab', 'Notas internas sobre formularios'),
  'Encuesta confiada': ('formularios-lab', 'Notas internas sobre formularios'),
  'Invitado privilegiado': ('jwt-lab', 'Notas internas sobre JWT'),
  'Secreto compartido debil': ('jwt-lab', 'Notas internas sobre JWT'),
  'Fuente principal': ('frontend-lab', 'Notas internas sobre frontend'),
  'Consola curiosa': ('frontend-lab', 'Notas internas sobre frontend'),
  'Cookie de rol': ('cookies-lab', 'Notas internas sobre cookies'),
  'Cookie firmada debil': ('cookies-lab', 'Notas internas sobre cookies'),
  'Rompe el sistema': ('reglas', 'Reglas del laboratorio'),
}
SHARED_CUHV_STYLE = """<style id="ctfcu-page-shared">
.cuhv-page{width:min(1680px,calc(100vw - 32px))!important;max-width:min(1680px,calc(100vw - 32px))!important;margin:0 auto!important;padding:32px 0 88px!important;display:grid!important;gap:28px!important;color:#eef1f5!important}
.cuhv-page>*{margin:0!important}
.cuhv-page a{color:#d7e4ef!important;text-decoration:none}
.cuhv-page a:hover,.cuhv-page a:focus{color:#fff!important}
.cuhv-hero,.cuhv-section,.cuhv-reader-reward,.cuhv-final-cover{position:relative!important;overflow:hidden!important;padding:28px!important;border:1px solid rgba(172,185,198,.16)!important;border-radius:30px!important;background:radial-gradient(circle at top right,rgba(127,147,168,.12),transparent 28%),linear-gradient(180deg,rgba(78,92,108,.96),rgba(29,36,43,.99))!important;box-shadow:0 26px 60px rgba(0,0,0,.28)!important}
.cuhv-hero::before,.cuhv-section::before{content:""!important;position:absolute!important;inset:0!important;pointer-events:none!important;background:linear-gradient(90deg,rgba(255,255,255,.04),rgba(255,255,255,0) 24%),repeating-linear-gradient(90deg,rgba(183,197,211,.04) 0,rgba(183,197,211,.04) 1px,transparent 1px,transparent 56px)!important;opacity:.4!important}
.cuhv-hero>*,.cuhv-section>*{position:relative!important;z-index:1!important}
.cuhv-hero{display:grid!important;grid-template-columns:minmax(0,1.12fr) minmax(320px,.88fr)!important;gap:22px!important;align-items:stretch!important}
.cuhv-hero-compact,.cuhv-hero-index{display:block!important}
.cuhv-hero-stage{display:grid!important;grid-template-columns:minmax(0,1.18fr) minmax(300px,.82fr)!important;grid-template-areas:"copy side"!important;gap:22px!important;align-items:stretch!important}
.cuhv-hero-copy,.cuhv-hero-side,.cuhv-card,.cuhv-step{min-width:0!important}
.cuhv-kicker{display:inline-flex!important;align-items:center!important;min-height:34px!important;padding:0 14px!important;border-radius:999px!important;background:linear-gradient(135deg,#46627f,#7b92ac)!important;color:#eef2f6!important;font-size:.78rem!important;font-weight:900!important;letter-spacing:.11em!important;text-transform:uppercase!important;box-shadow:0 12px 26px rgba(70,98,127,.2)!important}
.cuhv-hero h1,.cuhv-section-head h2{margin:12px 0 0!important;color:#f7fbff!important;letter-spacing:-.04em!important}
.cuhv-hero h1{font-size:clamp(2.5rem,5vw,5rem)!important;line-height:.95!important;max-width:14ch!important}
.cuhv-section-head{display:grid!important;gap:10px!important;max-width:72ch!important;margin-bottom:18px!important}
.cuhv-hero p,.cuhv-section-head p,.cuhv-card p,.cuhv-step p,.cuhv-note,.cuhv-note p,.cuhv-list li,.cuhv-photo-card figcaption{color:rgba(223,232,240,.82)!important;line-height:1.72!important}
.cuhv-actions{display:flex!important;flex-wrap:wrap!important;gap:12px!important;margin-top:20px!important}
.cuhv-button,.cuhv-button:visited{display:inline-flex!important;align-items:center!important;justify-content:center!important;min-height:50px!important;padding:0 18px!important;border-radius:16px!important;border:1px solid rgba(172,185,198,.14)!important;background:linear-gradient(135deg,#46627f,#7b92ac)!important;color:#eef1f3!important;font-weight:900!important;box-shadow:0 14px 28px rgba(70,98,127,.22)!important}
.cuhv-button-alt,.cuhv-button-alt:visited{background:linear-gradient(180deg,rgba(76,90,105,.88),rgba(34,42,50,.96))!important}
.cuhv-grid{display:grid!important;gap:18px!important}
.cuhv-grid-2{grid-template-columns:repeat(2,minmax(0,1fr))!important}
.cuhv-grid-3{grid-template-columns:repeat(3,minmax(0,1fr))!important}
.cuhv-grid-4{grid-template-columns:repeat(4,minmax(0,1fr))!important}
.cuhv-card,.cuhv-step,.cuhv-note,.cuhv-photo-card,.cuhv-hero-mini,.cuhv-hero-side-card,.cuhv-hero-side-note{position:relative!important;overflow:hidden!important;padding:22px!important;border:1px solid rgba(172,185,198,.14)!important;border-radius:24px!important;background:linear-gradient(180deg,rgba(84,99,116,.92),rgba(34,42,50,.98))!important;box-shadow:0 16px 36px rgba(0,0,0,.22)!important}
.cuhv-card h3,.cuhv-step strong,.cuhv-note strong,.cuhv-hero-mini strong,.cuhv-hero-side-card strong{display:block!important;margin:0 0 10px!important;color:#f7fbff!important;font-size:clamp(1.05rem,1.4vw,1.4rem)!important;line-height:1.2!important}
.cuhv-card>:last-child,.cuhv-step>:last-child,.cuhv-note>:last-child{margin-bottom:0!important}
.cuhv-list{margin:0!important;padding-left:18px!important}
.cuhv-list li+li{margin-top:8px!important}
.cuhv-codeblock{margin:0!important;padding:16px 18px!important;border:1px solid rgba(172,185,198,.14)!important;border-radius:18px!important;background:linear-gradient(180deg,rgba(16,27,44,.88),rgba(8,14,24,.96))!important;color:#edf4fb!important;font-size:.9rem!important;line-height:1.65!important;overflow:auto!important;white-space:pre-wrap!important;word-break:break-word!important}
.cuhv-timeline{display:grid!important;gap:16px!important}
.cuhv-step{padding-left:28px!important}
.cuhv-step::before{content:""!important;position:absolute!important;left:0!important;top:18px!important;bottom:18px!important;width:4px!important;border-radius:999px!important;background:linear-gradient(180deg,#7b92ac,rgba(180,194,207,.28))!important}
.cuhv-hero-mini-grid,.cuhv-hero-side-grid{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:14px!important}
.cuhv-photo-card{display:grid!important;gap:12px!important;align-content:start!important}
.cuhv-photo-card img,.cuhv-final-cover img{display:block!important;width:100%!important;border-radius:20px!important;object-fit:cover!important;border:1px solid rgba(172,185,198,.14)!important}
.cuhv-final-cover figure{margin:0!important}
@media (max-width:1320px){.cuhv-page{width:min(100vw - 24px,1680px)!important;max-width:min(100vw - 24px,1680px)!important}.cuhv-grid-4{grid-template-columns:repeat(2,minmax(0,1fr))!important}.cuhv-grid-3{grid-template-columns:repeat(2,minmax(0,1fr))!important}}
@media (max-width:1100px){.cuhv-hero,.cuhv-hero-stage{grid-template-columns:1fr!important}}
@media (max-width:760px){.cuhv-page{width:min(100vw - 16px,1680px)!important;max-width:min(100vw - 16px,1680px)!important;padding:18px 0 56px!important;gap:18px!important}.cuhv-hero,.cuhv-section,.cuhv-reader-reward,.cuhv-final-cover{padding:18px!important;border-radius:22px!important}.cuhv-hero h1{font-size:clamp(2rem,10vw,3.3rem)!important}.cuhv-grid-2,.cuhv-grid-3,.cuhv-grid-4,.cuhv-hero-mini-grid,.cuhv-hero-side-grid{grid-template-columns:1fr!important}.cuhv-card,.cuhv-step,.cuhv-note,.cuhv-photo-card,.cuhv-hero-mini,.cuhv-hero-side-card,.cuhv-hero-side-note{padding:16px!important;border-radius:18px!important}.cuhv-actions{flex-direction:column!important}.cuhv-button,.cuhv-button:visited{width:100%!important}}
</style>"""
extra_path = Path('/tmp/generated_safe_pages.json')
if extra_path.exists():
    extra = json.loads(extra_path.read_text(encoding='utf-8'))
    for page in extra.get('pages', []):
        PAGES[page['route']] = {
            'title': page['title'],
            'hidden': page.get('hidden', True),
            'auth_required': page.get('auth_required', False),
        }
    for challenge_name, meta in extra.get('links', {}).items():
        LINKS[challenge_name] = (meta['route'], meta['label'])
def load_content(route):
    content = Path('/tmp/cuh-pages/' + route + '.html').read_text(encoding='utf-8')
    content = re.sub(r'<style id="ctfcu-page-shared">.*?</style>', '', content, flags=re.S)
    if 'cuhv-page' in content:
        return content.rstrip() + '\n' + SHARED_CUHV_STYLE
    return content
def upsert_page(route, meta):
    page = Pages.query.filter_by(route=route).first()
    content = load_content(route)
    if page is None:
        page = Pages(title=meta['title'], route=route, content=content, draft=False, hidden=meta['hidden'], auth_required=meta['auth_required'])
        db.session.add(page)
    else:
        page.title = meta['title']
        page.content = content
        page.hidden = meta['hidden']
        page.auth_required = meta['auth_required']
        page.draft = False
app = create_app()
with app.app_context():
    for route, meta in PAGES.items():
        upsert_page(route, meta)
    db.session.commit()
    for challenge_name, (route, label) in LINKS.items():
        challenge = Challenges.query.filter_by(name=challenge_name).first()
        if challenge is None:
            continue
        marker = '(/' + route + ')'
        appendix = '\n\nMaterial de apoyo relacionado: [' + label + '](/' + route + ').'
        if marker not in (challenge.description or ''):
            challenge.description = (challenge.description or '').rstrip() + appendix
    db.session.commit()
    clear_pages()
    print('pages synced')
PY
docker cp "$WORKDIR/apply_pages.py" "${CTFD_CONTAINER}:/tmp/apply_pages.py"
docker exec -e PYTHONPATH=/opt/CTFd "${CTFD_CONTAINER}" python3 /tmp/apply_pages.py
