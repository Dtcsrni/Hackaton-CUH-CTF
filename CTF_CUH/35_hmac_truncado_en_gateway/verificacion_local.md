# Verificación local

Carpeta del reto: `35_hmac_truncado_en_gateway`

## Comando principal
```powershell
cd 35_hmac_truncado_en_gateway
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{gateway_hmac_verificado_completo}`.
- El archivo `hmac_truncado_en_gateway_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/hmac-truncado-en-gateway`.
