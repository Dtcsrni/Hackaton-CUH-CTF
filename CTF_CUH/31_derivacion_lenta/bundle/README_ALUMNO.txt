Derivación lenta
==========================

Objetivo
--------
Reemplaza la derivación rápida por PBKDF2-HMAC-SHA256 con sal aleatoria e iteraciones explícitas.

Qué contiene el bundle
----------------------
Módulo Python y requisitos de la política nueva.

Qué debes entregar
------------------
Edita `app/passwords.py` y ejecuta el validador.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
