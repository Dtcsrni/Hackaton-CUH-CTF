# Firma reciclada

## Propósito didáctico
Practicar análisis de trazas de firma y detección de nonces repetidos.

## Dinámica de resolución
El alumno revisa logs y nota de contexto, luego sintetiza la respuesta en tres campos.

## Material del alumno
- Bundle final: `firma_reciclada_bundle.zip`
- Página de apoyo: `/firma-reciclada`

## Validación del organizador
1. Ejecuta `python verify_organizer.py` dentro de esta carpeta.
2. Confirma que el validador devuelve `CUH{firma_con_nonce_repetido_detectada}`.
3. Sube el ZIP a CTFd como archivo descargable del reto.
4. Verifica que la página de apoyo publique el contexto correcto.

## Nota pedagógica
Reto de análisis defensivo; no requiere reproducir firmas ni extraer claves reales.
