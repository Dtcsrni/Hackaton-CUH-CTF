# Datos para CTFd: Semilla predecible

        ## Name
        Semilla predecible

        ## Category
        Criptografía

        ## Value
        640

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        El módulo de generación de llaves internas sigue usando un PRNG generalista inicializado con una semilla derivada del tiempo. Debes reemplazar ese patrón por una fuente de entropía adecuada y mantener una salida simple para el sistema.

        Material de apoyo relacionado: [Guía interna: Semilla predecible](/semilla-predecible).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{entropia_fuerte_para_llaves}`

        ## Hints
        - [20] Busca cómo se inicializa el generador antes de producir la llave.
- [35] Si la misma ventana de tiempo puede repetir la salida, la fuente de entropía no es aceptable.
- [50] La solución esperada usa el módulo `secrets` y elimina la semilla derivada de la hora.
