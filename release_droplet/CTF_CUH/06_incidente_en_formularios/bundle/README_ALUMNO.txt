Incidente en formularios
==========================

Objetivo
--------
Reconstruye el incidente y completa `respuesta.txt` con el vector, la cuenta afectada y el impacto.

Qué contiene el bundle
----------------------
Logs de aplicación, traza SQL, nota operativa y un validador local.

Qué debes entregar
------------------
Rellena `respuesta.txt` y ejecuta el validador.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
