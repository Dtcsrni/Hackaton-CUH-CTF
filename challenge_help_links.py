from __future__ import annotations

import json
from pathlib import Path


MANUAL_HELP_LINKS: dict[str, tuple[str, str]] = {
    "Calentamiento - Bienvenida": ("inicio-rapido", "Inicio rápido del laboratorio"),
    "Leer también es hacking": ("inicio-rapido", "Inicio rápido del laboratorio"),
    "Robots curiosos": ("guia-herramientas", "Guía de herramientas"),
    "Base64 no es cifrado": ("cracking-lab", "Notas internas sobre cracking"),
    "César escolar": ("cracking-lab", "Notas internas sobre cracking"),
    "Puertas abiertas": ("inventario-lab", "Inventario interno del laboratorio"),
    "Metadatos indiscretos": ("analisis-archivos", "Guía interna de análisis de archivos"),
    "Comandos Linux - búsqueda básica": ("analisis-archivos", "Guía interna de análisis de archivos"),
    "Logo en observación": ("analisis-archivos", "Guía interna de análisis de archivos"),
    "Portada con pista": ("analisis-archivos", "Guía interna de análisis de archivos"),
    "Cabeceras del laboratorio": ("inventario-lab", "Inventario interno del laboratorio"),
    "JSON de prueba": ("inventario-lab", "Inventario interno del laboratorio"),
    "Bitácora del proxy": ("analisis-archivos", "Guía interna de análisis de archivos"),
    "Hash filtrado": ("cracking-lab", "Notas internas sobre cracking"),
    "ZIP bajo llave": ("cracking-lab", "Notas internas sobre cracking"),
    "Acceso heredado": ("credenciales-legado", "Notas internas sobre credenciales heredadas"),
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


REQUIRED_INLINE_ARTIFACTS: dict[str, tuple[str, ...]] = {
    "Base64 no es cifrado": ("Cadena Base64:", "Mensaje Base64:", "Texto a decodificar:"),
    "César escolar": ("Texto cifrado:", "Mensaje cifrado:", "Cadena desplazada:"),
}


def _load_safe_help_links() -> dict[str, tuple[str, str]]:
    manifest_path = Path(__file__).resolve().parent / "refresh_assets" / "generated_safe_pages.json"
    if not manifest_path.exists():
        return {}

    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    links: dict[str, tuple[str, str]] = {}
    for challenge_name, meta in payload.get("links", {}).items():
        route = (meta or {}).get("route")
        label = (meta or {}).get("label")
        if route and label:
            links[challenge_name] = (route, label)
    return links


HELP_LINKS: dict[str, tuple[str, str]] = {**_load_safe_help_links(), **MANUAL_HELP_LINKS}
