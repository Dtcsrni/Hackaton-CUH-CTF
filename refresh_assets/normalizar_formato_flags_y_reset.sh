#!/usr/bin/env bash
set -euo pipefail

CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}
STAMP=$(date +%Y%m%d%H%M%S)
BACKUP_DIR="/opt/cuh-ctf/artifacts/backups/flag_format_reset_${STAMP}"
mkdir -p "${BACKUP_DIR}"

docker exec -i "${CTFD_CONTAINER}" python3 - <<'PY' > "${BACKUP_DIR}/before.json"
import json
from CTFd import create_app
from CTFd.models import Challenges, Flags, Solves, Fails

app = create_app()

with app.app_context():
    out = []
    for name in ['Calentamiento - Bienvenida', 'Hash filtrado']:
        challenge = Challenges.query.filter_by(name=name).first()
        if not challenge:
            continue
        out.append({
            'id': challenge.id,
            'name': challenge.name,
            'description': challenge.description,
            'flags': [f.content for f in Flags.query.filter_by(challenge_id=challenge.id).all()],
            'solves': Solves.query.filter_by(challenge_id=challenge.id).count(),
            'fails': Fails.query.filter_by(challenge_id=challenge.id).count(),
        })
    print(json.dumps(out, ensure_ascii=False, indent=2))
PY

cat > /opt/cuh-ctf/challenges/hash_filtrado/DATOS_CTFD.md <<'EOF'
# Datos para CTFd: Hash filtrado

## Name
Hash filtrado

## Category
Cracking

## Value
160

## Type
standard

## State
visible

## Description
Se ha recuperado un archivo de laboratorio con una clave corta almacenada como hash fuera de linea. Descarga el archivo, identifica el algoritmo y recupera el PIN con una tecnica de cracking local y autorizada. No necesitas atacar servicios reales ni interactuar con infraestructura externa: todo ocurre en tu Kali Linux. Cuando obtengas el valor correcto, envialo como flag del evento usando el formato `CUH{pin_valor}`.

## Flag
`CUH{pin_2603}`

## Hints
1. Primero identifica que algoritmo estas viendo antes de elegir herramienta.
2. No busques un diccionario grande: la clave es un PIN numerico corto.
3. Un ataque por mascara o fuerza bruta offline es suficiente en este laboratorio.
EOF

cat > /opt/cuh-ctf/challenges/hash_filtrado/README_ORGANIZADOR.md <<'EOF'
# Reto: Hash filtrado

## Proposito didactico
Introducir cracking fuera de linea de hashes en un entorno academico controlado. El alumno debe identificar el algoritmo y recuperar un PIN debil de laboratorio sin tocar servicios reales.

## Archivo asociado
`/opt/cuh-ctf/challenges/hash_filtrado/hash_respaldo.txt`

## Resolucion esperada
1. Descargar el archivo desde CTFd.
2. Identificar el hash SHA-256.
3. Probar cracking offline de un PIN numerico corto con John o Hashcat.
4. Construir la respuesta final con el formato del evento y enviar `CUH{pin_2603}`.
EOF

cat > /opt/cuh-ctf/challenges/hash_filtrado/verificacion_local.md <<'EOF'
# Verificacion local: Hash filtrado

## Comprobaciones
```bash
cat /opt/cuh-ctf/challenges/hash_filtrado/hash_respaldo.txt
python3 - <<'PY2'
import hashlib
print(hashlib.sha256(b"2603").hexdigest())
PY2
```

## Resultado esperado
- El archivo existe y declara `algoritmo=sha256`.
- La suma calculada coincide con `hash=120e90dfb21d132a40c6281f8c8f25331969559e200f589bfe8e775e333b5b3a`.
- La flag esperada en CTFd es `CUH{pin_2603}`.
EOF

python3 - <<'PY'
from pathlib import Path
import json

api_flag = Path('/opt/cuh-ctf/artifacts/ctfd_api_payloads/flag_hash_filtrado.json')
if api_flag.exists():
    api_flag.write_text(json.dumps({"type":"static","content":"CUH{pin_2603}","data":""}, ensure_ascii=False, indent=2) + "\n", encoding='utf-8')

