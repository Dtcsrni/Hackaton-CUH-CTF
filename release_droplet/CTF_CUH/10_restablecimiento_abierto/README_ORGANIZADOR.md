# Restablecimiento abierto

## Propósito didáctico
Practicar hardening de un flujo de restablecimiento de contraseñas.

## Dinámica de resolución
El alumno corrige un módulo Python y valida que emita y verifique tokens de forma razonable.

## Material del alumno
- Bundle final: `restablecimiento_abierto_bundle.zip`
- Página de apoyo: `/restablecimiento-abierto`

## Validación del organizador
1. Ejecuta `python verify_organizer.py` dentro de esta carpeta.
2. Confirma que el validador devuelve `CUH{token_de_reset_endurecido}`.
3. Sube el ZIP a CTFd como archivo descargable del reto.
4. Verifica que la página de apoyo publique el contexto correcto.

## Nota pedagógica
No hay correo ni infraestructura externa; el reto se centra en diseño de tokens.
