# Verificación local

Carpeta del reto: `29_firma_reciclada`

## Comando principal
```powershell
cd 29_firma_reciclada
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{firma_con_nonce_repetido_detectada}`.
- El archivo `firma_reciclada_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/firma-reciclada`.
