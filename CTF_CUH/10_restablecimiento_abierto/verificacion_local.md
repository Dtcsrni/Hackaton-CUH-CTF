# Verificación local

Carpeta del reto: `10_restablecimiento_abierto`

## Comando principal
```powershell
cd 10_restablecimiento_abierto
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{token_de_reset_endurecido}`.
- El archivo `restablecimiento_abierto_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/restablecimiento-abierto`.
