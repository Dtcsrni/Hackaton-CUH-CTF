from pathlib import Path
import textwrap


BASE = Path("/opt/cuh-ctf")
DOCS_PAGES = BASE / "docs" / "pages"
SCRIPTS = BASE / "scripts"


def common_style():
    return """<style>
  :root {
    --cuh-text: #eef4ff;
    --cuh-soft: #d8e4fb;
    --cuh-line: rgba(255,255,255,0.08);
    --cuh-blue: #71abff;
    --cuh-green: #61ff9c;
    --cuh-red: #ff636d;
  }
  .cuh-page {
    max-width: 1160px;
    margin: 0 auto;
    padding: 28px 24px 72px 24px;
    color: var(--cuh-text);
  }
  .cuh-head h1 {
    margin: 0 0 12px 0;
    font-size: 2.6rem;
    font-weight: 800;
    color: #fff;
  }
  .cuh-head p {
    margin: 0;
    color: var(--cuh-soft);
    line-height: 1.8;
    max-width: 920px;
  }
  .cuh-divider {
    height: 2px;
    margin: 28px 0 30px 0;
    background: linear-gradient(90deg, rgba(97,255,156,0), rgba(113,171,255,0.75), rgba(255,99,109,0.45), rgba(97,255,156,0));
    border-radius: 999px;
  }
  .cuh-grid {
    display: grid;
    gap: 16px;
  }
  .cuh-grid.cols-2 {
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  }
  .cuh-card {
    padding: 18px 20px;
    border: 1px solid var(--cuh-line);
    border-radius: 16px;
    background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.015));
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  }
  .cuh-card h3 {
    margin: 0 0 10px 0;
    font-size: 1.08rem;
    font-weight: 800;
    color: #fff;
  }
  .cuh-card p, .cuh-card li {
    color: var(--cuh-soft);
    line-height: 1.8;
  }
  .cuh-card p {
    margin: 0;
  }
  .cuh-card ul, .cuh-card ol {
    margin: 8px 0 0 18px;
    padding: 0;
  }
  .cuh-chip {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 999px;
    margin: 0 8px 8px 0;
    background: rgba(113,171,255,0.12);
    border: 1px solid rgba(113,171,255,0.18);
    color: #fff;
    font-weight: 700;
    font-size: 0.92rem;
  }
  .cuh-code {
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    color: #fff;
  }
  .cuh-links {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    margin-top: 28px;
  }
  .cuh-link {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 180px;
    padding: 14px 18px;
    text-decoration: none;
    border-radius: 14px;
    color: #fff;
    font-weight: 800;
    background: linear-gradient(180deg, rgba(22,54,109,0.96), rgba(18,43,89,1));
    border: 1px solid rgba(255,255,255,0.08);
  }
  .cuh-link:hover {
    color: #fff;
    text-decoration: none;
  }
</style>"""


def page(title: str, intro: str, body: str, links: list[tuple[str, str]]):
    link_html = "\n".join(
        f'    <a class="cuh-link" href="{href}">{label}</a>' for label, href in links
    )
    return f"""{common_style()}
<div class="cuh-page">
  <header class="cuh-head">
    <h1>{title}</h1>
    <p>{intro}</p>
  </header>
  <div class="cuh-divider"></div>
  {body}
  <div class="cuh-links">
{link_html}
  </div>
</div>
"""


