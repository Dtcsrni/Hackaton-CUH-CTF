XOR de respaldo
==========================

Objetivo
--------
Identifica el problema criptográfico del respaldo, recupera la frase sensible y explica qué evidencia lo delata.

Qué contiene el bundle
----------------------
Dos salidas cifradas, una nota operativa y un validador.

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
