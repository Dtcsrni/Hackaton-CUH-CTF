# Verificación local

Carpeta del reto: `51_contenido_mixto_heredado`

## Comando principal
```powershell
cd 51_contenido_mixto_heredado
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{todos_los_recursos_van_por_https}`.
- El archivo `contenido_mixto_heredado_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/contenido-mixto-heredado`.
