# Datos para CTFd: Restablecimiento abierto

        ## Name
        Restablecimiento abierto

        ## Category
        Auth

        ## Value
        470

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        El flujo de restablecimiento genera tokens previsibles y no revisa vigencia ni usuario vinculado con suficiente rigor. Debes cerrar ese diseño y dejar una validación mínima seria.

        Material de apoyo relacionado: [Guía interna: Restablecimiento abierto](/restablecimiento-abierto).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{token_de_reset_endurecido}`

        ## Hints
        - [20] Observa cómo se genera el token y qué datos usa.
- [35] Si el token no está ligado al usuario y al tiempo, sigue siendo demasiado débil.
- [50] La validación espera secreto, expiración y comprobación explícita del usuario al que pertenece el token.
