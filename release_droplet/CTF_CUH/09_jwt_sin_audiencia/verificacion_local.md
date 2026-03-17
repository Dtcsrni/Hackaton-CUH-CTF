# Verificación local

Carpeta del reto: `09_jwt_sin_audiencia`

## Comando principal
```powershell
cd 09_jwt_sin_audiencia
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{jwt_con_validacion_completa}`.
- El archivo `jwt_sin_audiencia_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/jwt-sin-audiencia`.
