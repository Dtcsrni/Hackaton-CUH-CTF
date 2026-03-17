# Paquete base CTF_CUH para organizador

## Visión general del paquete
Este repositorio entrega un paquete base listo para montar dos retos introductorios e intermedios de un hackathon CTF académico del Centro Universitario Hidalguense (CUH). Todo el contenido está diseñado para un laboratorio controlado, aislado y autorizado.

## Propósito pedagógico
- Introducir reconocimiento básico de red sin requerir explotación.
- Reforzar habilidades iniciales de navegación y búsqueda en Linux.
- Reducir improvisación del organizador con materiales operativos completos.

## Descripción de los dos retos
### 1. Puertas abiertas
Reto de reconocimiento donde el alumno enumera puertos en una IP de laboratorio, detecta el puerto `31337/tcp` y valida con `nc` un banner que devuelve la flag.

### 2. Comandos Linux - búsqueda básica
Reto basado en un archivo ZIP con estructura de directorios y archivos señuelo. El alumno lo descomprime en Kali Linux y encuentra la flag con herramientas básicas.

## Cómo está organizada la carpeta raíz
- `01_escaneo_de_puertos_puertas_abiertas/`: servicio TCP, datos de CTFd, validación y notas de red.
- `02_comandos_linux_busqueda_basica/`: estructura del reto Linux, script para generar el ZIP y validaciones.
- `CTFD_COPY_PASTE.md`: resumen rápido para cargar ambos retos en CTFd.
- `manifest.csv`: inventario mínimo de retos y artefactos.
- `CHECKLIST_*.md`: apoyo operativo antes, durante y después del evento.

## Qué archivos debe subir el organizador a CTFd
- Para `Puertas abiertas`: crear el reto en CTFd usando los textos de `01_escaneo_de_puertos_puertas_abiertas/DATOS_CTFD.md`. No hay archivo para subir; el reto depende de que el servicio TCP esté activo.
- Para `Comandos Linux - búsqueda básica`: generar y subir `02_comandos_linux_busqueda_basica/reto_archivos_linux.zip` junto con los textos de `02_comandos_linux_busqueda_basica/DATOS_CTFD.md`.

## Qué archivos no debe compartir con participantes
Para esta edición, los archivos operativos del organizador deben mantenerse fuera del alcance de los participantes:
- `README_ORGANIZADOR.md`
- `verificacion_local.md`
- `manifest.csv`
- `CHECKLIST_PRE_EVENTO.md`
- `CHECKLIST_DURANTE_EVENTO.md`
- `CHECKLIST_POST_EVENTO.md`

Si en futuras ediciones se agregan credenciales temporales, IPs privadas adicionales o notas de monitoreo, esos materiales también deben permanecer solo del lado del organizador.

## Cómo probar ambos retos antes del evento
1. Inicie `01_escaneo_de_puertos_puertas_abiertas/server_31337.py` en Windows.
2. Verifique escucha local en TCP `31337`.
3. Ejecute `02_comandos_linux_busqueda_basica/crear_zip.ps1`.
4. Revise que el ZIP contenga la carpeta raíz `reto_linux`.
5. Haga una prueba piloto desde Kali Linux o con una cuenta de alumno en CTFd.

## Cómo modificar IPs o paths si el laboratorio cambia
- La IP documentada de referencia es `192.168.56.25`.
- Si la topología cambia, reemplace esa IP en los archivos `DATOS_CTFD.md`, `verificacion_local.md` y en cualquier material operativo que la mencione.
- Si el proyecto se mueve a otra ruta local, el script `crear_zip.ps1` seguirá funcionando porque calcula rutas relativas a su propia ubicación.

## Recomendaciones para ejecutar una prueba piloto
- Use una VM Kali configurada igual que la del evento.
- Verifique conectividad con la IP real del host antes de iniciar el reto.
- Suba el ZIP a una instancia de prueba de CTFd y descargue el archivo como alumno.
- Confirme que ambas flags son aceptadas por CTFd sin ajustes manuales.
