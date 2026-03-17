# Datos para CTFd: Derivación lenta

        ## Name
        Derivación lenta

        ## Category
        Criptografía

        ## Value
        500

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        La derivación de credenciales del sistema batch sigue usando un hash rápido y una sal fija. Debes reemplazarla por una KDF más adecuada con sal aleatoria e iteraciones explícitas.

        Material de apoyo relacionado: [Guía interna: Derivación lenta](/derivacion-lenta).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{kdf_endurecida_con_pbkdf2}`

        ## Hints
        - [20] Busca la función que genera la derivación, no la que compara resultados.
- [35] Si la sal sigue siendo constante, el problema central permanece.
- [50] La solución esperada usa PBKDF2-HMAC-SHA256, sal aleatoria e iteraciones altas y legibles.
