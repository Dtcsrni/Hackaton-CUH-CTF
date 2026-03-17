# Verificación local

Carpeta del reto: `33_cbc_sin_integridad`

## Comando principal
```powershell
cd 33_cbc_sin_integridad
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{cbc_sin_integridad_identificada}`.
- El archivo `cbc_sin_integridad_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/cbc-sin-integridad`.
