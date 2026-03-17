# CTFd Copy/Paste

## Reto 1
### Name
Puertas abiertas

### Category
Reconocimiento

### Value
300

### Type
standard

### State
visible

### Description
En este entorno autorizado del hackathon CUH se ha publicado un servicio de laboratorio en la IP `192.168.56.25`. Tu objetivo es observar, enumerar e interpretar lo que realmente está expuesto antes de sacar conclusiones. Usa herramientas de reconocimiento desde Kali Linux y valida manualmente cualquier hallazgo relevante dentro de este laboratorio académico controlado.

### Flag
`CUH{escanear_antes_de_interpretar}`

### Hints
1. Antes de interpretar un servicio, enumera qué puertos están abiertos.
2. Un servicio útil no siempre está en un puerto estándar.
3. Después de identificar el puerto, una conexión manual puede aclarar el hallazgo.

### Archivo o servicio asociado
Servicio TCP `31337` en la IP de laboratorio documentada.

### Notas operativas
- Mantener `server_31337.py` ejecutándose durante toda la ventana del reto.
- Validar conectividad desde Kali antes de abrir el evento.
- Si cambia la IP del host, actualizar la descripción antes de publicar el reto.

## Reto 2
### Name
Comandos Linux - búsqueda básica

### Category
Linux

### Value
150

### Type
standard

### State
visible

### Description
Se ha preparado un archivo comprimido con evidencias de laboratorio para este entorno autorizado del hackathon CUH. Descárgalo, descomprímelo en Kali Linux y revisa su estructura con herramientas básicas del sistema. La respuesta no requiere software especializado; basta con observar rutas, listar archivos y validar contenido dentro de este laboratorio académico controlado.

### Flag
`CUH{linux_tambien_se_investiga}`

### Hints
1. Empieza descomprimiendo el archivo y revisando toda la estructura.
2. `find`, `grep` y `cat` son suficientes para este reto.
3. No todos los archivos visibles contienen la respuesta final.

### Archivo o servicio asociado
Archivo descargable `reto_archivos_linux.zip`.

### Notas operativas
- Generar el ZIP con `crear_zip.ps1` antes de subirlo a CTFd.
- Verificar que el ZIP conserva la carpeta raíz `reto_linux`.
- Probar la descarga del archivo con una cuenta de alumno.
