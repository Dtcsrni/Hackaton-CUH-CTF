# Verificación local

Carpeta del reto: `16_recuperacion_de_contexto`

## Comando principal
```powershell
cd 16_recuperacion_de_contexto
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{contexto_filtrado_y_mitigado}`.
- El archivo `recuperacion_de_contexto_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/recuperacion-de-contexto`.
