# Datos para CTFd: RSA sin OAEP

        ## Name
        RSA sin OAEP

        ## Category
        Criptografía

        ## Value
        460

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        El módulo de descifrado del portal sigue usando un padding heredado que ya no debería quedarse en producción. Debes migrarlo a OAEP con parámetros explícitos y coherentes.

        Material de apoyo relacionado: [Guía interna: RSA sin OAEP](/rsa-sin-oaep).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{rsa_con_oaep_y_sha256}`

        ## Hints
        - [20] El archivo ya importa la librería correcta; el problema está en la política de padding.
- [35] La corrección no es solo cambiar un nombre: también importa la función hash usada en OAEP.
- [50] La validación espera OAEP con MGF1 y SHA-256 en ambos componentes.
