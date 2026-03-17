# Datos para CTFd: Credenciales expuestas en tránsito

        ## Name
        Credenciales expuestas en tránsito

        ## Category
        Forense

        ## Value
        600

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        Un extracto de captura, un log del proxy y una nota del SOC muestran un inicio de sesión enviado por HTTP antes de que el equipo cerrara el canal seguro. Debes reconstruir qué portal estuvo implicado, qué ruta recibió las credenciales y cuál fue el impacto principal de haber dejado ese flujo sin HTTPS.

        Material de apoyo relacionado: [Guía interna: Credenciales expuestas en tránsito](/credenciales-expuestas-en-transito).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{credenciales_expuestas_por_http_reconstruidas}`

        ## Hints
        - [20] No busques un payload extraño. Aquí la pista fuerte es que la autenticación viajó por un canal que no debería usarse ya.
- [35] Cruza host, método y ruta entre la traza y el proxy hasta detectar el login que todavía salía por HTTP.
- [50] La respuesta final pide portal, ruta e impacto. El impacto se describe como exposición de credenciales en texto plano durante el tránsito.
