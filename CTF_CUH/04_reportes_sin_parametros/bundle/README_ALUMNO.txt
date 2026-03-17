Reportes sin parámetros
==========================

Objetivo
--------
Corrige el filtro de búsqueda para que el término no se incruste directamente dentro del SQL.

Qué contiene el bundle
----------------------
Backend PHP, esquema de apoyo y validador local.

Qué debes entregar
------------------
Edita `app/reportes.php` y ejecuta el validador.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
