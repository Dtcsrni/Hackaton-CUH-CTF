# Verificación local

Carpeta del reto: `27_huella_de_publicacion`

## Comando principal
```powershell
cd 27_huella_de_publicacion
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{huella_de_publicacion_reconstruida}`.
- El archivo `huella_de_publicacion_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/huella-de-publicacion`.
