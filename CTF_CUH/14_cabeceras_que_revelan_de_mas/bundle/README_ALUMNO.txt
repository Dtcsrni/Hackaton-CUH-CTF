Cabeceras que revelan de más
==========================

Objetivo
--------
Endurece la configuración web eliminando exposición innecesaria y definiendo políticas de seguridad razonables.

Qué contiene el bundle
----------------------
Fragmento de configuración nginx y validador local.

Qué debes entregar
------------------
Edita `config/nginx.conf` y ejecuta el validador.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