ctfcli = Path('/opt/cuh-ctf/artifacts/ctfcli/hash_filtrado/challenge.yml')
if ctfcli.exists():
    text = ctfcli.read_text(encoding='utf-8')
    text = text.replace('content: 2603', 'content: CUH{pin_2603}')
    ctfcli.write_text(text, encoding='utf-8')
PY

docker exec -i "${CTFD_CONTAINER}" python3 - <<'PY'
from datetime import datetime
from CTFd import create_app
from CTFd.models import Challenges, Flags, Solves, Fails, Users, Notifications, db

UPDATES = {
    'Calentamiento - Bienvenida': {
        'flag': 'CUH{cuh_ctf_2026_ok}',
        'description': """Este es el reto inicial de validación de la plataforma.

El objetivo es comprobar que el flujo completo funciona correctamente:
1. abrir el desafío,
2. enviar una bandera,
3. recibir puntos,
4. aparecer en el marcador.

Envía exactamente esta bandera:

`CUH{cuh_ctf_2026_ok}`

Si la plataforma acepta la bandera, el despliegue base quedó operativo.""",
    },
    'Hash filtrado': {
        'flag': 'CUH{pin_2603}',
        'description': """Se ha recuperado un archivo de laboratorio con una clave corta almacenada como hash fuera de linea. Descarga el archivo, identifica el algoritmo y recupera el PIN con una tecnica de cracking local y autorizada. No necesitas atacar servicios reales ni interactuar con infraestructura externa: todo ocurre en tu Kali Linux.

Cuando recuperes el valor correcto, envialo como flag del evento con el formato `CUH{pin_valor}`.""",
    },
}

NOTICE_TITLE = 'Actualización de formato de flags y reinicio de retos'
NOTICE_CONTENT = (
    'Se normalizó el formato de flags del evento para que todas usen CUH{...}. '
    'Por este motivo, las misiones "Calentamiento - Bienvenida" y "Hash filtrado" fueron actualizadas y reiniciadas. '
    'Si ya habías interactuado con alguna de ellas, vuelve a abrir el reto, revisa el nuevo formato de respuesta y envíalo nuevamente.'
)

app = create_app()

with app.app_context():
    affected_ids = []
    for name, spec in UPDATES.items():
        challenge = Challenges.query.filter_by(name=name).first()
        if not challenge:
            continue
        challenge.description = spec['description']
        Flags.query.filter_by(challenge_id=challenge.id).delete()
        db.session.add(Flags(challenge_id=challenge.id, type='static', content=spec['flag'], data=''))
        Solves.query.filter_by(challenge_id=challenge.id).delete()
        Fails.query.filter_by(challenge_id=challenge.id).delete()
        affected_ids.append(challenge.id)

    Notifications.query.filter_by(title=NOTICE_TITLE).delete()
    db.session.flush()
    users = Users.query.all()
    for user in users:
        db.session.add(Notifications(
            title=NOTICE_TITLE,
            content=NOTICE_CONTENT,
            user_id=user.id,
            team_id=None,
            date=datetime.utcnow(),
        ))
    db.session.commit()
    print('affected=' + ','.join(map(str, affected_ids)))
    print('notified_users=' + str(len(users)))
PY

docker exec -i "${CTFD_CONTAINER}" python3 - <<'PY' > "${BACKUP_DIR}/after.json"
import json
from CTFd import create_app
from CTFd.models import Challenges, Flags, Solves, Fails, Notifications

app = create_app()

with app.app_context():
    out = []
    for name in ['Calentamiento - Bienvenida', 'Hash filtrado']:
        challenge = Challenges.query.filter_by(name=name).first()
        if not challenge:
            continue
        out.append({
            'id': challenge.id,
            'name': challenge.name,
            'description': challenge.description,
            'flags': [f.content for f in Flags.query.filter_by(challenge_id=challenge.id).all()],
            'solves': Solves.query.filter_by(challenge_id=challenge.id).count(),
            'fails': Fails.query.filter_by(challenge_id=challenge.id).count(),
        })
    out.append({
        'notification_title': 'Actualización de formato de flags y reinicio de retos',
        'notification_count': Notifications.query.filter_by(title='Actualización de formato de flags y reinicio de retos').count()
    })
    print(json.dumps(out, ensure_ascii=False, indent=2))
PY
