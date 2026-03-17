Linux expuesto: sudoers heredado
==========================

Objetivo
--------
Reduce `sudoers` a los permisos operativos estrictamente necesarios.

Qué contiene el bundle
----------------------
Archivo `sudoers` heredado y validador local.

Qué debes entregar
------------------
Edita `config/sudoers` y valida localmente.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
