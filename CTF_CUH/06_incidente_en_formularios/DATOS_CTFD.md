# Datos para CTFd: Incidente en formularios

        ## Name
        Incidente en formularios

        ## Category
        Forense

        ## Value
        420

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        Se entrega un conjunto de logs del portal, un extracto de la traza SQL y una nota operativa interna. Debes reconstruir el incidente, identificar la cuenta afectada y describir el fallo de diseño que lo permitió.

        Material de apoyo relacionado: [Guía interna: Incidente en formularios](/incidente-en-formularios).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{incidente_de_formularios_reconstruido}`

        ## Hints
        - [20] Empieza por correlacionar hora, ruta y resultado en los logs de aplicación.
- [35] La traza SQL te dice más sobre el fallo que el mensaje visible del formulario.
- [50] No te piden un payload: te piden el vector lógico, la cuenta afectada y el impacto observado.
