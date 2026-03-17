# Datos para CTFd: Reportes sin parámetros

        ## Name
        Reportes sin parámetros

        ## Category
        Web

        ## Value
        380

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        El buscador de reportes de un portal interno sigue concatenando el término de búsqueda dentro de la cláusula WHERE. Debes revisar el backend, parametrizar el filtro y dejar el archivo listo para una consulta mantenible.

        Material de apoyo relacionado: [Guía interna: Reportes sin parámetros](/reportes-sin-parametros).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{reportes_filtrados_con_parametros}`

        ## Hints
        - [20] No hace falta tocar la interfaz. El problema está en cómo se forma el filtro del lado del servidor.
- [35] Un LIKE también puede parametrizarse; prepara primero la consulta y construye después el valor de búsqueda.
- [50] El validador espera placeholder, bind y ausencia de concatenación directa en el SQL.
