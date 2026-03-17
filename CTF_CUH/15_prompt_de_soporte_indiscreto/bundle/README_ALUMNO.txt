Prompt de soporte indiscreto
==========================

Objetivo
--------
Rediseña el ensamblado del prompt para limitar alcance, redactar contexto sensible y rechazar solicitudes fuera de política.

Qué contiene el bundle
----------------------
Módulo Python del asistente y política base.

Qué debes entregar
------------------
Corrige `assistant/prompt_guard.py` y ejecuta el validador.

Cómo validarlo
--------------
Ejecuta:

```powershell
python tests\validate_fix.py
```

Si la corrección o el análisis es consistente, el validador imprimirá la flag.
