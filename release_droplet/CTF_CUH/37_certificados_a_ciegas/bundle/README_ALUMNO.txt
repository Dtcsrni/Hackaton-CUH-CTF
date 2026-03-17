Certificados a ciegas
==========================

Objetivo
--------
Endurece el cliente TLS para validar cadena y hostname con la CA interna.

Qué contiene el bundle
----------------------
Módulo TLS, CA interna sintética y validador.

Qué debes entregar
------------------
Edita `app/client_tls.py` y ejecuta el validador.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
