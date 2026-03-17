# Firmware en capas

## Propósito didáctico
Practicar triage de firmware y lectura de artefactos embebidos con herramientas habituales de Kali.

## Dinámica de resolución
El alumno interpreta el scan, selecciona el artefacto útil y explica el hallazgo operativo.

## Material del alumno
- Bundle final: `firmware_en_capas_bundle.zip`
- Página de apoyo: `/firmware-en-capas`

## Validación del organizador
1. Ejecuta `python verify_organizer.py` dentro de esta carpeta.
2. Confirma que el validador devuelve `CUH{binwalk_descubre_el_resto_olvidado}`.
3. Sube el ZIP a CTFd como archivo descargable del reto.
4. Verifica que la página de apoyo publique el contexto correcto.

## Nota pedagógica
Reto de análisis por capas orientado a priorización de hallazgos.
