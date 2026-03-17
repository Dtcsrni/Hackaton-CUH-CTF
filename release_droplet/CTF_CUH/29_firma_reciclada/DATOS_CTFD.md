# Datos para CTFd: Firma reciclada

        ## Name
        Firma reciclada

        ## Category
        Criptografía

        ## Value
        420

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        Un servicio de firma dejó trazas suficientes para ver que dos firmas distintas comparten el mismo componente crítico. Debes identificar la causa, la clave afectada y la mitigación inmediata.

        Material de apoyo relacionado: [Guía interna: Firma reciclada](/firma-reciclada).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{firma_con_nonce_repetido_detectada}`

        ## Hints
        - [20] Mira si algún valor aparentemente aleatorio se repite donde no debería.
- [35] El problema no es que la firma falle, sino que se repite un componente demasiado sensible.
- [50] La salida final debe nombrar causa, clave afectada y mitigación, no un exploit.
