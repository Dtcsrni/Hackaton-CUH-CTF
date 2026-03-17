# Datos para CTFd: Cabeceras que revelan de más

        ## Name
        Cabeceras que revelan de más

        ## Category
        Web

        ## Value
        420

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        La configuración web entrega información innecesaria, deja una política CSP demasiado abierta y no controla caché para contenido sensible. Debes endurecer el bloque de cabeceras.

        Material de apoyo relacionado: [Guía interna: Cabeceras que revelan de más](/cabeceras-que-revelan-de-mas).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{cabeceras_endurecidas}`

        ## Hints
        - [20] Revisa más de una cabecera: el problema no es aislado.
- [35] Una CSP útil no puede quedarse en wildcard si quieres proteger la aplicación.
- [50] La validación espera eliminación de información expuesta y políticas explícitas para CSP, caché y framing.
