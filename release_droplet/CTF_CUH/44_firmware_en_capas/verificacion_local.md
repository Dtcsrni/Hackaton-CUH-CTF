# Verificación local

Carpeta del reto: `44_firmware_en_capas`

## Comando principal
```powershell
cd 44_firmware_en_capas
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{binwalk_descubre_el_resto_olvidado}`.
- El archivo `firmware_en_capas_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/firmware-en-capas`.
