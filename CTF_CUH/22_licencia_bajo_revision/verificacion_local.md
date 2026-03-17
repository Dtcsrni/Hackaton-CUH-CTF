# Verificación local

Carpeta del reto: `22_licencia_bajo_revision`

## Comando principal
```powershell
cd 22_licencia_bajo_revision
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{licencia_reconstruida_sin_parche}`.
- El archivo `licencia_bajo_revision_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/licencia-bajo-revision`.
