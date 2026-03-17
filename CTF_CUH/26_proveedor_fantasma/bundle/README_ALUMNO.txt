Proveedor fantasma
==========================

Objetivo
--------
Identifica la entidad real, su dominio y la inconsistencia principal del expediente.

Qué contiene el bundle
----------------------
Factura, extracto de dominio, nota interna y validador.

Qué debes entregar
------------------
Completa `respuesta.txt` y ejecuta el validador.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
