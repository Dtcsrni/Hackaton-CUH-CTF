# Credenciales expuestas en tránsito

## Propósito didáctico
Practicar reconstrucción de incidentes ligados a autenticación expuesta por HTTP durante migraciones a HTTPS.

## Dinámica de resolución
El alumno cruza traza, logs y nota del SOC para responder con portal, ruta e impacto.

## Material del alumno
- Bundle final: `credenciales_expuestas_en_transito_bundle.zip`
- Página de apoyo: `/credenciales-expuestas-en-transito`

## Validación del organizador
1. Ejecuta `python verify_organizer.py` dentro de esta carpeta.
2. Confirma que el validador devuelve `CUH{credenciales_expuestas_por_http_reconstruidas}`.
3. Sube el ZIP a CTFd como archivo descargable del reto.
4. Verifica que la página de apoyo publique el contexto correcto.

## Nota pedagógica
Reto forense y pedagógico sobre consecuencias de no cerrar HTTP a tiempo en rutas sensibles.
