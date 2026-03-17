Portal sin redirección segura
==========================

Objetivo
--------
Corrige la configuración de borde para que el portal deje de servirse por HTTP y fuerce HTTPS.

Qué contiene el bundle
----------------------
Configuración Nginx heredada, nota de despliegue, contexto del certificado y validador.

Qué debes entregar
------------------
Edita `infra/nginx.conf` y ejecuta el validador.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
