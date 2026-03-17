Licencia bajo revisión
==========================

Objetivo
--------
Recupera la licencia exacta que el ejecutable considera válida.

Qué contiene el bundle
----------------------
Binario PE, nota breve y validador de respuesta.

Qué debes entregar
------------------
Escribe la licencia en `respuesta.txt` y valida localmente.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