PAGES = {
    "index": {
        "title": "Hackaton CTF CUH 2026",
        "hidden": False,
        "auth_required": False,
        "content": page(
            "Hackaton OSINT + CTF CUH 2026",
            "Laboratorio academico controlado del Centro Universitario Hidalguense con retos introductorios e intermedios de reconocimiento, Linux, web, forense y cracking.",
            """
  <section class="cuh-grid cols-2">
    <div class="cuh-card">
      <h3>Acceso rapido</h3>
      <ol>
        <li>Ingresa a <span class="cuh-code">http://45.55.49.111:8000</span>.</li>
        <li>Abre <strong>Desafios</strong> y elige un reto.</li>
        <li>Descarga el archivo o valida el servicio publicado.</li>
        <li>Resuelve desde Kali Linux y envia la flag en CTFd.</li>
      </ol>
    </div>
    <div class="cuh-card">
      <h3>Servicios del laboratorio</h3>
      <p><span class="cuh-chip">31337/tcp</span><span class="cuh-chip">8081/http</span><span class="cuh-chip">8082/http</span><span class="cuh-chip">8083/http</span></p>
      <p>Todos los servicios anteriores forman parte del alcance autorizado. No hay acceso SSH, shell ni otros objetivos validos fuera de CTFd y estos endpoints.</p>
    </div>
    <div class="cuh-card">
      <h3>Retos con archivos</h3>
      <p><span class="cuh-chip">reto_archivos_linux.zip</span><span class="cuh-chip">logo_cuh_reto.png</span><span class="cuh-chip">portada_cuh_reto.png</span><span class="cuh-chip">proxy_lab.zip</span><span class="cuh-chip">hash_respaldo.txt</span><span class="cuh-chip">evidencia_protegida.zip</span><span class="cuh-chip">acceso_heredado_kit.zip</span></p>
    </div>
    <div class="cuh-card">
      <h3>Herramientas utiles</h3>
      <p><span class="cuh-chip">nmap</span><span class="cuh-chip">nc</span><span class="cuh-chip">curl</span><span class="cuh-chip">unzip</span><span class="cuh-chip">find</span><span class="cuh-chip">grep</span><span class="cuh-chip">file</span><span class="cuh-chip">strings</span><span class="cuh-chip">john</span><span class="cuh-chip">hashcat</span></p>
    </div>
  </section>
""",
            [
                ("Desafios", "/challenges"),
                ("Inicio rapido", "/inicio-rapido"),
                ("Guia de herramientas", "/guia-herramientas"),
                ("FAQ", "/faq"),
                ("Reglas", "/reglas"),
            ],
        ),
    },
    "reglas": {
        "title": "Reglas",
        "hidden": False,
        "auth_required": False,
        "content": page(
            "Reglas del evento",
            "Las siguientes reglas delimitan el alcance tecnico y academico del laboratorio. El objetivo es aprender, no probar tecnicas fuera del entorno autorizado.",
            """
  <section class="cuh-grid cols-2">
    <div class="cuh-card">
      <h3>Alcance permitido</h3>
      <ul>
        <li>La plataforma CTFd en <span class="cuh-code">http://45.55.49.111:8000</span>.</li>
        <li>Los servicios explicitamente publicados por los retos.</li>
        <li>Los archivos adjuntos entregados desde CTFd.</li>
      </ul>
    </div>
    <div class="cuh-card">
      <h3>Acceso prohibido</h3>
      <ul>
        <li>No hay acceso SSH, shell, Docker, base de datos ni escritorio remoto para participantes.</li>
        <li>No esta permitido escanear ni probar puertos no documentados como parte del evento fuera del mismo droplet del laboratorio.</li>
        <li>No esta permitido salir del alcance del laboratorio ni reutilizar tecnicas contra terceros.</li>
      </ul>
    </div>
    <div class="cuh-card">
      <h3>Uso de herramientas</h3>
      <p>Se permite automatizacion y consulta de documentacion siempre que no afecte la disponibilidad del evento y se mantenga dentro del alcance autorizado.</p>
    </div>
    <div class="cuh-card">
      <h3>Flags y envios</h3>
      <p>Revisa si el reto espera una flag con formato <span class="cuh-code">CUH{...}</span> o un valor plano, como una clave o PIN recuperado. Si una flag no valida, reporta al staff el nombre del reto y tu evidencia minima.</p>
    </div>
  </section>
""",
            [
                ("FAQ", "/faq"),
                ("Inicio rapido", "/inicio-rapido"),
                ("Desafios", "/challenges"),
            ],
        ),
    },
    "faq": {
        "title": "Preguntas Frecuentes",
        "hidden": False,
        "auth_required": False,
        "content": Path("/opt/cuh-ctf/docs/FAQ_PARTICIPANTES_CTFD.html").read_text(
            encoding="utf-8"
        ),
    },
    "cronograma": {
        "title": "Cronograma",
        "hidden": False,
        "auth_required": False,
        "content": page(
            "Cronograma operativo",
            "Secuencia recomendada para el evento y para una resolucion ordenada de los retos. Los horarios exactos pueden ser ajustados por el staff.",
            """
  <section class="cuh-grid cols-2">
    <div class="cuh-card">
      <h3>Antes de empezar</h3>
      <ul>
        <li>Confirmar acceso a CTFd.</li>
        <li>Abrir Kali Linux y validar conectividad.</li>
        <li>Revisar reglas, FAQ e inicio rapido.</li>
      </ul>
    </div>
    <div class="cuh-card">
      <h3>Ruta sugerida</h3>
      <ol>
        <li>Puertas abiertas</li>
        <li>Comandos Linux - busqueda basica</li>
        <li>Logo en observacion / Portada con pista</li>
        <li>Cabeceras del laboratorio / JSON de prueba</li>
        <li>Bitacora del proxy</li>
        <li>Hash filtrado / ZIP bajo llave / Acceso heredado</li>
      </ol>
    </div>
    <div class="cuh-card">
      <h3>Durante el evento</h3>
      <p>Si un reto usa servicio, valida primero conectividad y luego interpreta. Si usa archivo, descarga, enumera y recien despues aplica herramientas mas especificas.</p>
    </div>
    <div class="cuh-card">
      <h3>Soporte</h3>
      <p>Las dudas operativas deben dirigirse al personal organizador. No esta permitido compartir soluciones completas ni flags entre participantes.</p>
    </div>
  </section>
""",
            [
                ("Inicio rapido", "/inicio-rapido"),
                ("FAQ", "/faq"),
                ("Desafios", "/challenges"),
            ],
        ),
    },
    "panel-interno": {
        "title": "Panel Interno",
        "hidden": True,
        "auth_required": False,
        "content": page(
            "Panel interno",
            "Documento interno expuesto por error a modo de pista historica del laboratorio.",
            """
  <section class="cuh-grid">
    <div class="cuh-card">
      <h3>Acceso de rastreadores detectado</h3>
      <p>Si llegaste aqui, documenta el hallazgo y valida el contenido visible.</p>
      <p>Flag: <strong>CUH{robots_no_guardan_secretos}</strong></p>
    </div>
  </section>
""",
            [
                ("Inicio", "/"),
                ("Desafios", "/challenges"),
            ],
        ),
    },
    "inicio-rapido": {
        "title": "Inicio rapido",
        "hidden": False,
        "auth_required": False,
        "content": page(
            "Inicio rapido para participantes",
            "Pagina de referencia para comenzar sin perder tiempo en friccion operativa.",
            """
  <section class="cuh-grid cols-2">
    <div class="cuh-card">
      <h3>Paso 1: acceso</h3>
      <p>Abre <span class="cuh-code">http://45.55.49.111:8000</span>, inicia sesion y revisa el tablero de desafios.</p>
    </div>
    <div class="cuh-card">
      <h3>Paso 2: entorno</h3>
      <p>Trabaja desde Kali Linux. No necesitas ni tienes acceso SSH al servidor del evento.</p>
    </div>
    <div class="cuh-card">
      <h3>Paso 3: segun el reto</h3>
      <ul>
        <li>Si el reto usa red: <span class="cuh-code">nmap</span>, <span class="cuh-code">nc</span> o <span class="cuh-code">curl</span>.</li>
        <li>Si usa archivo: descarga, descomprime si aplica y enumera primero.</li>
        <li>Si usa cracking: limita tu trabajo al archivo o servicio de laboratorio indicado.</li>
      </ul>
    </div>
    <div class="cuh-card">
      <h3>Paso 4: envio</h3>
      <p>Envia la respuesta exacta esperada por el reto. Algunas son <span class="cuh-code">CUH{...}</span> y otras son valores planos, como un PIN.</p>
    </div>
  </section>
""",
            [
                ("FAQ", "/faq"),
                ("Guia de herramientas", "/guia-herramientas"),
                ("Desafios", "/challenges"),
            ],
        ),
    },
    "guia-herramientas": {
        "title": "Guia de herramientas",
        "hidden": False,
        "auth_required": False,
        "content": page(
            "Guia de herramientas",
            "Comandos base utiles dentro del alcance autorizado del laboratorio. No sustituyen el criterio tecnico, pero aceleran el arranque.",
            """
  <section class="cuh-grid cols-2">
    <div class="cuh-card">
      <h3>Reconocimiento</h3>
      <ul>
        <li><span class="cuh-code">nmap -sS -Pn 45.55.49.111</span></li>
        <li><span class="cuh-code">nc 45.55.49.111 31337</span></li>
      </ul>
    </div>
    <div class="cuh-card">
      <h3>HTTP</h3>
      <ul>
        <li><span class="cuh-code">curl -I http://45.55.49.111:8081</span></li>
        <li><span class="cuh-code">curl http://45.55.49.111:8082/api/status</span></li>
        <li><span class="cuh-code">curl -u usuario:clave http://45.55.49.111:8083/panel</span></li>
      </ul>
    </div>
    <div class="cuh-card">
      <h3>Archivos</h3>
      <ul>
        <li><span class="cuh-code">unzip archivo.zip</span></li>
        <li><span class="cuh-code">find . -type f</span></li>
        <li><span class="cuh-code">grep -R "CUH{" .</span></li>
        <li><span class="cuh-code">file imagen.png</span></li>
        <li><span class="cuh-code">grep -a "CUH{" archivo.bin</span></li>
      </ul>
    </div>
    <div class="cuh-card">
      <h3>Cracking offline</h3>
      <ul>
        <li><span class="cuh-code">john</span> y <span class="cuh-code">hashcat</span> para hashes.</li>
        <li><span class="cuh-code">zip2john</span> o <span class="cuh-code">fcrackzip</span> para ZIP protegidos.</li>
        <li>Limita cualquier prueba al archivo o servicio del reto correspondiente.</li>
      </ul>
    </div>
  </section>
""",
            [
                ("Inicio rapido", "/inicio-rapido"),
                ("FAQ", "/faq"),
                ("Desafios", "/challenges"),
            ],
        ),
    },
    "inventario-lab": {
        "title": "Inventario del laboratorio",
        "hidden": True,
        "auth_required": False,
        "content": page(
            "Inventario tecnico del laboratorio",
            "Pagina interna con contexto de servicios y familias de retos. No contiene flags ni soluciones directas.",
            """
  <section class="cuh-grid cols-2">
    <div class="cuh-card">
      <h3>Servicios publicados</h3>
      <ul>
        <li><span class="cuh-code">31337/tcp</span> laboratorio TCP de entrenamiento</li>
        <li><span class="cuh-code">8081/http</span> servicio HTTP con observacion de cabeceras</li>
        <li><span class="cuh-code">8082/http</span> servicio API basico de estado</li>
        <li><span class="cuh-code">8083/http</span> servicio heredado con autenticacion basica</li>
      </ul>
    </div>
    <div class="cuh-card">
      <h3>Retos asociados</h3>
      <p>Puertas abiertas, Cabeceras del laboratorio, JSON de prueba y Acceso heredado.</p>
    </div>
  </section>
""",
            [
                ("Inicio rapido", "/inicio-rapido"),
                ("Desafios", "/challenges"),
            ],
        ),
    },
    "analisis-archivos": {
        "title": "Analisis de archivos",
        "hidden": True,
        "auth_required": False,
        "content": page(
            "Guia interna de analisis de archivos",
            "Lista de trabajo para retos donde la evidencia se entrega como archivo adjunto y se resuelve fuera de linea.",
            """
  <section class="cuh-grid cols-2">
    <div class="cuh-card">
      <h3>Flujo recomendado</h3>
      <ol>
        <li>Descargar el archivo correcto desde CTFd.</li>
        <li>Identificar tipo real de archivo.</li>
        <li>Descomprimir si aplica.</li>
        <li>Listar estructura y revisar contenido textual antes de usar herramientas mas complejas.</li>
      </ol>
    </div>
    <div class="cuh-card">
      <h3>Retos asociados</h3>
      <p>Comandos Linux - busqueda basica, Logo en observacion, Portada con pista, Bitacora del proxy, Hash filtrado y ZIP bajo llave.</p>
    </div>
  </section>
""",
            [
                ("Guia de herramientas", "/guia-herramientas"),
                ("Desafios", "/challenges"),
            ],
        ),
    },
    "credenciales-legado": {
        "title": "Credenciales heredadas",
        "hidden": True,
        "auth_required": False,
        "content": page(
            "Nota interna sobre credenciales heredadas",
            "Contexto tecnico para retos con autenticacion basica del laboratorio. No contiene usuarios o claves reales del evento fuera del material adjunto.",
            """
  <section class="cuh-grid cols-2">
    <div class="cuh-card">
      <h3>HTTP Basic Auth</h3>
      <p>La autenticacion se envuelve en una cabecera <span class="cuh-code">Authorization: Basic ...</span>. El reto correspondiente ya delimita la ruta y el kit de credenciales candidatas.</p>
    </div>
    <div class="cuh-card">
      <h3>Retos asociados</h3>
      <p>Acceso heredado. La prueba debe hacerse solo contra <span class="cuh-code">http://45.55.49.111:8083/panel</span> y usando el kit adjunto del laboratorio.</p>
    </div>
  </section>
""",
            [
                ("FAQ", "/faq"),
                ("Desafios", "/challenges"),
            ],
        ),
    },
}


