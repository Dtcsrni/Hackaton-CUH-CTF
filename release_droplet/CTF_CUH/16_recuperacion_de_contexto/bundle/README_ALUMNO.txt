Recuperación de contexto
==========================

Objetivo
--------
Identifica la causa de la fuga, el dato expuesto y la mitigación principal.

Qué contiene el bundle
----------------------
Trazas del asistente, nota de contexto y validador.

Qué debes entregar
------------------
Completa `respuesta.txt` y ejecútalo contra el validador.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
