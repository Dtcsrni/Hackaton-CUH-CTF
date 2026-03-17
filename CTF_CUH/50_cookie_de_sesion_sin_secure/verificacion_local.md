# Verificación local

Carpeta del reto: `50_cookie_de_sesion_sin_secure`

## Comando principal
```powershell
cd 50_cookie_de_sesion_sin_secure
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{cookies_de_sesion_solo_por_https}`.
- El archivo `cookie_de_sesion_sin_secure_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/cookie-de-sesion-sin-secure`.
