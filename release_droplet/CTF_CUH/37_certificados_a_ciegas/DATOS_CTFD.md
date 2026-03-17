# Datos para CTFd: Certificados a ciegas

        ## Name
        Certificados a ciegas

        ## Category
        Criptografía

        ## Value
        660

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        El cliente interno de sincronización TLS sigue aceptando certificados sin verificar la cadena ni el nombre del host. Debes endurecer el contexto SSL para que confíe solo en la CA correcta y exija validación completa.

        Material de apoyo relacionado: [Guía interna: Certificados a ciegas](/certificados-a-ciegas).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{tls_validado_con_ca_y_hostname}`

        ## Hints
        - [20] El problema está en el contexto SSL, no en la petición HTTP.
- [35] Si el cliente sigue usando un contexto no verificado o `CERT_NONE`, la corrección es insuficiente.
- [50] La solución esperada crea un contexto verificado con la CA entregada y hostname checking activo.