CHALLENGE_LINKS = {
    "Calentamiento - Bienvenida": ("inicio-rapido", "Inicio rápido del laboratorio"),
    "Leer también es hacking": ("inicio-rapido", "Inicio rápido del laboratorio"),
    "Robots curiosos": ("guia-herramientas", "Guía de herramientas"),
    "Base64 no es cifrado": ("cracking-lab", "Notas internas sobre cracking"),
    "César escolar": ("cracking-lab", "Notas internas sobre cracking"),
    "Puertas abiertas": ("inventario-lab", "Inventario interno del laboratorio"),
    "Metadatos indiscretos": ("analisis-archivos", "Guía interna de análisis de archivos"),
    "Cabeceras del laboratorio": ("inventario-lab", "Inventario interno del laboratorio"),
    "JSON de prueba": ("inventario-lab", "Inventario interno del laboratorio"),
    "Comandos Linux - búsqueda básica": ("analisis-archivos", "Guia interna de analisis de archivos"),
    "Logo en observación": ("analisis-archivos", "Guia interna de analisis de archivos"),
    "Portada con pista": ("analisis-archivos", "Guia interna de analisis de archivos"),
    "Bitácora del proxy": ("analisis-archivos", "Guia interna de analisis de archivos"),
    "Hash filtrado": ("cracking-lab", "Notas internas sobre cracking"),
    "ZIP bajo llave": ("cracking-lab", "Notas internas sobre cracking"),
    "Acceso heredado": ("credenciales-legado", "Nota interna sobre credenciales heredadas"),
    "Registro sin servidor": ("formularios-lab", "Notas internas sobre formularios"),
    "Encuesta confiada": ("formularios-lab", "Notas internas sobre formularios"),
    "Invitado privilegiado": ("jwt-lab", "Notas internas sobre JWT"),
    "Secreto compartido debil": ("jwt-lab", "Notas internas sobre JWT"),
    "Fuente principal": ("frontend-lab", "Notas internas sobre frontend"),
    "Consola curiosa": ("frontend-lab", "Notas internas sobre frontend"),
    "Cookie de rol": ("cookies-lab", "Notas internas sobre cookies"),
    "Cookie firmada debil": ("cookies-lab", "Notas internas sobre cookies"),
    "Acceso por defecto": ("bruteforce-lab", "Guía interna de fuerza bruta"),
    "Formulario de acceso": ("bruteforce-lab", "Guía interna de fuerza bruta"),
    "Rompe el sistema": ("reglas", "Reglas del laboratorio"),
}


