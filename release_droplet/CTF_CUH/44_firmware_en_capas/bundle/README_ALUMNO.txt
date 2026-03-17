Firmware en capas
==========================

Objetivo
--------
Identifica la herramienta adecuada, el artefacto embebido útil y el hallazgo operativo derivado.

Qué contiene el bundle
----------------------
Salida de scan, extracto residual, nota de equipo y validador.

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
