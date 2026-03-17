# Datos para CTFd: Cookie de rol heredada

        ## Name
        Cookie de rol heredada

        ## Category
        Auth

        ## Value
        430

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        Una cookie de rol heredada sigue aceptando contenido sin verificación robusta. Debes endurecer la validación y limitar el rol efectivo a un conjunto de valores permitidos.

        Material de apoyo relacionado: [Guía interna: Cookie de rol heredada](/cookie-de-rol-heredada).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{cookie_de_rol_endurecida}`

        ## Hints
        - [20] La cookie entra al backend ya deserializada; el problema es qué hace luego el código con ella.
- [35] Si cualquier valor llega a convertirse en rol efectivo, la corrección sigue incompleta.
- [50] El validador espera firma HMAC, comparación segura y lista cerrada de roles.
