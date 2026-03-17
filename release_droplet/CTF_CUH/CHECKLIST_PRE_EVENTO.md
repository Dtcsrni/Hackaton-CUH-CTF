# Checklist pre-evento

- Confirmar el modo de red de VirtualBox y la IP real del host para el laboratorio.
- Verificar que la VM Kali inicia correctamente y tiene `nmap`, `nc`, `unzip`, `find`, `grep` y `cat` disponibles.
- Validar conectividad entre Kali y la IP del host documentada para el evento.
- Iniciar `server_31337.py` y comprobar que el puerto TCP `31337` está en escucha.
- Ejecutar `crear_zip.ps1` y confirmar que `reto_archivos_linux.zip` existe.
- Revisar el contenido interno del ZIP y confirmar la estructura `reto_linux/...`.
- Resolver ambos retos con una cuenta de alumno o una prueba controlada.
- Confirmar que las flags aceptadas por CTFd coinciden exactamente con las documentadas.
- Revisar que los hints publicados en CTFd corresponden al nivel esperado.
- Probar el envío de flags en CTFd antes de abrir el evento.
- Preparar un plan de respaldo: copia del ZIP, copia local de la documentación y un método alterno para reiniciar el servicio TCP.
