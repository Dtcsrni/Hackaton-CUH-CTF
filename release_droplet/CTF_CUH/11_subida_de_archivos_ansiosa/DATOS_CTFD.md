# Datos para CTFd: Subida de archivos ansiosa

        ## Name
        Subida de archivos ansiosa

        ## Category
        Web

        ## Value
        440

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        El backend acepta prácticamente cualquier archivo y decide el destino solo por la extensión visible. Debes endurecer tamaño, tipo permitido, nombre generado y directorio final.

        Material de apoyo relacionado: [Guía interna: Subida de archivos ansiosa](/subida-de-archivos-ansiosa).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{subida_de_archivos_endurecida}`

        ## Hints
        - [20] El problema no es solo la extensión; revisa qué hace el código con el nombre y el destino.
- [35] Una validación razonable necesita lista permitida, tamaño máximo y nombre controlado por el servidor.
- [50] El validador espera validación de MIME/extensión, nombre aleatorio y almacenamiento fuera de la ruta pública por defecto.
