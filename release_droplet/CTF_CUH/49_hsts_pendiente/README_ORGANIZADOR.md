# HSTS pendiente

## Propósito didáctico
Reforzar el papel de HSTS como capa complementaria a TLS y a la redirección inicial.

## Dinámica de resolución
El alumno corrige el virtual host HTTPS y valida que la cabecera quede declarada con parámetros sólidos.

## Material del alumno
- Bundle final: `hsts_pendiente_bundle.zip`
- Página de apoyo: `/hsts-pendiente`

## Validación del organizador
1. Ejecuta `python verify_organizer.py` dentro de esta carpeta.
2. Confirma que el validador devuelve `CUH{hsts_define_la_politica_de_transporte}`.
3. Sube el ZIP a CTFd como archivo descargable del reto.
4. Verifica que la página de apoyo publique el contexto correcto.

## Nota pedagógica
Reto de hardening orientado a cabeceras de transporte, útil para despliegues institucionales.
