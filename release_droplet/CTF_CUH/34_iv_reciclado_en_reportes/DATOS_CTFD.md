# Datos para CTFd: IV reciclado en reportes

        ## Name
        IV reciclado en reportes

        ## Category
        Criptografía

        ## Value
        600

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        Dos reportes cifrados del mismo lote comparten demasiada estructura y una nota del equipo revela cómo se están generando sus parámetros. Debes identificar el problema, describir el hallazgo observable y proponer una mitigación operativa correcta.

        Material de apoyo relacionado: [Guía interna: IV reciclado en reportes](/iv-reciclado-en-reportes).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{iv_reciclado_detectado_en_reportes}`

        ## Hints
        - [20] Compara los primeros bloques antes de mirar el resto del material.
- [35] Si dos mensajes con el mismo prefijo producen el mismo primer bloque, revisa cómo se está manejando el IV.
- [50] La respuesta final pide problema, hallazgo y mitigación, no solo el nombre del algoritmo.
