# Datos para CTFd: Linux expuesto: servicio olvidado

        ## Name
        Linux expuesto: servicio olvidado

        ## Category
        Linux

        ## Value
        520

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        Se entrega un inventario de servicio y un archivo `.service` demasiado permisivo. Debes dejarlo limitado, con usuario dedicado, binding local y sin capacidades innecesarias.

        Material de apoyo relacionado: [Guía interna: Linux expuesto servicio olvidado](/linux-expuesto-servicio-olvidado).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{servicio_olvidado_documentado_y_limitado}`

        ## Hints
        - [20] Revisa usuario de ejecución, interfaz de escucha y capacidades.
- [35] Si sigue ejecutando como root y escuchando en todas las interfaces, el problema principal continúa.
- [50] La solución esperada define usuario dedicado, binding local y restricciones básicas del servicio.
