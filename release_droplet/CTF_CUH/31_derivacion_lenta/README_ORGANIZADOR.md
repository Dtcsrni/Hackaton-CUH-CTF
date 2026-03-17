# Derivación lenta

## Propósito didáctico
Practicar migración desde hashes rápidos hacia KDFs adecuadas para credenciales.

## Dinámica de resolución
El alumno corrige el módulo de derivación y valida la nueva política.

## Material del alumno
- Bundle final: `derivacion_lenta_bundle.zip`
- Página de apoyo: `/derivacion-lenta`

## Validación del organizador
1. Ejecuta `python verify_organizer.py` dentro de esta carpeta.
2. Confirma que el validador devuelve `CUH{kdf_endurecida_con_pbkdf2}`.
3. Sube el ZIP a CTFd como archivo descargable del reto.
4. Verifica que la página de apoyo publique el contexto correcto.

## Nota pedagógica
Reto de parche local con foco en almacenamiento seguro de secretos.
