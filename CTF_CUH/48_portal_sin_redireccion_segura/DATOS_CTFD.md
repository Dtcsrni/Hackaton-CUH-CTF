# Datos para CTFd: Portal sin redirección segura

        ## Name
        Portal sin redirección segura

        ## Category
        Web

        ## Value
        520

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        El portal del laboratorio ya tiene certificado interno disponible, pero la configuración de borde sigue atendiendo el sitio principal en HTTP y no obliga a redirigir al canal cifrado. Debes corregir la configuración para que todo acceso al puerto 80 termine inmediatamente en HTTPS y el listener seguro quede preparado para servir la aplicación.

        Material de apoyo relacionado: [Guía interna: Portal sin redirección segura](/portal-sin-redireccion-segura).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{https_obligatorio_desde_el_borde}`

        ## Hints
        - [20] El problema no está en la app Python, sino en la configuración del reverse proxy.
- [35] La corrección debe cubrir dos cosas: redirección desde 80 y un bloque HTTPS explícito del lado seguro.
- [50] El validador espera `return 301 https://$host$request_uri;`, `listen 443 ssl;` y referencias al certificado configurado.
