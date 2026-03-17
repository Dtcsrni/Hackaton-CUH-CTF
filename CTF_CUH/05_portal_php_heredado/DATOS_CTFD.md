# Datos para CTFd: Portal PHP heredado

        ## Name
        Portal PHP heredado

        ## Category
        Web

        ## Value
        400

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        El portal mezcla una consulta concatenada con una verificación de contraseñas ya obsoleta. Debes dejar el acceso en un formato más sano: consulta preparada y verificación de hash adecuada.

        Material de apoyo relacionado: [Guía interna: Portal PHP heredado](/portal-php-heredado).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{portal_php_heredado_endurecido}`

        ## Hints
        - [20] Hay dos problemas: uno en la consulta y otro en la comparación de contraseñas.
- [35] Si todavía dependes de md5, la corrección sigue incompleta.
- [50] La solución esperada usa prepare para consultar y password_verify para validar el hash.
