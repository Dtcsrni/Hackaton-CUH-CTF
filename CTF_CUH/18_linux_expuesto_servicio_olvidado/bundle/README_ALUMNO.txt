Linux expuesto: servicio olvidado
==========================

Objetivo
--------
Endurece la unidad del servicio para ejecutarla con menos privilegios y menor superficie de exposición.

Qué contiene el bundle
----------------------
Archivo `.service`, inventario mínimo y validador.

Qué debes entregar
------------------
Edita `config/cuh-reportes.service` y ejecuta el validador.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
