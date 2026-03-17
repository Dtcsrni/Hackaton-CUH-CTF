HSTS pendiente
==========================

Objetivo
--------
Completa la política HSTS del portal para que el navegador mantenga el uso de HTTPS.

Qué contiene el bundle
----------------------
Virtual host HTTPS, nota de contexto y validador.

Qué debes entregar
------------------
Edita `infra/site.conf` y ejecuta el validador.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
