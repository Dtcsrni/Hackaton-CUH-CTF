# Datos para CTFd: CBC sin integridad

        ## Name
        CBC sin integridad

        ## Category
        Criptografía

        ## Value
        580

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        Recibes una captura de un mensaje cifrado en bloques, una nota del equipo de integración y una observación del área de monitoreo. Debes identificar el modo, explicar el riesgo principal y proponer la mitigación adecuada.

        Material de apoyo relacionado: [Guía interna: CBC sin integridad](/cbc-sin-integridad).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{cbc_sin_integridad_identificada}`

        ## Hints
        - [20] El problema no está en el IV aleatorio, sino en lo que falta alrededor del cifrado.
- [35] Si un atacante puede alterar el ciphertext y el sistema no detecta el cambio, falta una propiedad importante.
- [50] La respuesta final pide modo, riesgo y mitigación, no un descifrado del mensaje.
