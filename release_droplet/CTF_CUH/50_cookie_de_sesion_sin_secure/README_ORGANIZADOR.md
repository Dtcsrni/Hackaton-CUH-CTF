# Cookie de sesión sin Secure

## Propósito didáctico
Practicar hardening de cookies de sesión después de una migración a HTTPS.

## Dinámica de resolución
El alumno revisa la configuración del framework, ajusta atributos de sesión y valida el resultado localmente.

## Material del alumno
- Bundle final: `cookie_de_sesion_sin_secure_bundle.zip`
- Página de apoyo: `/cookie-de-sesion-sin-secure`

## Validación del organizador
1. Ejecuta `python verify_organizer.py` dentro de esta carpeta.
2. Confirma que el validador devuelve `CUH{cookies_de_sesion_solo_por_https}`.
3. Sube el ZIP a CTFd como archivo descargable del reto.
4. Verifica que la página de apoyo publique el contexto correcto.

## Nota pedagógica
Reto seguro de configuración en capa de aplicación, alineado con despliegues web reales.
