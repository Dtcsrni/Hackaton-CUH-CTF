# Flujo del reto Puertas abiertas

```mermaid
flowchart LR
    A["Alumno en Kali Linux"] --> B["nmap contra 192.168.56.25"]
    B --> C["Detecta 31337/tcp abierto"]
    C --> D["Conecta con nc al puerto 31337"]
    D --> E["Recibe banner del servicio"]
    E --> F["Obtiene la flag y la envía a CTFd"]
```

## Explicación breve del flujo
El alumno no recibe el puerto como dato inicial. Primero enumera la superficie visible del host de laboratorio, detecta un puerto no estándar y luego usa una conexión manual para verificar qué entrega el servicio. La flag aparece como parte del banner del laboratorio controlado.
