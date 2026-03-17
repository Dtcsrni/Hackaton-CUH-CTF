# Datos para CTFd: Consulta concatenada

        ## Name
        Consulta concatenada

        ## Category
        Web

        ## Value
        360

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        Se entrega un login heredado en PHP que sigue armando la consulta SQL mediante concatenación directa de usuario y clave. El objetivo del reto es corregir el archivo para que la autenticación use parámetros en lugar de mezclar datos del cliente con la consulta.

        Material de apoyo relacionado: [Guía interna: Consulta concatenada](/consulta-concatenada).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{consulta_concatenada_corregida}`

        ## Hints
        - [20] Busca el archivo que realmente construye la consulta. El problema no está en el HTML.
- [35] Si todavía ves comillas mezcladas con variables dentro del SQL, la corrección sigue incompleta.
- [50] La validación espera una consulta preparada y una ejecución separada de los valores.
