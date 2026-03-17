Portal PHP heredado
==========================

Objetivo
--------
Corrige el flujo heredado del portal para que consulte de forma segura y valide contraseñas con un mecanismo actual.

Qué contiene el bundle
----------------------
Backend PHP heredado y un validador local.

Qué debes entregar
------------------
Edita `app/auth.php` hasta que el validador devuelva la flag.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
