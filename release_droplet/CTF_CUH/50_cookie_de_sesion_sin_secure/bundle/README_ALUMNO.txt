Cookie de sesión sin Secure
==========================

Objetivo
--------
Endurece la configuración de sesión para que la cookie viaje solo por HTTPS y con atributos razonables.

Qué contiene el bundle
----------------------
Archivo de settings, nota de contexto y validador.

Qué debes entregar
------------------
Edita `app/settings.py` y ejecuta el validador.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
