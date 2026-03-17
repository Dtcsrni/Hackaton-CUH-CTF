# Verificación local

Carpeta del reto: `30_rsa_sin_oaep`

## Comando principal
```powershell
cd 30_rsa_sin_oaep
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{rsa_con_oaep_y_sha256}`.
- El archivo `rsa_sin_oaep_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/rsa-sin-oaep`.
