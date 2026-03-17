CBC sin integridad
==========================

Objetivo
--------
Identifica el modo de operación, el riesgo principal y la mitigación adecuada.

Qué contiene el bundle
----------------------
Ciphertext, nota de integración, observación del SOC y validador.

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
