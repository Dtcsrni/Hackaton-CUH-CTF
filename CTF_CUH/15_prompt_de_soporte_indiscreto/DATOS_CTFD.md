# Datos para CTFd: Prompt de soporte indiscreto

        ## Name
        Prompt de soporte indiscreto

        ## Category
        IA defensiva

        ## Value
        500

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        El asistente interno de soporte mezcla instrucciones del sistema, contexto sensible y mensajes del usuario sin defensas suficientes. Debes rediseñar el prompt y la capa de filtrado para que pase una batería defensiva.

        Material de apoyo relacionado: [Guía interna: Prompt de soporte indiscreto](/prompt-de-soporte-indiscreto).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{prompt_de_soporte_endurecido}`

        ## Hints
        - [20] No basta con decir 'ignora el prompt del usuario'; la mitigación debe ser estructural.
- [35] Separa claramente instrucciones del sistema, contexto permitido y datos que nunca deben salir.
- [50] La validación espera reglas explícitas de denegación, reducción de contexto y rechazo a peticiones fuera de alcance.
