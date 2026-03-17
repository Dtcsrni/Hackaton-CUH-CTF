from __future__ import annotations

from pathlib import Path

from CTFd import create_app
from CTFd.models import ChallengeFiles, Challenges, db

from challenge_help_links import HELP_LINKS
from challenge_description_overrides import DESCRIPTIONS, EXPECTED_CHALLENGE_COUNT


SPECIAL_INPUT_NOTES = {
    "Base64 no es cifrado": [
        "La cadena o valor que debes revisar ya está en la propia plataforma; no hay un archivo oculto aparte.",
        "No necesitas una clave externa: la pista correcta es reconocer que Base64 es una codificación reversible y no un cifrado.",
    ],
    "César escolar": [
        "El mensaje a analizar está ya dentro del reto; no depende de material adicional.",
        "No hay una clave entregada por separado. Debes inferir el desplazamiento correcto a partir de una salida legible y del formato de la flag.",
    ],
    "Fuente principal": [
        "Todo el insumo operativo está en el HTML y en los recursos enlazados por la propia página.",
        "No necesitas adjuntos ni credenciales externas: basta con revisar el documento y sus referencias con cuidado.",
    ],
    "Consola curiosa": [
        "La evidencia útil aparece en la consola del navegador durante la carga normal del reto.",
        "No hay un archivo extra que descargar; el insumo correcto es abrir la herramienta adecuada y observar el comportamiento del frontend.",
    ],
    "Cookie de rol": [
        "El insumo principal es la cookie y cómo la aplicación la usa entre peticiones; no hay material descargable.",
        "No necesitas adivinar rutas externas: el propio flujo del reto expone la pista importante.",
    ],
    "JSON de prueba": [
        "El insumo clave es la respuesta JSON del recurso que el propio sitio expone en el reto.",
        "No hace falta una clave o archivo aparte; lo importante es interpretar bien los campos de la respuesta.",
    ],
    "Calentamiento - Bienvenida": [
        "La flag está dentro de la propia plataforma y no depende de ninguna descarga.",
        "No necesitas herramientas externas: aquí la observación cuidadosa es suficiente.",
    ],
    "Leer también es hacking": [
        "Todo lo necesario está en el texto y en la información ya visible dentro de la plataforma.",
        "No hay clave ni adjunto oculto: la dificultad está en leer con atención, no en forzar el reto.",
    ],
    "Rompe el sistema": [
        "La validación de este reto es manual y depende del reporte revisado por la organización.",
        "No se resuelve desde el tablero público ni requiere adjuntos descargables.",
    ],
}


