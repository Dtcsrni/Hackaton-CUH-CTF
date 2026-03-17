# Datos para CTFd: HMAC truncado en gateway

        ## Name
        HMAC truncado en gateway

        ## Category
        Criptografía

        ## Value
        620

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        El gateway firma mensajes con HMAC, pero el verificador compara solo una parte de la firma y lo hace de forma insegura. Debes endurecer la verificación sin romper el formato del servicio.

        Material de apoyo relacionado: [Guía interna: HMAC truncado en gateway](/hmac-truncado-en-gateway).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{gateway_hmac_verificado_completo}`

        ## Hints
        - [20] La clave no está rota; el problema está en cómo se compara la firma recibida.
- [35] Si el código acepta solo un prefijo de la firma, la validación sigue siendo débil.
- [50] La solución esperada usa comparación completa y constante sobre una firma hexadecimal de longitud fija.
