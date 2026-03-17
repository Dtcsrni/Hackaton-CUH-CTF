Credenciales expuestas en tránsito
==========================

Objetivo
--------
Reconstruye el incidente de autenticación por HTTP y resume portal, ruta e impacto principal.

Qué contiene el bundle
----------------------
Resumen de tráfico, log del proxy, nota del SOC y validador.

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