def write_source_files():
    DOCS_PAGES.mkdir(parents=True, exist_ok=True)
    for route, page_def in PAGES.items():
        (DOCS_PAGES / f"{route}.html").write_text(
            page_def["content"], encoding="utf-8", newline="\n"
        )


def write_sync_script():
    sync_py = textwrap.dedent(
        f"""
        from pathlib import Path
        from CTFd import create_app
        from CTFd.models import db, Pages, Challenges

        PAGES = {repr({k: {ik: iv for ik, iv in v.items() if ik != "content"} for k, v in PAGES.items()})}
        LINKS = {repr(CHALLENGE_LINKS)}

        def load_content(route):
            return Path('/opt/cuh-ctf/docs/pages/' + route + '.html').read_text(encoding='utf-8')

        app = create_app()
        with app.app_context():
            for route, data in PAGES.items():
                page = Pages.query.filter_by(route=route).first()
                if page is None:
                    page = Pages()
                    db.session.add(page)
                page.title = data['title']
                page.route = route
                page.content = load_content(route)
                page.draft = False
                page.hidden = data['hidden']
                page.auth_required = data['auth_required']
                page.format = 'html'
                page.link_target = None
            db.session.flush()

            managed_routes = ['/inventario-lab)', '(/analisis-archivos)', '(/credenciales-legado)']
            for chal_name, (route, label) in LINKS.items():
                challenge = Challenges.query.filter_by(name=chal_name).first()
                if challenge is None:
                    continue
                lines = [line for line in (challenge.description or '').splitlines() if not any(token in line for token in managed_routes)]
                lines.append('')
                lines.append(f'Recurso interno opcional del laboratorio: [{{label}}](/{{route}}).')
                challenge.description = '\\n'.join(lines).strip()

            db.session.commit()
            print('Paginas y asociaciones sincronizadas.')
        """
    ).strip() + "\n"

    wrapper = textwrap.dedent(
        """
        #!/usr/bin/env bash
        set -euo pipefail
        CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}
        WORKDIR=/tmp/cuh_ctfd_pages
        mkdir -p "$WORKDIR"
        trap 'rm -rf "$WORKDIR"' EXIT
        docker cp /opt/cuh-ctf/docs/pages/. "${CTFD_CONTAINER}:/opt/cuh-pages"
        cat > "$WORKDIR/sync_pages.py" <<'PY'
        from pathlib import Path
        import shutil
        shutil.rmtree('/opt/cuh-ctf/docs/pages', ignore_errors=True)
        shutil.copytree('/opt/cuh-pages', '/opt/cuh-ctf/docs/pages')
        PY
        docker cp "$WORKDIR/sync_pages.py" "${CTFD_CONTAINER}:/tmp/sync_pages.py"
        docker exec "${CTFD_CONTAINER}" python3 /tmp/sync_pages.py >/dev/null
        cat > "$WORKDIR/apply_pages.py" <<'PY'
        """
    )
    wrapper_end = textwrap.dedent(
        """
        PY
        docker cp "$WORKDIR/apply_pages.py" "${CTFD_CONTAINER}:/tmp/apply_pages.py"
        docker exec -e PYTHONPATH=/opt/CTFd "${CTFD_CONTAINER}" python3 /tmp/apply_pages.py
        """
    )
    # The container needs the page sources, but the DB write should operate inside the container using the same source path.
    # Copy to /tmp/pages inside the container and read from there in the DB sync script.
    sync_py = sync_py.replace(
        "/opt/cuh-ctf/docs/pages/",
        "/tmp/cuh-pages/",
    )
    wrapper = textwrap.dedent(
        """
        #!/usr/bin/env bash
        set -euo pipefail
        CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}
        WORKDIR=/tmp/cuh_ctfd_pages
        mkdir -p "$WORKDIR"
        trap 'rm -rf "$WORKDIR"' EXIT
        printf 'syncing pages\\n' >/dev/null
        docker exec "${CTFD_CONTAINER}" mkdir -p /tmp/cuh-pages
        """
    )
    for route in PAGES:
        wrapper += f'docker cp "/opt/cuh-ctf/docs/pages/{route}.html" "${{CTFD_CONTAINER}}:/tmp/cuh-pages/{route}.html"\n'
    wrapper += 'cat > "$WORKDIR/apply_pages.py" <<\'PY\'\n'
    wrapper += sync_py
    wrapper += "PY\n"
    wrapper += 'docker cp "$WORKDIR/apply_pages.py" "${CTFD_CONTAINER}:/tmp/apply_pages.py"\n'
    wrapper += 'docker exec -e PYTHONPATH=/opt/CTFd "${CTFD_CONTAINER}" python3 /tmp/apply_pages.py\n'

    SCRIPTS.mkdir(parents=True, exist_ok=True)
    (SCRIPTS / "actualizar_paginas_ctfd.sh").write_text(
        wrapper, encoding="utf-8", newline="\n"
    )
    (SCRIPTS / "actualizar_paginas_ctfd.sh").chmod(0o755)


if __name__ == "__main__":
    write_source_files()
    write_sync_script()
