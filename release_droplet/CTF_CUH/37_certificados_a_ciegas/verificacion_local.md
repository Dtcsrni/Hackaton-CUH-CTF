# Verificación local

Carpeta del reto: `37_certificados_a_ciegas`

## Comando principal
```powershell
cd 37_certificados_a_ciegas
python verify_organizer.py
```

## Resultado esperado
- El script debe devolver `OK`.
- La salida del validador debe incluir `CUH{tls_validado_con_ca_y_hostname}`.
- El archivo `certificados_a_ciegas_bundle.zip` debe existir y abrir correctamente.

## Comprobaciones extra
- El bundle no debe incluir `solutions/`.
- El bundle sí debe incluir `README_ALUMNO.txt`.
- El material de apoyo publicado debe resolver en `/certificados-a-ciegas`.
