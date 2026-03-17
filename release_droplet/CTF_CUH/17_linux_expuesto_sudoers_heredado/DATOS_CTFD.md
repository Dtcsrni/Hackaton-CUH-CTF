# Datos para CTFd: Linux expuesto: sudoers heredado

        ## Name
        Linux expuesto: sudoers heredado

        ## Category
        Linux

        ## Value
        500

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        Se entrega una configuración de `sudoers` heredada que permite más de lo que debería a usuarios operativos. Debes reducir el alcance y dejar reglas mínimas y legibles.

        Material de apoyo relacionado: [Guía interna: Linux expuesto sudoers heredado](/linux-expuesto-sudoers-heredado).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{sudoers_heredado_corregido}`

        ## Hints
        - [20] Revisa qué usuarios y qué comandos tienen permisos amplios.
- [35] Un ALL demasiado abierto casi nunca es necesario en una cuenta operativa.
- [50] La validación espera reglas concretas, `NOPASSWD` restringido y ausencia de privilegios globales innecesarios.
