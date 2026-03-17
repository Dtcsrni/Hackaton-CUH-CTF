# Datos para CTFd: HSTS pendiente

        ## Name
        HSTS pendiente

        ## Category
        Web

        ## Value
        540

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        El sitio ya responde por HTTPS, pero todavía no comunica al navegador una política estricta de transporte. Eso deja margen para que clientes nuevos vuelvan a tocar HTTP antes de quedar fijados al canal seguro. Debes completar la configuración del virtual host para anunciar HSTS de forma clara y mantenible.

        Material de apoyo relacionado: [Guía interna: HSTS pendiente](/hsts-pendiente).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{hsts_define_la_politica_de_transporte}`

        ## Hints
        - [20] Aquí no falta el certificado; falta la política que le dice al navegador que no vuelva a bajar a HTTP.
- [35] La respuesta fuerte no es un comentario ni un redirect adicional, sino una cabecera `Strict-Transport-Security` bien construida.
- [50] El validador espera `max-age`, `includeSubDomains` y el modificador `always` dentro del bloque HTTPS.
