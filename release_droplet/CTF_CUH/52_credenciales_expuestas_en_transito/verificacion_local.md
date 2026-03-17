# Verificación local

Carpeta del reto: `52_credenciales_expuestas_en_transito`

## Comando principal
```powershell
cd 52_credenciales_expuestas_en_transito
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{credenciales_expuestas_por_http_reconstruidas}`.
- El archivo `credenciales_expuestas_en_transito_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/credenciales-expuestas-en-transito`.
