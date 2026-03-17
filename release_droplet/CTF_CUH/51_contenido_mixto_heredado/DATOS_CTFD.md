# Datos para CTFd: Contenido mixto heredado

        ## Name
        Contenido mixto heredado

        ## Category
        Web

        ## Value
        580

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        La portada principal ya entra por HTTPS, pero aún arrastra referencias duras a scripts, imágenes y llamadas API sobre HTTP plano. Debes limpiar ese contenido mixto para que el navegador no tenga que decidir entre bloquear recursos o degradar la confianza del sitio.

        Material de apoyo relacionado: [Guía interna: Contenido mixto heredado](/contenido-mixto-heredado).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{todos_los_recursos_van_por_https}`

        ## Hints
        - [20] Revisa tanto la plantilla HTML como el JavaScript cliente; el problema no vive solo en una etiqueta `<script>`.
- [35] Si queda una sola referencia `http://` al dominio del laboratorio, la corrección sigue incompleta.
- [50] El validador espera que `dashboard.html` y `app.js` usen URLs `https://` y que desaparezcan las referencias heredadas en texto plano.
