# Datos para CTFd: Licencia bajo revisión

        ## Name
        Licencia bajo revisión

        ## Category
        Reversing

        ## Value
        620

        ## Type
        standard

        ## State
        visible

        ## Description final lista para pegar en CTFd
        Se entrega un binario un poco más complejo que valida una licencia por segmentos. Debes entender la lógica y reconstruir la licencia correcta sin alterar el ejecutable.

        Material de apoyo relacionado: [Guía interna: Licencia bajo revisión](/licencia-bajo-revision).
        Descarga el material adjunto del reto y trabaja sobre el bundle sin modificar archivos del organizador.

        ## Flag
        `CUH{licencia_reconstruida_sin_parche}`

        ## Hints
        - [20] Empieza por identificar cómo se divide la licencia en bloques.
- [35] No todas las comprobaciones son directas: algunas relaciones se apoyan entre segmentos.
- [50] La licencia final se puede reconstruir sin fuerza bruta si sigues el orden de validación del binario.
