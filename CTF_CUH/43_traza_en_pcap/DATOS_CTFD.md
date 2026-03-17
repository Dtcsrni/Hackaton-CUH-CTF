# Datos para CTFd: Traza en PCAP

        ## Name
        Traza en PCAP

        ## Category
        Forense

        ## Value
        560

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        Un recorte de tráfico de laboratorio y una nota del SOC esconden una pista operativa entre consultas y respuestas aparentemente rutinarias. Debes identificar el host que importa, el recurso solicitado y la herramienta de Kali más útil para reconstruirlo rápido.

        Material de apoyo relacionado: [Guía interna: Traza en PCAP](/traza-en-pcap).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{tshark_reconstruye_la_pista}`

        ## Hints
        - [20] No revises el tráfico como texto plano primero. Este reto recompensa filtrar por host y recurso.
- [35] La pista no está en todas las peticiones, sino en una descarga concreta que rompe el patrón del resto.
- [50] La respuesta final pide herramienta, host y recurso. Piensa en el flujo de análisis típico de un PCAP en Kali.
