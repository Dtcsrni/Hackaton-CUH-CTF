# Datos para CTFd: Sesión que confía demasiado

        ## Name
        Sesión que confía demasiado

        ## Category
        Auth

        ## Value
        400

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        La aplicación acepta el rol efectivo de la sesión a partir de datos entregados por el cliente. Debes mover la decisión sensible al backend y dejar la sesión en un formato más defensivo.

        Material de apoyo relacionado: [Guía interna: Sesión que confía demasiado](/sesion-que-confia-demasiado).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{rol_de_sesion_validado_en_backend}`

        ## Hints
        - [20] Busca dónde se forma la sesión y de dónde sale el rol.
- [35] Si el backend sigue creyendo cualquier valor enviado por el cliente, el problema sigue ahí.
- [50] La validación espera una lista cerrada de roles y una asignación basada en datos internos.
