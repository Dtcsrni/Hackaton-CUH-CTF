Consulta concatenada
==========================

Objetivo
--------
Corrige el login para que deje de construir la consulta SQL concatenando usuario y clave.

Qué contiene el bundle
----------------------
Código PHP heredado, esquema de referencia y un validador local.

Qué debes entregar
------------------
Edita `app/login.php` y vuelve a ejecutar el validador hasta obtener la flag.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
