# Datos para CTFd: JWT sin audiencia

        ## Name
        JWT sin audiencia

        ## Category
        Auth

        ## Value
        450

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        El validador de tokens del portal solo revisa firma y expiación. Debes endurecerlo para que también controle algoritmo permitido, issuer y audience esperados.

        Material de apoyo relacionado: [Guía interna: JWT sin audiencia](/jwt-sin-audiencia).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{jwt_con_validacion_completa}`

        ## Hints
        - [20] Lee el archivo completo antes de cambiar nada; faltan varias validaciones, no una sola.
- [35] Si no defines issuer y audience esperados, el token sigue siendo ambiguo.
- [50] La corrección esperada restringe algoritmo, issuer, audience y expiración.
