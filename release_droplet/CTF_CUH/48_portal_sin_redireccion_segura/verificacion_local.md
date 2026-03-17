# Verificación local

Carpeta del reto: `48_portal_sin_redireccion_segura`

## Comando principal
```powershell
cd 48_portal_sin_redireccion_segura
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{https_obligatorio_desde_el_borde}`.
- El archivo `portal_sin_redireccion_segura_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/portal-sin-redireccion-segura`.
