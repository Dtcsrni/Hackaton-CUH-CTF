RSA sin OAEP
==========================

Objetivo
--------
Migra el descifrado RSA a OAEP con SHA-256 y deja el módulo en un formato claro.

Qué contiene el bundle
----------------------
Módulo Python y política criptográfica del servicio.

Qué debes entregar
------------------
Edita `app/rsa_guard.py` y ejecuta el validador.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
