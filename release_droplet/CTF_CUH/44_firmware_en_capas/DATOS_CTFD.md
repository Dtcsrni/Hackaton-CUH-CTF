# Datos para CTFd: Firmware en capas

        ## Name
        Firmware en capas

        ## Category
        Forense

        ## Value
        600

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        Un firmware sintético del laboratorio deja restos de una configuración anterior y una nota de extracción parcial. Debes identificar la herramienta de Kali que conviene usar, el artefacto embebido relevante y el hallazgo operativo que justifica revisarlo.

        Material de apoyo relacionado: [Guía interna: Firmware en capas](/firmware-en-capas).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{binwalk_descubre_el_resto_olvidado}`

        ## Hints
        - [20] Este reto no se resuelve leyendo el archivo como texto normal. Piensa en análisis por capas.
- [35] La salida útil no es el firmware en sí, sino un artefacto interno detectado en la extracción.
- [50] Necesitas herramienta, artefacto y hallazgo. La pista fuerte del bundle apunta a cómo se descubren componentes embebidos.
