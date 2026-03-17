# Portal sin redirección segura

## Propósito didáctico
Practicar endurecimiento de reverse proxy cuando un portal todavía no obliga a usar HTTPS.

## Dinámica de resolución
El alumno corrige el archivo de Nginx, valida redirección y listener seguro, y ejecuta el validador local.

## Material del alumno
- Bundle final: `portal_sin_redireccion_segura_bundle.zip`
- Página de apoyo: `/portal-sin-redireccion-segura`

## Validación del organizador
1. Ejecuta `python verify_organizer.py` dentro de esta carpeta.
2. Confirma que el validador devuelve `CUH{https_obligatorio_desde_el_borde}`.
3. Sube el ZIP a CTFd como archivo descargable del reto.
4. Verifica que la página de apoyo publique el contexto correcto.

## Nota pedagógica
Reto seguro de configuración. No requiere servicio desplegado; el aprendizaje está en la revisión y el parche del archivo.
