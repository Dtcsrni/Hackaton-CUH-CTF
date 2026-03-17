IV reciclado en reportes
==========================

Objetivo
--------
Identifica el problema criptográfico, el hallazgo observable y la mitigación correcta.

Qué contiene el bundle
----------------------
Dos ciphertexts, IV declarado, contexto del lote y validador.

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
