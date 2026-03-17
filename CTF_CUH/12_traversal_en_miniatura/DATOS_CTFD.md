# Datos para CTFd: Traversal en miniatura

        ## Name
        Traversal en miniatura

        ## Category
        Web

        ## Value
        470

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        El pequeño servidor de archivos resuelve rutas a partir del parámetro pedido sin comprobar si el destino sigue dentro del directorio autorizado. Debes normalizar y forzar el alcance.

        Material de apoyo relacionado: [Guía interna: Traversal en miniatura](/traversal-en-miniatura).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{rutas_normalizadas_y_resueltas}`

        ## Hints
        - [20] Observa cómo se compone el path final a partir del nombre recibido.
- [35] Un join no basta si luego no compruebas dónde termina apuntando el path resuelto.
- [50] La solución esperada usa resolve y verifica que el destino permanezca dentro de la raíz permitida.
