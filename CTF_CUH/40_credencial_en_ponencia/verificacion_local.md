# Verificación local

Carpeta del reto: `40_credencial_en_ponencia`

## Comando principal
```powershell
cd 40_credencial_en_ponencia
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{credencial_en_ponencia_correlacionada}`.
- El archivo `credencial_en_ponencia_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/credencial-en-ponencia`.
