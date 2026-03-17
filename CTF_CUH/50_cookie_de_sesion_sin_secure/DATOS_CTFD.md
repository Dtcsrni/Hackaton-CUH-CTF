# Datos para CTFd: Cookie de sesión sin Secure

        ## Name
        Cookie de sesión sin Secure

        ## Category
        Auth

        ## Value
        560

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        La plataforma ya se sirve por HTTPS, pero la configuración de sesión sigue permitiendo que la cookie viaje sin la marca correcta de transporte. Debes endurecer la configuración del framework para que la sesión solo se entregue por HTTPS y además mantenga atributos básicos de protección para navegación real.

        Material de apoyo relacionado: [Guía interna: Cookie de sesión sin Secure](/cookie-de-sesion-sin-secure).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{cookies_de_sesion_solo_por_https}`

        ## Hints
        - [20] Aquí no se parchea el HTML ni el reverse proxy. El problema vive en la configuración de sesión de la aplicación.
- [35] Si la cookie sigue saliendo sin `Secure`, el cambio todavía no protege el tránsito; aprovecha también para revisar `HttpOnly` y `SameSite`.
- [50] El validador espera `SESSION_COOKIE_SECURE = True`, `SESSION_COOKIE_HTTPONLY = True` y `SESSION_COOKIE_SAMESITE = "Lax"`.
