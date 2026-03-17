Firma reciclada
==========================

Objetivo
--------
Identifica la causa del fallo de firma, la clave afectada y la mitigación principal.

Qué contiene el bundle
----------------------
Logs de firma, nota criptográfica y validador.

Qué debes entregar
------------------
Completa `respuesta.txt` y ejecútalo contra el validador.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