def _dedupe_lines(lines: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for line in lines:
        cleaned = line.strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        ordered.append(cleaned)
    return ordered


def build_attachment_section(challenge_id: int) -> tuple[list[str], list[str]]:
    files = ChallengeFiles.query.filter_by(challenge_id=challenge_id).all()
    if not files:
        return (
            ["Este desafío no depende de adjuntos descargables."],
            ["Todo lo necesario está en la propia plataforma, en la guía enlazada o en el flujo del reto."],
        )

    names = [Path(item.location or "").name for item in files if item.location]
    visible_names = [name for name in names if name]
    if not visible_names:
        return (
            ["Descarga el material adjunto desde la sección de archivos del desafío antes de empezar."],
            ["El material adjunto forma parte de la resolución esperada."],
        )

    rendered = ", ".join(f"`{name}`" for name in visible_names)
    return (
        [f"Descarga {rendered} desde la sección de archivos del desafío."],
        ["Ese material forma parte de la resolución esperada."],
    )


def build_input_lines(challenge: Challenges, attachment_lines: list[str], attachment_support: list[str]) -> list[str]:
    category = (challenge.category or "").strip()
    lines: list[str] = []

    if attachment_lines and "no depende de adjuntos" not in attachment_lines[0].lower():
        lines.extend(attachment_lines)
    elif category in {"Web", "Auth", "Reconocimiento"}:
        lines.append(
            "El insumo operativo está en la propia plataforma: HTML, respuestas HTTP, comportamiento del flujo, cookies o elementos visibles del navegador según el caso."
        )
    elif category == "Criptografía":
        lines.append(
            "La cadena, mensaje o artefacto que debes analizar ya está en el propio reto o en el material que este mismo desafío entrega."
        )
    elif category in {"Forense", "OSINT"}:
        lines.append(
            "La evidencia útil está en el material del reto o en los artefactos ya expuestos por la propia plataforma; no hace falta salir del contexto del laboratorio."
        )
    elif category in {"Linux", "Windows"}:
        lines.append(
            "Debes trabajar sobre la configuración, evidencias o artefactos previstos por el reto, sin asumir infraestructura adicional fuera del material entregado."
        )
    elif category in {"Cracking", "Reversing"}:
        lines.append(
            "El reto se resuelve con el artefacto o servicio ya indicado por la propia misión; no depende de datos secretos entregados por fuera."
        )
    else:
        lines.append(
            "Todo lo necesario para avanzar está dentro del propio reto, sus archivos adjuntos o la guía enlazada."
        )

    if getattr(challenge, "connection_info", None):
        lines.append(f"Si el reto muestra datos de conexión, ese punto de entrada forma parte del laboratorio previsto: `{challenge.connection_info}`.")

    lines.extend(attachment_support)
    lines.extend(SPECIAL_INPUT_NOTES.get(challenge.name, []))
    return _dedupe_lines(lines)


def build_goal_lines(challenge: Challenges) -> list[str]:
    category = (challenge.category or "").strip()
    if challenge.name == "Rompe el sistema":
        return [
            "La misión se cierra cuando la organización valida el hallazgo y acredita manualmente la flag correspondiente.",
        ]
    if category in {"Web", "Auth", "Reconocimiento"}:
        return [
            "La resolución se considera completa cuando identificas el hallazgo correcto dentro del flujo previsto y recuperas la flag final del reto.",
        ]
    if category in {"Forense", "OSINT"}:
        return [
            "La misión se cierra cuando correlacionas la evidencia correcta, descartas falsos positivos y entregas la flag final en formato `CUH{...}`.",
        ]
    if category in {"Criptografía", "Cracking", "Reversing"}:
        return [
            "El reto queda completo cuando aplicas la transformación, análisis o validación correcta y recuperas la flag final en formato `CUH{...}`.",
        ]
    if category in {"Linux", "Windows"}:
        return [
            "La misión se cierra cuando corriges o interpretas el material del laboratorio con el criterio técnico esperado y obtienes la flag final en formato `CUH{...}`.",
        ]
    return [
        "Entrega la flag final en formato `CUH{...}` cuando hayas validado el criterio técnico correcto del reto.",
    ]


def build_clarification_lines(challenge: Challenges) -> list[str]:
    lines = []
    if challenge.value and challenge.value > 200:
        lines.append(
            "Si completas el reto en menos de `5 minutos`, la plataforma puede pedir al menos `4 evidencias` del proceso antes de permitir nuevas entregas."
        )
    if challenge.state == "hidden":
        lines.append("Este reto no forma parte del tablero público y solo aparece por asignación expresa de la organización.")
    return _dedupe_lines(lines)


def build_help_lines(challenge: Challenges) -> list[str]:
    route_label = HELP_LINKS.get(challenge.name)
    if route_label is None:
        return []

    route, label = route_label
    return [
        f"Consulta la guía relacionada [{label}](/{route}).",
        "Usa ese material como apoyo operativo; la resolución final sigue estando en el reto, su flujo o sus archivos.",
    ]


def render_section(title: str, lines: list[str]) -> str:
    clean_lines = _dedupe_lines(lines)
    if not clean_lines:
        return ""
    items = "\n".join(f"- {line}" for line in clean_lines)
    return f"### {title}\n{items}"


def main() -> None:
    app = create_app()
    with app.app_context():
        missing = []
        missing_help_links = []
        updated = 0
        for name, description in DESCRIPTIONS.items():
            challenge = Challenges.query.filter_by(name=name).first()
            if challenge is None:
                missing.append(name)
                continue
            if name not in HELP_LINKS:
                missing_help_links.append(name)

            attachment_lines, attachment_support = build_attachment_section(challenge.id)
            sections = [
                render_section("Insumos disponibles", build_input_lines(challenge, attachment_lines, attachment_support)),
                render_section("Objetivo de cierre", build_goal_lines(challenge)),
                render_section("Archivos del reto", attachment_lines),
                render_section("Material de apoyo", build_help_lines(challenge)),
                render_section("Aclaraciones clave", build_clarification_lines(challenge)),
            ]
            rendered_sections = "\n\n".join(section for section in sections if section)
            challenge.description = f"{description}\n\n{rendered_sections}"
            updated += 1

        if missing:
            raise SystemExit(f"Challenges without DB row: {missing}")
        if missing_help_links:
            raise SystemExit(f"Challenges without help link mapping: {missing_help_links}")

        db.session.commit()
        print(f"descriptions updated {updated}")
        if updated != EXPECTED_CHALLENGE_COUNT:
            raise SystemExit(
                f"Expected {EXPECTED_CHALLENGE_COUNT} updated challenges, got {updated}"
            )


if __name__ == "__main__":
    main()
