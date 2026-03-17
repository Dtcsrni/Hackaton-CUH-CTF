# Verificación local

Carpeta del reto: `19_windows_expuesto_share_legado`

## Comando principal
```powershell
cd 19_windows_expuesto_share_legado
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{share_legado_reducido}`.
- El archivo `windows_expuesto_share_legado_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/windows-expuesto-share-legado`.
