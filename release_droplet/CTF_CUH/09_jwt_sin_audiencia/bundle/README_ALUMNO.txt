JWT sin audiencia
==========================

Objetivo
--------
Endurece el validador JWT para restringir algoritmo, issuer, audience y expiración.

Qué contiene el bundle
----------------------
Módulo Python y nota de claims esperadas.

Qué debes entregar
------------------
Edita `app/jwt_validator.py` y valida localmente.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
