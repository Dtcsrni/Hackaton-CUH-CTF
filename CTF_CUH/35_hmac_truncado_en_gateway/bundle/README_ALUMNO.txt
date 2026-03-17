HMAC truncado en gateway
==========================

Objetivo
--------
Corrige la verificación de firma para que use HMAC-SHA256 completo y comparación segura.

Qué contiene el bundle
----------------------
Módulo Python del gateway, requisitos y validador.

Qué debes entregar
------------------
Edita `app/verifier.py` y ejecuta el validador.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
