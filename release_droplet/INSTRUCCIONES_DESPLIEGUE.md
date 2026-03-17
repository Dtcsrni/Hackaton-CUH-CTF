# Despliegue del Hackaton CTF CUH 2026 en tu propio Droplet

Este paquete contiene todo lo necesario para **replicar exactamente** el estado de la plataforma CTF del Hackaton CUH 2026 en tu propio servidor (por ejemplo, un Droplet de DigitalOcean) o en tu máquina local.

## Contenido de esta carpeta

1. **`Hackatón CTF CUH 2026.2026-03-17_08_53_16.zip`**: Es el **Backup completo** de la plataforma. Contiene la base de datos, todos los retos, configuraciones visuales (colores, logos) y las banderas.
2. **`CTF_CUH/`**: Contiene el código fuente e instrucciones organizativas de los retos, incluyendo los servicios externos que no corren dentro de CTFd (por ejemplo, el script del reto de puertos abiertos).

---

## 🚀 Paso 1: Instalar CTFd (La plataforma web)

Para levantar la plataforma, usarás la versión oficial y limpia de CTFd, y luego inyectarás el backup.

1. Conéctate a tu Droplet o abre una terminal en tu entorno Linux con Docker instalado.
2. Clona el repositorio oficial de CTFd:
   ```bash
   git clone https://github.com/CTFd/CTFd.git
   cd CTFd
   ```
3. Levanta la plataforma en segundo plano:
   ```bash
   docker-compose up -d
   ```
   *(Esto descargará las imágenes y levantará el servidor web en el puerto `8000`)*.

---

## 📦 Paso 2: Importar el Backup Exacto

Una vez que CTFd esté corriendo:
1. Abre tu navegador y ve a `http://<IP_DE_TU_DROPLET>:8000`.
2. Verás la pantalla inicial de configuración de CTFd ("Setup CTFd"). No te preocupes por llenarla perfectamente, simplemente crea un usuario **Admin** temporal y dale un nombre cualquiera al evento.
3. Una vez dentro de la plataforma, ve al menú superior derecho y entra al **Admin Panel**.
4. En el panel izquierdo, navega a **Config** > **Backup** (o ve a `http://<IP_DE_TU_DROPLET>:8000/admin/config/backup`).
5. En la sección **Import**, selecciona el archivo `Hackatón CTF CUH 2026*.zip` que viene en esta carpeta.
6. Haz clic en importar. CTFd se reiniciará para cargar los datos.

¡Listo! Al recargar la página, tendrás **la misma apariencia visual, los mismos retos, banderas y puntajes** exactamente como estaban en el Hackaton.

---

## 🔧 Paso 3: Levantar los servicios externos de los retos

Algunos retos requieren que corran pequeños servicios o servidores externos al CTFd. Todo eso está en la carpeta `CTF_CUH`.

Por ejemplo, para el reto de **Puertas Abiertas**:
1. Copia la carpeta `CTF_CUH` a tu Droplet.
2. Entra a `cd CTF_CUH/01_escaneo_de_puertos_puertas_abiertas`.
3. Ejecuta el servidor vulnerable en segundo plano (requiere Python 3):
   ```bash
   nohup python3 server_31337.py &
   ```
   *(Esto dejará el puerto 31337 abierto y listo para que intentes hackearlo)*.

Para otros retos, consulta el `README_GENERAL_ORGANIZADOR.md` dentro de `CTF_CUH/`.
