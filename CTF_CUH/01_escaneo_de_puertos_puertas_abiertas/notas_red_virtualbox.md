# Notas de red en VirtualBox para el reto Puertas abiertas

## Modos de red útiles
### NAT
La VM sale a Internet usando la red del host, pero normalmente no puede recibir conexiones directas desde el host sin reglas adicionales de redirección. No es la mejor opción para este reto si el alumno debe alcanzar un servicio publicado en Windows.

### Adaptador puente
La VM aparece como otro equipo en la red física. Es útil si el laboratorio permite que host y VM compartan la misma LAN y no existen restricciones institucionales.

### Host-only
Crea una red privada entre host y VM. Suele ser la opción más conveniente para un laboratorio local porque aísla el entorno y facilita que Kali alcance servicios publicados en Windows. Para este paquete se recomienda `Host-only` como primera opción.

### Red interna
Permite comunicación entre máquinas virtuales conectadas a la misma red interna, pero no incluye al host por defecto. Solo conviene si el servicio también va a ejecutarse dentro de otra VM y no en Windows.

## Recomendación para laboratorio local
Para este reto conviene usar `Host-only` cuando el servicio `server_31337.py` corre en Windows y Kali Linux vive en VirtualBox. Esa configuración reduce exposición a la red externa y simplifica la conectividad.

## Cómo adaptar la IP del reto
La IP `192.168.56.25` es una referencia documentada, no una verdad universal. Si VirtualBox asigna otra IP al adaptador `Host-only` del host:

1. Detecte la IP real del host con `ipconfig`.
2. Reemplace `192.168.56.25` en la documentación del reto y en los textos preparados para CTFd.
3. Verifique desde Kali con `ping` o `nmap -Pn` a la nueva IP.

## Aclaración importante
Toda la red descrita en este proyecto corresponde a un laboratorio académico controlado, aislado y autorizado. No debe reutilizarse la documentación para pruebas fuera de ese contexto.
