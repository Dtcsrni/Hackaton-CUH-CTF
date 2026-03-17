# Reto 2: Comandos Linux - búsqueda básica

## Propósito didáctico
Este reto reduce fricción al inicio del hackathon y enseña a trabajar con archivos comprimidos, navegación de directorios y búsqueda básica en Linux dentro de un laboratorio académico controlado.

## Cómo generar el ZIP en Windows
Ubicación del script:

`CTF_CUH/02_comandos_linux_busqueda_basica/crear_zip.ps1`

Ejecución recomendada:

```powershell
cd O:\Descargas\hackaton\CTF_CUH\02_comandos_linux_busqueda_basica
powershell -ExecutionPolicy Bypass -File .\crear_zip.ps1
```

También puede ejecutarse desde una sesión moderna de PowerShell abierta en esa carpeta:

```powershell
.\crear_zip.ps1
```

## Dónde queda el ZIP final
El archivo se genera en:

`O:\Descargas\hackaton\CTF_CUH\02_comandos_linux_busqueda_basica\reto_archivos_linux.zip`

## Cómo subirlo a CTFd
1. Genere el ZIP con `crear_zip.ps1`.
2. Cree el reto en CTFd con los datos de [DATOS_CTFD.md](./DATOS_CTFD.md).
3. Adjunte `reto_archivos_linux.zip` como archivo descargable del reto.
4. Verifique desde una cuenta de prueba que el archivo se descarga completo.

## Cómo verificar que la estructura interna es correcta
El ZIP debe contener la carpeta raíz `reto_linux` y la siguiente estructura:

```text
reto_linux/
reto_linux/README.txt
reto_linux/notas/sistema.log
reto_linux/notas/usuarios.txt
reto_linux/evidencia/instrucciones.txt
reto_linux/evidencia/pista.tmp
reto_linux/evidencia/oculto/flag.txt
```

## Cómo probarlo desde Kali
Ejemplo de flujo esperado:

```bash
unzip reto_archivos_linux.zip
cd reto_linux
find . -type f
grep -R "CUH{" .
cat ./evidencia/oculto/flag.txt
```

## Errores comunes
- El ZIP se sube sin regenerarlo después de editar archivos.
- El script se ejecuta fuera de su carpeta y el organizador revisa otro archivo por error.
- Se comprime el contenido interno de `reto_linux` sin la carpeta raíz, cambiando la experiencia del alumno.
- El archivo descargado en CTFd quedó corrupto o incompleto.

## Criterios de validación antes del evento
- `crear_zip.ps1` genera `reto_archivos_linux.zip` sin errores.
- El ZIP contiene exactamente la carpeta `reto_linux` con la estructura esperada.
- `flag.txt` contiene `CUH{linux_tambien_se_investiga}`.
- La descripción de CTFd no revela la ruta exacta de la flag.
- Un alumno de prueba puede resolverlo solo con herramientas básicas de Linux.
