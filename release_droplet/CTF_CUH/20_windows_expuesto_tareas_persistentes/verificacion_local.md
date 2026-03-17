# Verificación local

Carpeta del reto: `20_windows_expuesto_tareas_persistentes`

## Comando principal
```powershell
cd 20_windows_expuesto_tareas_persistentes
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{persistencia_en_tareas_reconstruida}`.
- El archivo `windows_expuesto_tareas_persistentes_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/windows-expuesto-tareas-persistentes`.
