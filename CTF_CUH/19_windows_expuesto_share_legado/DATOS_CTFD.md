# Datos para CTFd: Windows expuesto: share legado

        ## Name
        Windows expuesto: share legado

        ## Category
        Windows

        ## Value
        540

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        Se entregan exportes de permisos, política local y una nota de operación de un share heredado. Debes identificar la exposición principal y proponer la corrección mínima con mayor impacto.

        Material de apoyo relacionado: [Guía interna: Windows expuesto share legado](/windows-expuesto-share-legado).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{share_legado_reducido}`

        ## Hints
        - [20] Mira primero qué grupo conserva permisos amplios sobre el share.
- [35] El problema no es solo compartir la carpeta, sino quién puede modificarla y desde dónde.
- [50] La respuesta debe nombrar grupo expuesto, permiso dominante y acción correctiva principal.
