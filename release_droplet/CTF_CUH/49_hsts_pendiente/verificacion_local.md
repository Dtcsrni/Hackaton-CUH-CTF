# Verificación local

Carpeta del reto: `49_hsts_pendiente`

## Comando principal
```powershell
cd 49_hsts_pendiente
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{hsts_define_la_politica_de_transporte}`.
- El archivo `hsts_pendiente_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/hsts-pendiente`.
