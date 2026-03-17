# Verificación local del reto Comandos Linux - búsqueda básica

## Pasos exactos para generar el ZIP
1. Abrir PowerShell en `O:\Descargas\hackaton\CTF_CUH\02_comandos_linux_busqueda_basica`.
2. Ejecutar:

```powershell
.\crear_zip.ps1
```

3. Confirmar que existe `reto_archivos_linux.zip` en la misma carpeta.

## Pasos exactos para validar que contiene la estructura correcta
1. Listar el contenido del ZIP desde PowerShell:

```powershell
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::OpenRead('O:\Descargas\hackaton\CTF_CUH\02_comandos_linux_busqueda_basica\reto_archivos_linux.zip').Entries | Select-Object -ExpandProperty FullName
```

2. Confirmar que aparecen estas rutas:

```text
reto_linux/README.txt
reto_linux/notas/sistema.log
reto_linux/notas/usuarios.txt
reto_linux/evidencia/instrucciones.txt
reto_linux/evidencia/pista.tmp
reto_linux/evidencia/oculto/flag.txt
```

## Comandos Linux esperados

```bash
unzip reto_archivos_linux.zip
cd reto_linux
find . -type f
grep -R "CUH{" .
cat ./evidencia/oculto/flag.txt
```

## Resultado esperado de cada comando
### `unzip reto_archivos_linux.zip`
Debe crear la carpeta `reto_linux` con subdirectorios `notas` y `evidencia`.

### `cd reto_linux`
Debe ubicar al alumno en la raíz del material del reto.

### `find . -type f`
Debe listar todos los archivos y permitir descubrir la ruta `./evidencia/oculto/flag.txt`.

### `grep -R "CUH{" .`
Debe devolver la coincidencia dentro de `./evidencia/oculto/flag.txt`.

### `cat ./evidencia/oculto/flag.txt`
Debe mostrar exactamente:

```text
CUH{linux_tambien_se_investiga}
```

## Checklist de aprobación del reto
- El script `crear_zip.ps1` termina sin error.
- El ZIP generado se llama `reto_archivos_linux.zip`.
- La carpeta raíz interna del ZIP es `reto_linux`.
- La flag final coincide exactamente con la documentada.
- La descripción de CTFd no revela la ruta exacta del archivo con la flag.
