from __future__ import annotations


def _clean(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


DESCRIPTIONS = {
    "Calentamiento - Bienvenida": _clean(
        """
        Este primer reto sirve para reconocer el terreno antes de entrar a los laboratorios más densos. La flag no está escondida detrás de una herramienta exótica ni de una técnica rara: está donde normalmente mucha gente no mira porque da por hecho que "solo es una bienvenida".

        Lee con calma, revisa el contenido completo y confirma qué partes de la interfaz sí forman parte del ejercicio. La idea es que entiendas desde el inicio que en este hackatón la observación también puntúa.
        """
    ),
    "Leer también es hacking": _clean(
        """
        A veces el dato útil no está en un panel secreto sino en un texto introductorio, una nota pequeña o una instrucción que casi todos se saltan. Este reto está diseñado para romper esa costumbre y obligarte a prestar atención al contexto.

        No necesitas fuerza bruta ni scripts. Solo hace falta revisar bien la información disponible, distinguir lo decorativo de lo operativo y localizar la referencia que realmente importa.
        """
    ),
    "Robots curiosos": _clean(
        """
        En muchos sitios, los archivos pensados para motores de búsqueda, rastreadores o automatizaciones terminan revelando rutas, hábitos de publicación o secciones que deberían haber pasado desapercibidas. Aquí debes mirar justo en esa dirección.

        El reto consiste en revisar cómo se comporta el sitio frente a visitantes automáticos, identificar qué se está exponiendo sin querer y seguir esa pista hasta encontrar la flag.
        """
    ),
    "Base64 no es cifrado": _clean(
        """
        Este reto gira alrededor de una confusión muy común: tratar un formato de codificación como si fuera un mecanismo de protección real. El material incluido parece ocultar un dato, pero en realidad solo está representado de otra manera.

        Cadena Base64: `Q1VIe2Jhc2U2NF9lc19zb2xvX2NvZGlmaWNhY2lvbn0=`

        La clave está en reconocer la transformación correcta, revertirla con criterio y confirmar que el resultado tiene sentido antes de darlo por bueno.
        """
    ),
    "César escolar": _clean(
        """
        Un mensaje corto ha sido desplazado usando un método clásico y deliberadamente sencillo. El objetivo no es presumir una herramienta automática, sino reconocer el patrón, probar desplazamientos razonables y validar qué salida encaja con el contexto del laboratorio.

        Texto cifrado: `FXK{fhvdu_hv_lqlflr}`

        Si el resultado final parece ruido, todavía no tienes la transformación correcta. Busca una salida legible y coherente con el formato habitual de flag del evento.
        """
    ),
    "Puertas abiertas": _clean(
        """
        Todo servicio que responde ya cuenta una historia: qué protocolo habla, qué versión parece usar y qué superficie de exposición está dejando visible. En este reto debes interpretar ese inventario sin quedarte solo en la lista de puertos.

        La flag aparece cuando conectas la información del escaneo con la pista correcta del servicio relevante. No hace falta forzar nada; lo importante es leer bien lo que la exposición ya revela.
        """
    ),
    "Metadatos indiscretos": _clean(
        """
        Una imagen puede enseñar mucho más de lo que muestra a simple vista. Este reto se centra en la información que suele viajar pegada al archivo: autoría, herramientas, exportaciones previas o restos de edición que terminan revelando pistas útiles.

        Trabaja sobre el archivo con herramientas de inspección de metadatos y no te conformes con la primera propiedad llamativa. La señal buena suele estar en el detalle menos vistoso.
        """
    ),
    "Comandos Linux - búsqueda básica": _clean(
        """
        Aquí el trabajo es metódico: recorrer archivos, filtrar contenido y localizar una pieza concreta de información sin perder tiempo revisando todo a mano. El ejercicio está pensado para que practiques búsquedas simples pero bien dirigidas.

        Usa utilidades básicas de Linux, entiende qué estás buscando y reduce el ruido. La flag está accesible para quien ordena bien el recorrido y no improvisa comandos sin objetivo.
        """
    ),
    "Logo en observación": _clean(
        """
        El logo del evento no es solo identidad visual: también funciona como artefacto para practicar observación digital. En este reto debes revisar el archivo como evidencia, no como decoración.

        Busca capas de información en torno a la imagen, su origen o sus propiedades internas. La solución no depende de edición avanzada, sino de mirar el recurso con mentalidad forense.
        """
    ),
    "Portada con pista": _clean(
        """
        La portada del sitio puede contener más que diseño y texto institucional. En este reto debes examinar ese bloque como si fuera una escena con varios niveles de información: lo visible, lo estructural y lo que se queda fuera del primer vistazo.

        El objetivo es localizar una pista útil sin romper nada y sin asumir que todo está en el HTML principal. Si revisas con cuidado, la propia portada te orienta.
        """
    ),
    "Cabeceras del laboratorio": _clean(
        """
        Antes de tocar un formulario o una cookie conviene mirar qué dice realmente el servidor cuando responde. Las cabeceras HTTP dan contexto sobre caché, tecnologías, pistas de despliegue y decisiones que impactan seguridad.

        Este reto te pide interpretar esa conversación de red, separar lo rutinario de lo relevante y detectar la cabecera o combinación de cabeceras que conduce a la flag.
        """
    ),
    "JSON de prueba": _clean(
        """
        No todo endpoint útil está diseñado para personas. A veces una ruta de prueba o un recurso pensado para desarrollo expone datos que ayudan a entender cómo está construido el sitio. Este reto se apoya en esa idea.

        Revisa la respuesta con calma, presta atención a claves, valores y convenciones internas y decide qué campo sí merece ser seguido. La solución está en interpretar el JSON, no en coleccionarlo entero.
        """
    ),
    "Bitácora del proxy": _clean(
        """
        Un registro de tráfico puede contar mejor la historia que la aplicación misma. En esta bitácora hay suficiente contexto para reconstruir qué recurso llamó la atención y por qué.

        Tu trabajo es leer el log como evidencia: identificar patrones, peticiones distintas al resto y detalles que destaquen por ruta, estado o cabeceras. La flag aparece cuando eliges la anomalía correcta.
        """
    ),
    "Hash filtrado": _clean(
        """
        Alguien dejó expuesto un hash, pero eso por sí solo no basta: primero hay que reconocer de qué tipo es y decidir una estrategia razonable. Este reto busca que practiques análisis previo antes de intentar cualquier recuperación.

        Fíjate en longitud, formato y contexto. Una buena identificación reduce muchísimo el espacio de búsqueda y te acerca a la cadena original, que es donde termina apareciendo la flag.
        """
    ),
    "ZIP bajo llave": _clean(
        """
        Un contenedor comprimido parece protegido, pero la clave no tiene por qué ser fuerte si el contexto del laboratorio ya apunta a cómo fue elegida. Aquí debes combinar observación y cracking controlado.

        El archivo adjunto tiene todo lo necesario para avanzar si eliges bien las pistas y validas tus intentos con método. La flag está dentro del contenido desbloqueado, no en el nombre del fichero.
        """
    ),
    "Acceso heredado": _clean(
        """
        Las credenciales heredadas suelen sobrevivir más tiempo del que deberían: aparecen en documentos viejos, copias de trabajo o notas internas que nadie depuró. Este reto explora justamente ese problema.

        Debes reconstruir qué patrón siguió el equipo anterior, identificar qué dato merece probarse dentro del material entregado y usarlo para llegar al recurso que guarda la flag.
        """
    ),
    "Registro sin servidor": _clean(
        """
        Un formulario que aparenta validar correctamente puede seguir confiando demasiado en lo que ocurre del lado del navegador. Este ejercicio está pensado para que detectes esa falsa sensación de control.

        Revisa cómo se envían y procesan los datos, qué validaciones viven solo en cliente y qué consecuencias tiene eso. La flag aparece cuando entiendes qué parte del flujo nunca debió darse por segura.
        """
    ),
    "Encuesta confiada": _clean(
        """
        Esta encuesta acepta más de lo que debería porque mezcla lógica de interfaz con confianza implícita en el cliente. El reto consiste en observar ese desajuste y demostrar que el flujo real es más laxo de lo que parece.

        No se trata de romper la aplicación, sino de entender qué datos viajan, cuáles deberían verificarse otra vez y qué decisión insegura deja rastro suficiente para encontrar la flag.
        """
    ),
    "Invitado privilegiado": _clean(
        """
        Un rol o privilegio no debería depender de un dato que el propio cliente pueda presentar como si fuera verdad. Este reto te coloca frente a un flujo donde esa frontera está mal definida.

        Observa tokens, respuestas y decisiones de autorización. La solución llega cuando identificas qué campo está dando más poder del que merece y sigues esa pista hasta la evidencia final.
        """
    ),
    "Secreto compartido debil": _clean(
        """
        Cuando una firma o un token dependen de un secreto pobre, repetido o demasiado predecible, toda la confianza del sistema se vuelve frágil. Este reto gira alrededor de ese riesgo.

        Examina el material entregado, entiende cómo se está utilizando el secreto y qué señales delatan que no fue elegido con suficiente cuidado. La flag está ligada a ese punto débil, no a una cadena aleatoria.
        """
    ),
    "Fuente principal": _clean(
        """
        El código fuente de una página puede revelar pistas que jamás fueron pensadas para la vista principal: comentarios, rutas internas, identificadores, nombres de archivos o referencias a recursos olvidados.

        Aquí debes leer el documento con mentalidad de auditoría ligera. La flag no está necesariamente visible en pantalla, pero sí en los elementos que sostienen esa interfaz.
        """
    ),
    "Consola curiosa": _clean(
        """
        La consola del navegador es una fuente excelente de contexto cuando una aplicación expone mensajes de depuración, pistas de desarrollo o estructuras internas que nunca debieron llegar a producción.

        Abre la herramienta correcta, revisa lo que realmente se registra y distingue entre ruido y señal. La solución sale de lo que el propio frontend decidió contar de más.
        """
    ),
    "Cookie de rol": _clean(
        """
        Una cookie no debería convertirse en fuente de verdad para algo tan sensible como el rol de un usuario. Este reto muestra qué pasa cuando la aplicación hace exactamente eso.

        Observa qué valores persisten entre peticiones, cómo se reflejan en la interfaz y dónde aparece la decisión insegura. La flag llega cuando identificas la confianza indebida y sus efectos.
        """
    ),
    "Cookie firmada debil": _clean(
        """
        Firmar una cookie solo ayuda si la validación es correcta y la clave realmente resiste. En este reto verás un esquema que aparenta solidez, pero deja suficientes huellas para cuestionarlo.

        Analiza formato, metadatos y consistencia entre valores. La resolución exige entender cómo debería protegerse una cookie y qué falla concreta la vuelve una mala base para decisiones importantes.
        """
    ),
    "Acceso por defecto": _clean(
        """
        Muchas exposiciones empiezan por algo aburrido: credenciales por defecto que nadie cambió. Este reto trabaja esa realidad desde un laboratorio controlado y con un contexto acotado.

        Toma las pistas del material de apoyo, entiende qué servicio o panel está siendo insinuado y usa esa información para verificar si la configuración inicial sigue vigente. La flag está del otro lado de esa omisión.
        """
    ),
    "Formulario de acceso": _clean(
        """
        Un login dice mucho más que "usuario" y "contraseña". El modo en que valida, los mensajes que devuelve y las diferencias entre respuestas pueden revelar por dónde empezar a estudiar el flujo.

        En este reto debes observar el formulario como superficie de análisis: qué espera, cómo reacciona y qué pista operativa deja disponible para encontrar la flag.
        """
    ),
    "Consulta concatenada": _clean(
        """
        Un desarrollador dejó un login de PHP armado con prisas y la consulta principal terminó construyéndose a partir de fragmentos pegados directamente. El ejercicio no busca que ataques un servicio en vivo, sino que leas el código como auditor y detectes por qué ese patrón es inseguro.

        Dentro del bundle encontrarás la aplicación rota, un validador y el contexto suficiente para reconstruir la intención original. La meta es corregir el punto vulnerable, mantener el flujo funcional y hacer que la validación local devuelva la flag cuando el parche ya no dependa de concatenación insegura.
        """
    ),
    "Reportes sin parámetros": _clean(
        """
        El módulo de reportes filtra resultados de una base de datos, pero lo hace mezclando entrada de usuario con la consulta final. El reto parte de una situación muy típica: una pantalla que "funciona" hasta que alguien revisa cómo se arma realmente el backend.

        Tu trabajo consiste en estudiar el código, entender qué filtros quiso implementar el equipo y rehacer la consulta con parámetros y controles coherentes. No basta con apagar el error: la solución debe seguir devolviendo resultados válidos y pasar el conjunto de pruebas incluido.
        """
    ),
    "Portal PHP heredado": _clean(
        """
        Este portal mezcla autenticación, sesiones y acceso a base de datos en una sola capa heredada, con varias decisiones inseguras acumuladas con el tiempo. El bundle reproduce ese escenario para que lo abordes como una tarea real de saneamiento y no como un ejemplo aislado.

        Tendrás que localizar dónde se acoplan mal las responsabilidades, qué parte del flujo genera la exposición principal y cómo corregirla sin romper el comportamiento esperado. La flag aparece cuando el portal queda funcional, consistente y validado por los tests del reto.
        """
    ),
    "Incidente en formularios": _clean(
        """
        Aquí no se te entrega una app para tocar, sino el rastro de un incidente: logs de aplicación, trazas de base de datos y artefactos suficientes para reconstruir qué pasó con un formulario sensible. La dificultad está en leer la secuencia completa sin inventar pasos que no están soportados por la evidencia.

        El objetivo es identificar la ruta afectada, entender qué decisión insegura abrió el problema y extraer de los registros la información exacta que lleva a la flag. Si ordenas bien la cronología, el caso se explica solo.
        """
    ),
    "Sesión que confía demasiado": _clean(
        """
        Una aplicación interna acepta señales del cliente como si fueran confirmaciones del servidor, y eso contamina la gestión de sesión con datos que nunca debieron gobernar permisos. El reto está montado para que revises esa frontera de confianza con precisión.

        Analiza cómo se construye el estado del usuario, qué atributos pueden ser manipulables y dónde debería imponerse la validación del lado correcto. La flag llega cuando el backend deja de creer en información que el cliente no debería controlar.
        """
    ),
    "Cookie de rol heredada": _clean(
        """
        El sistema arrastra una implementación antigua de cookies que mezcla identidad, rol y firma de manera poco robusta. En vez de rehacer la aplicación desde cero, aquí debes evaluar qué parte del diseño es realmente peligrosa y endurecerla.

        El material te guía hacia validación, expiración, separación de responsabilidades y comprobación del lado servidor. La solución correcta conserva el flujo útil para el usuario, pero elimina la posibilidad de que la cookie defina más de lo que debería.
        """
    ),
    "JWT sin audiencia": _clean(
        """
        Un token puede estar bien firmado y aun así ser aceptado de forma incorrecta si quien lo consume omite validaciones críticas. En este laboratorio el validador admite JWT con demasiada confianza porque deja huecos en campos esenciales.

        Revisa cómo se verifican algoritmo, emisor, audiencia y tiempos de vida. La meta no es solo "hacer que pase un check", sino dejar un validador que rechace lo que no corresponde y devuelva la flag cuando las pruebas de seguridad y funcionamiento pasen completas.
        """
    ),
    "Restablecimiento abierto": _clean(
        """
        El flujo de reseteo de contraseña parece cómodo para soporte, pero esa comodidad se consiguió debilitando la lógica del token y del proceso de confirmación. Este reto reproduce el problema para que lo sanees con criterio.

        Debes revisar generación, expiración, alcance y uso del token, además de qué datos se aceptan durante el cambio de contraseña. La flag se obtiene cuando el circuito queda endurecido y la validación demuestra que ya no se puede reutilizar ni aceptar fuera de contexto.
        """
    ),
    "Subida de archivos ansiosa": _clean(
        """
        Un cargador de archivos no debería decidir confianza solo por extensión o por el nombre que trae el cliente. En este reto se entrega un módulo que quiere aceptar rápido y filtra tarde, lo que abre una superficie de riesgo innecesaria.

        Examina cómo se validan tipo, tamaño, nombre y destino de almacenamiento. Tu parche debe hacer más que bloquear un caso obvio: tiene que establecer reglas claras de aceptación y dejar el flujo suficientemente sólido como para que el validador entregue la flag.
        """
    ),
    "Traversal en miniatura": _clean(
        """
        Un servicio aparentemente pequeño para descargar o previsualizar archivos puede exponer mucho más de lo que pretende si resuelve rutas de manera ingenua. El escenario de este reto concentra esa idea en una implementación mínima pero realista.

        Revisa cómo se unen directorios, cómo se normalizan rutas y qué base de referencia se toma para servir contenido. La solución correcta cierra el acceso impropio sin romper el uso legítimo del visor y queda confirmada cuando el validador devuelve la flag.
        """
    ),
    "Portal defaceado en PHP": _clean(
        """
        El sitio ya aparece comprometido: la parte visible cambió y ahora toca reconstruir cómo quedó alterado, qué archivos fueron tocados y cuál sería una restauración segura. Es un reto de análisis y reparación, no de intrusión.

        Trabaja con la evidencia incluida, compara versiones, separa personalización legítima de modificación maliciosa y deja una copia restaurada que pase la verificación. La flag sale cuando puedes demostrar que entendiste el alcance del defacement y revertiste solo lo necesario.
        """
    ),
    "Cabeceras que revelan de más": _clean(
        """
        No todas las exposiciones vienen de una consulta o de un formulario; a veces el propio servidor entrega demasiado contexto sobre su configuración, su caché o su política de carga. Este reto se centra en esas señales.

        Debes endurecer el conjunto de cabeceras y la configuración asociada para reducir superficie y comportamiento ambiguo. El objetivo es dejar una respuesta más sobria, más segura y suficientemente bien definida como para superar las pruebas del laboratorio.
        """
    ),
    "Prompt de soporte indiscreto": _clean(
        """
        Un asistente interno de soporte fue montado sin delimitar bien qué contexto puede usar, qué instrucciones debe ignorar y qué información nunca debería revelar. En lugar de explotar el sistema, aquí toca rediseñarlo defensivamente.

        Revisa prompt base, políticas de salida, aislamiento de contexto y criterios de rechazo. La flag aparece cuando la batería de pruebas demuestra que el asistente sigue siendo útil, pero ya no entrega información fuera de alcance ni obedece instrucciones impropias.
        """
    ),
    "Recuperación de contexto": _clean(
        """
        Este reto parte de una fuga ya ocurrida: se entregan trazas de conversación, eventos y decisiones del sistema para que reconstruyas cómo un asistente terminó exponiendo contexto interno. La dificultad está en identificar la causa raíz y no quedarse solo con el síntoma.

        Analiza el encadenamiento de mensajes, qué memoria se arrastró más de la cuenta y qué defensa faltó en el punto crítico. La solución combina lectura forense con propuesta de mitigación validada por el conjunto de pruebas.
        """
    ),
    "Linux expuesto: sudoers heredado": _clean(
        """
        El laboratorio simula un servidor Linux al que se le fueron acumulando permisos cómodos para operación diaria hasta dejar reglas de sudo demasiado amplias. El reto consiste en auditar esa configuración y corregirla sin dejar inservible el sistema.

        Estudia los archivos entregados, identifica qué permisos son excesivos, qué comandos deberían restringirse y cómo endurecer la política con el menor privilegio posible. Cuando la revisión queda bien hecha, el validador entrega la flag.
        """
    ),
    "Linux expuesto: servicio olvidado": _clean(
        """
        Un servicio residual, una unidad que nadie recuerda y varios indicios en el sistema bastan para abrir superficie de exposición innecesaria. Este reto reproduce ese escenario desde la perspectiva de inventario y hardening.

        Tendrás que revisar puertos, unidades, rutas de ejecución y configuraciones heredadas para decidir qué debe mantenerse, qué debe aislarse y qué ya no debería existir. La flag sale cuando tu propuesta deja el sistema limpio y consistente con las pruebas del reto.
        """
    ),
    "Windows expuesto: share legado": _clean(
        """
        El entorno Windows de este reto incluye un recurso compartido con permisos y supuestos heredados de otra época. No hay que "entrar" al sistema: hay que leer la configuración exportada, entender los riesgos y reconstruir una versión más segura.

        Revisa ACL, grupos, exposición del share y dependencia con procesos de trabajo. La solución correcta demuestra que sabes separar uso legítimo de acceso innecesario y por eso termina devolviendo la flag.
        """
    ),
    "Windows expuesto: tareas persistentes": _clean(
        """
        Las tareas programadas pueden ser una ayuda administrativa o una vía silenciosa para mantener cambios no deseados en un sistema. En este caso se te entregan artefactos suficientes para reconstruir qué tareas estaban activas y por qué representan un problema.

        Analiza cronología, ejecutables asociados, rutas, usuarios y eventos del sistema. Después corrige la persistencia sin romper lo que sí era parte de la operación normal. La validación final confirma ese equilibrio y revela la flag.
        """
    ),
    "Binario de despacho": _clean(
        """
        Un binario pequeño puede esconder lógica suficiente para obligarte a leer ensamblador con atención. Este reto está pensado para practicar reversing orientado a comprensión: qué valida el programa, cómo transforma la entrada y qué condición exacta espera.

        Usa desensamblado o trazado, reconstruye la lógica paso a paso y evita modificar el binario. La flag aparece cuando entiendes de verdad el flujo y produces la respuesta coherente con esa verificación.
        """
    ),
    "Licencia bajo revisión": _clean(
        """
        Este es un reto de reversing más completo: la comprobación de licencia no vive en un único punto, sino distribuida entre varias rutinas y transformaciones que exigen una lectura más paciente. La dificultad está en unir esas piezas sin perder el hilo.

        El material adjunto da lo necesario para analizar el ejecutable, identificar dónde se deriva la condición final y reconstruir el dato correcto sin parchear el sistema ni saltarte la lógica. La flag solo aparece cuando esa reconstrucción es precisa.
        """
    ),
    "Perfil disperso": _clean(
        """
        La identidad digital de una persona o equipo rara vez vive en un solo sitio. Este reto de OSINT te pide reunir señales repartidas entre perfiles, publicaciones y referencias indirectas para reconstruir una pista útil sin asumir demasiado pronto que ya viste lo importante.

        Observa nombres repetidos, alias, formatos y pequeños detalles que conectan una fuente con otra. La flag está detrás de esa correlación, no en una búsqueda aislada.
        """
    ),
    "Agenda filtrada": _clean(
        """
        Un documento de agenda o planificación puede revelar más de lo que aparenta: horarios, asistentes, rutas, nombres internos y hábitos de trabajo. El reto consiste en sacar valor de esos fragmentos sin perderte en datos secundarios.

        Cruza fechas, contexto y referencias internas hasta aislar el elemento que realmente cambia la lectura del caso. La flag aparece cuando interpretas la agenda como fuente de inteligencia y no como simple calendario.
        """
    ),
    "Foto del laboratorio": _clean(
        """
        Una sola fotografía puede contener dispositivos, pantallas, etiquetas, reflejos y relaciones espaciales útiles para una investigación. Este reto está diseñado para que combines observación visual con atención al contexto del entorno.

        Acércate a la imagen por capas: primero la escena general, luego detalles textuales y finalmente elementos que conecten con otras piezas del laboratorio. La flag surge de esa lectura completa.
        """
    ),
    "Proveedor fantasma": _clean(
        """
        Hay proveedores que solo dejan un rastro tenue: un dominio olvidado, una firma en un documento, un patrón de contacto o una referencia cruzada en un material secundario. Este reto te pide seguir ese rastro con paciencia.

        El objetivo es distinguir qué dato realmente apunta a una entidad concreta y cuál solo añade ruido. Cuando logras reconstruir la identidad correcta del proveedor, la flag queda al alcance.
        """
    ),
    "Huella de publicación": _clean(
        """
        Publicar deja huellas: nombres de archivo, tiempos, versiones, plataformas y residuos de edición que ayudan a reconstruir de dónde salió un contenido. Este reto explota esa idea desde un enfoque de correlación.

        No basta con mirar una sola evidencia. Debes comparar pistas entre varias fuentes, identificar coincidencias útiles y llegar a la atribución correcta que termina revelando la flag.
        """
    ),
    "XOR de respaldo": _clean(
        """
        Un equipo intentó "proteger" un respaldo con una operación simple y acabó generando un esquema reversible con el contexto adecuado. Este reto te pide reconocer esa construcción, separar patrón y ruido y recuperar el contenido válido.

        El material adjunto incluye suficiente estructura para inferir cómo se aplicó la operación y en qué parte conviene empezar a tirar del hilo. La flag está en el resultado descifrado, no en el archivo intermedio.
        """
    ),
    "Firma reciclada": _clean(
        """
        Cuando un proceso reutiliza material criptográfico fuera de contexto, la seguridad deja de depender solo del algoritmo y pasa a depender de una mala práctica operativa. Este reto se apoya en ese tipo de error.

        Analiza cómo se está produciendo o verificando la firma, qué se repite donde no debería y qué conclusión puede extraerse de esa repetición. La flag aparece cuando entiendes la debilidad del esquema y la aprovechas dentro del laboratorio controlado.
        """
    ),
    "RSA sin OAEP": _clean(
        """
        RSA puede parecer suficiente por sí solo, pero el modo de uso importa tanto como la clave. En este reto la implementación prescinde de un relleno adecuado y deja señales que permiten razonar sobre el problema.

        Revisa los parámetros, el formato del material entregado y el comportamiento esperado. La solución exige comprensión del esquema, no una prueba ciega de herramientas: debes reconocer por qué el uso es débil y qué dato se puede recuperar a partir de ello.
        """
    ),
    "Derivación lenta": _clean(
        """
        No todas las debilidades criptográficas están en el cifrado; a veces el problema aparece antes, en cómo se deriva una clave desde una contraseña o una semilla. Este reto examina justo esa fase.

        Analiza parámetros de derivación, costos, sal y material complementario. La flag se obtiene cuando consigues reproducir correctamente el proceso y verificas que el resultado coincide con el escenario del laboratorio.
        """
    ),
    "Bloques repetidos": _clean(
        """
        Ver el mismo patrón varias veces en un cifrado por bloques suele ser una pista valiosa, especialmente cuando el modo elegido filtra más estructura de la debida. Aquí el reto es reconocer esa repetición y leer qué te está diciendo sobre el proceso.

        Inspecciona tamaño, repeticiones y relación entre fragmentos equivalentes. La solución no sale de una sola intuición, sino de conectar la regularidad del material con el modo de operación que mejor explica esas huellas.
        """
    ),
    "CBC sin integridad": _clean(
        """
        Cifrar no basta si el mensaje puede ser alterado y el sistema no tiene forma de detectar esa manipulación. Este reto parte de un paquete protegido con bloques, pero sin una verificación de integridad que cierre realmente el circuito.

        Revisa las evidencias, distingue confidencialidad de autenticación y decide qué propiedad falta en el esquema actual. La flag aparece cuando identificas con precisión el modo, el riesgo operativo y la mitigación correcta.
        """
    ),
    "IV reciclado en reportes": _clean(
        """
        Dos reportes cifrados del mismo lote comparten más estructura de la que deberían, y eso apunta a un error de operación criptográfica más que a una rotura del algoritmo. La tarea consiste en reconocer ese síntoma a partir de artefactos pequeños pero suficientes.

        Compara primeros bloques, revisa el contexto del proceso y explica por qué esa coincidencia no es casual. La solución se valida cuando nombras el problema exacto, el hallazgo observable y la corrección prioritaria.
        """
    ),
    "HMAC truncado en gateway": _clean(
        """
        El gateway sí usa HMAC, pero lo desperdicia al verificar solo una fracción de la firma y hacerlo con una comparación insegura. Este reto se centra en esa clase de error que no rompe el algoritmo, pero sí el control de integridad que se esperaba de él.

        Debes endurecer la validación sin cambiar el formato del mensaje ni la lógica general del servicio. La flag aparece cuando la firma completa se compara de forma segura y el chequeo deja de aceptar atajos peligrosos.
        """
    ),
    "Semilla predecible": _clean(
        """
        Una llave no es fuerte solo por su tamaño: también importa de dónde sale. En este laboratorio, el módulo de generación sigue dependiendo de un generador generalista inicializado con una semilla demasiado predecible para material criptográfico.

        Tu trabajo es sustituir esa base por una fuente de entropía adecuada, conservar un formato de salida útil para el sistema y dejar el módulo listo para que el validador confirme la mejora.
        """
    ),
    "Certificados a ciegas": _clean(
        """
        TLS pierde gran parte de su valor cuando el cliente decide confiar en cualquier certificado sin validar cadena ni nombre del host. Este reto reproduce esa mala práctica en un cliente interno que "funciona", pero solo porque dejó de verificar lo importante.

        Revisa el contexto SSL, la política de confianza y el material de CA entregado. La flag se obtiene cuando el cliente deja de aceptar conexiones a ciegas y aplica una validación completa de autenticidad.
        """
    ),
    "Cronología cruzada": _clean(
        """
        Varias publicaciones, una agenda y comentarios secundarios dejan suficiente rastro para reconstruir una secuencia de hechos, pero solo si ordenas bien el tiempo y no tratas cada fuente como una isla. Este reto exige correlación cronológica real, no una lectura superficial.

        La solución aparece cuando identificas el evento pivote, la cuenta que realmente lo operó y el artefacto correcto asociado a ese momento. Si la línea temporal tiene huecos, todavía falta trabajo.
        """
    ),
    "Repositorio fantasma": _clean(
        """
        Un repositorio retirado del perfil principal todavía deja señales en issues exportados, capturas viejas y notas de versión. El reto no se resuelve con una sola coincidencia: hay que reconstruir la atribución completa con nombre, organización y tag.

        Prioriza la evidencia que conserve rutas o referencias exactas y usa el resto como confirmación. La flag aparece cuando la identidad del repositorio queda cerrada sin ambigüedad.
        """
    ),
    "Credencial en ponencia": _clean(
        """
        Un gafete apenas visible, una lista parcial de asistentes y una nota de backstage bastan para identificar a una persona concreta, pero solo si descartas falsos positivos con cuidado. Este reto está diseñado para premiar correlación fina entre fragmentos.

        La respuesta correcta une nombre, alias y track a partir de varias piezas complementarias. Si uno de esos datos depende de una sola fuente débil, aún no está realmente validado.
        """
    ),
    "Red de proveedores": _clean(
        """
        Varios proveedores aparecen dispersos entre licitaciones, firmas y documentos públicos, pero uno de ellos funciona como pivote de la red. El reto consiste en identificar esa empresa central, el dominio que la conecta con otras evidencias y el documento que consolida la relación.

        No basta con enumerar nombres. La solución exige mapear relaciones y distinguir qué fuente une realmente el conjunto.
        """
    ),
    "Trazas de convocatoria": _clean(
        """
        Una convocatoria republicada varias veces puede dejar más información en sus propiedades, versiones y renombres que en el texto visible del PDF final. Este reto trabaja precisamente esa trazabilidad documental.

        Debes atribuir la versión maestra, identificar al editor responsable y recuperar la clave interna del lote. La flag aparece cuando esas tres piezas se sostienen entre sí y ya no dependen de conjeturas.
        """
    ),
    "Traza en PCAP": _clean(
        """
        Una captura pequeña puede contener decenas de peticiones anodinas y una sola que cambie por completo la lectura del caso. Este reto está pensado para quien ya usa Kali como entorno de trabajo y sabe que el filtrado correcto vale más que abrir tráfico a ciegas.

        Debes identificar la herramienta adecuada, el host que realmente importa y el recurso clave pedido en la traza. La solución sale de priorizar bien el tráfico, no de leer todo como si fuera un log plano.
        """
    ),
    "Firmware en capas": _clean(
        """
        Un firmware no siempre se analiza desde su capa principal. A veces la pieza valiosa está en un artefacto embebido, olvidado entre filesystem, textos residuales y configuraciones heredadas. Este reto se apoya en ese tipo de triage.

        La meta es reconocer qué herramienta conviene usar, qué artefacto merece atención y qué hallazgo operativo lo vuelve importante. Si te quedas en la superficie del firmware, se te escapa la parte útil.
        """
    ),
    "Metadatos en cascada": _clean(
        """
        Varias imágenes del laboratorio fueron exportadas una y otra vez, pero no todo se limpió entre versiones. Este reto exige leer esa cadena de metadatos como una fuente de atribución técnica y no solo como propiedades sueltas del archivo.

        Debes correlacionar autoría, comentarios y huellas de ubicación hasta cerrar una historia coherente. La flag aparece cuando identificas la herramienta adecuada y unes correctamente persona y lugar.
        """
    ),
    "Carving de evidencias": _clean(
        """
        Cuando una evidencia mezcla archivos de distintos tipos, la clave no está en abrirlo todo, sino en recuperar primero y elegir después qué pieza realmente importa. Este reto trabaja ese enfoque de carving y selección que muchas veces acelera un análisis real.

        La solución exige decir qué herramienta usarías, qué archivo recuperado pesa más y qué detalle operacional lo vuelve relevante para el caso. Si solo enumeras artefactos, todavía falta el criterio de priorización.
        """
    ),
    "Diccionario de laboratorio": _clean(
        """
        En cracking controlado no siempre gana la wordlist más grande. A veces el contexto del entorno, la convención de nombres y el tipo de cuenta reducen tanto el espacio de búsqueda que la estrategia importa más que la fuerza bruta ciega.

        Este reto premia justamente eso: elegir bien herramienta, cuenta y diccionario temático a partir de la información disponible. La flag aparece cuando el punto de partida ya es técnicamente sólido antes de lanzar nada pesado.
        """
    ),
    "Portal sin redirección segura": _clean(
        """
        Un certificado emitido no resuelve nada si el portal todavía acepta peticiones útiles por HTTP y deja al usuario decidir, por costumbre o por enlace viejo, si entra al canal cifrado o no. Este reto se centra en esa deuda típica de borde: el sitio debería forzar HTTPS desde el primer contacto y todavía no lo hace.

        Debes revisar la configuración del proxy, convertir el acceso en una redirección inequívoca hacia HTTPS y dejar listo el listener seguro para servir la aplicación. La flag aparece cuando el tránsito inseguro deja de ser una opción válida para el portal.
        """
    ),
    "HSTS pendiente": _clean(
        """
        Muchos equipos creen que con un redirect basta, pero sin una política persistente el navegador sigue pudiendo tocar HTTP en visitas nuevas o en condiciones de primera carga. Este reto trabaja esa capa menos visible pero muy importante del transporte seguro: HSTS.

        La meta es completar el virtual host para que el navegador reciba una instrucción clara y duradera de usar solo HTTPS. La flag se obtiene cuando la configuración expresa esa política con parámetros razonables y deja de depender solo de redirecciones reactivas.
        """
    ),
    "Cookie de sesión sin Secure": _clean(
        """
        Migrar un portal a HTTPS y olvidar la configuración de la cookie de sesión deja una sensación falsa de cierre. Si la cookie no está marcada correctamente, el riesgo sigue vivo y la sesión continúa expuesta más de la cuenta en el lado equivocado del flujo.

        En este reto debes revisar la configuración del framework y llevar la sesión a un estado más defensivo, no solo activando `Secure`, sino completando atributos mínimos coherentes con una aplicación web real. La flag aparece cuando la sesión deja de comportarse como si el portal todavía viviera en HTTP.
        """
    ),
    "Contenido mixto heredado": _clean(
        """
        Una migración parcial a HTTPS suele delatarse por pequeños restos: una imagen, un script o una llamada API que siguen apuntando a HTTP aunque la página principal ya entre por TLS. Este reto te pone delante de ese escenario para que limpies la deuda sin depender de que el navegador "lo arregle".

        Debes revisar plantilla y frontend, localizar todas las referencias heredadas y dejar el conjunto alineado con HTTPS. La flag aparece cuando el portal ya no mezcla transporte seguro con recursos pedidos en texto plano.
        """
    ),
    "Credenciales expuestas en tránsito": _clean(
        """
        La evidencia de este reto no habla de una intrusión compleja, sino de un error de despliegue muy concreto: un login que siguió aceptando credenciales por HTTP en plena migración del portal. El problema es sencillo de describir y grave en sus consecuencias, justo por eso conviene reconstruirlo bien.

        Debes correlacionar la traza, el log del proxy y la nota del SOC para identificar portal, ruta sensible e impacto real observado. La flag aparece cuando la reconstrucción deja claro que las credenciales viajaron en texto plano y por qué eso nunca debió ocurrir.
        """
    ),
    "Rompe el sistema": _clean(
        """
        Misión oculta reservada para hallazgos reales sobre la plataforma del hackatón. Este reto no forma parte del tablero general y solo se acredita cuando el equipo organizador confirma que el reporte mejoró el laboratorio o evitó un fallo relevante.

        La resolución no depende de un adjunto ni de una ruta pública concreta. Se cierra por revisión académica, con trazabilidad del hallazgo y validación manual del equipo organizador.
        """
    ),
}


EXPECTED_CHALLENGE_COUNT = 77
