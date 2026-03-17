from __future__ import annotations


def hs(h1: str, h2: str, h3: str) -> list[dict]:
    return [
        {"cost": 20, "content": h1.strip()},
        {"cost": 35, "content": h2.strip()},
        {"cost": 50, "content": h3.strip()},
    ]


HINTS = {
    "Calentamiento - Bienvenida": hs(
        "No busques fuera del propio material inicial. Aquí la flag suele estar donde la mayoría solo pasa por encima.",
        "Lee hasta el final y revisa si hay texto pequeño, nota operativa o bloque que parezca meramente introductorio.",
        "Si ya abriste varias herramientas, vas tarde: el reto se resuelve prestando atención al contenido visible y completo de la bienvenida.",
    ),
    "Leer también es hacking": hs(
        "La pista útil está en el propio texto del evento, no en una sección externa.",
        "Revisa el contenido de arriba abajo y fíjate en frases que parezcan secundarias pero demasiado específicas para ser relleno.",
        "La solución aparece cuando dejas de leer la página como marketing y la lees como instrucciones de laboratorio.",
    ),
    "Robots curiosos": hs(
        "Empieza por los recursos que suelen consultar rastreadores y automatizaciones antes que un usuario normal.",
        "Si encuentras rutas, no te quedes en listarlas: revisa cuál de ellas parece más interesante para el contexto del hackatón.",
        "La flag no está en el archivo de control en sí, sino en una ruta o referencia revelada por ese archivo.",
    ),
    "Base64 no es cifrado": hs(
        "Primero identifica si estás ante una codificación reversible o ante un cifrado real.",
        "Si el alfabeto usa letras, números, `+`, `/` o `=`, probablemente no necesitas atacar nada; necesitas decodificar correctamente.",
        "La salida válida debe ser legible y coherente con el formato del evento. Si obtienes ruido, todavía no aplicaste la transformación correcta.",
    ),
    "César escolar": hs(
        "Antes de automatizar, prueba si el texto encaja con un desplazamiento corto del alfabeto.",
        "Busca una salida con palabras legibles; este reto premia reconocer el patrón, no bruteforcear sin mirar.",
        "Si dudas entre varios desplazamientos, quédate con el que produce una cadena clara y compatible con una flag o con el contexto del laboratorio.",
    ),
    "Puertas abiertas": hs(
        "No todos los puertos importan igual. Empieza por el servicio que mejor encaje con la temática del laboratorio.",
        "Fíjate en banner, título, tecnología o pequeñas pistas que te indiquen cuál servicio expone algo más que conectividad.",
        "La flag suele estar ligada al servicio realmente útil; si solo enumeraste puertos pero no interpretaste el contexto, todavía falta el paso importante.",
    ),
    "Metadatos indiscretos": hs(
        "No revises solo el contenido visual de la imagen. Este reto está en la información que viaja con el archivo.",
        "Extrae metadatos de autoría, software, comentarios, fechas o rutas exportadas antes de asumir que no hay nada.",
        "La pista correcta suele estar en una propiedad concreta del archivo, no en la imagen a simple vista.",
    ),
    "Comandos Linux - búsqueda básica": hs(
        "No necesitas recorrer todo manualmente. Piensa en qué comando te deja filtrar por nombre o por contenido.",
        "Decide primero si la flag es un archivo concreto o una cadena escondida dentro de varios archivos.",
        "Si sigues navegando directorio por directorio, cambia de enfoque: este reto se resuelve con búsqueda dirigida, no con inspección artesanal.",
    ),
    "Logo en observación": hs(
        "Trata el logo como evidencia digital, no como decoración del sitio.",
        "Revisa propiedades del archivo, nombre real, dimensiones, metadatos y cualquier información residual asociada a la imagen.",
        "La solución no exige editar la imagen; exige observar cómo fue producida o qué información conserva internamente.",
    ),
    "Portada con pista": hs(
        "La pista está asociada a la portada, pero no necesariamente al texto principal que ves de entrada.",
        "Inspecciona la estructura del bloque, sus recursos vinculados y cualquier elemento que cargue o describa el contenido.",
        "Si solo leíste el hero, todavía te falta revisar qué información técnica o secundaria acompaña a esa portada.",
    ),
    "Cabeceras del laboratorio": hs(
        "El servidor ya está hablando contigo antes de que toques el cuerpo de la respuesta.",
        "Abre las cabeceras completas y busca una que revele más de lo necesario sobre configuración, despliegue o contexto.",
        "La flag no suele venir en el HTML cuando el reto se llama así; viene en la respuesta HTTP o en una pista directa dejada allí.",
    ),
    "JSON de prueba": hs(
        "Lee el recurso JSON como una fuente de contexto, no como un simple volcado de datos.",
        "Busca claves que parezcan temporales, internas, de depuración o vinculadas al laboratorio.",
        "La respuesta útil suele salir de un campo concreto o de una ruta mencionada dentro del JSON, no de copiar todo el objeto.",
    ),
    "Bitácora del proxy": hs(
        "Empieza por detectar qué petición se comporta distinto al resto.",
        "Cruza método, ruta, código de estado y hora para encontrar la entrada anómala o especialmente reveladora.",
        "No busques un payload; busca la evidencia que indique qué recurso, ruta o patrón merece seguirse para encontrar la flag.",
    ),
    "Hash filtrado": hs(
        "Identificar el tipo de hash acorta más el problema que lanzar herramientas a ciegas.",
        "Longitud, prefijos y formato suelen decirte si estás ante MD5, SHA-1, bcrypt u otra familia.",
        "Antes de intentar recuperar el valor, asegúrate de haber clasificado bien el hash. Ese paso es parte del reto.",
    ),
    "ZIP bajo llave": hs(
        "No ataques el archivo como si la contraseña fuera completamente aleatoria. El contexto del laboratorio importa.",
        "Revisa nombres, notas y material relacionado para inferir cómo pudo elegirse la clave antes de lanzar intentos ciegos.",
        "La flag no está en el contenedor bloqueado por sí mismo; está dentro del contenido que se abre cuando eliges la pista correcta.",
    ),
    "Acceso heredado": hs(
        "Lo heredado rara vez es fuerte. Busca patrones repetidos en nombres, documentos o notas internas.",
        "Piensa qué dato del material entregado parece antiguo, reutilizable o demasiado cómodo para un entorno real.",
        "La solución sale de reconstruir la lógica de la credencial, no de probar palabras aleatorias sin relación con el bundle.",
    ),
    "Registro sin servidor": hs(
        "Observa qué validaciones viven solo en la interfaz y cuáles realmente parecen sostenerse del otro lado.",
        "Si un valor puede ser manipulado antes de enviarse, pregúntate qué parte del flujo confía en él sin volver a validarlo.",
        "La flag aparece cuando identificas qué decisión se dejó al cliente y qué efecto produce eso en el resultado final.",
    ),
    "Encuesta confiada": hs(
        "No revises solo el formulario visible; revisa qué campos viajan y qué asume la aplicación sobre ellos.",
        "Fíjate en parámetros ocultos, valores prellenados o decisiones de confianza que solo se sostienen en frontend.",
        "La clave del reto es demostrar que el cliente puede influir más de la cuenta, no encontrar un texto llamativo en la página.",
    ),
    "Invitado privilegiado": hs(
        "Cuando un rol depende de algo que viaja desde el cliente, el problema suele aparecer en el punto donde se decide la autorización.",
        "Revisa token, cookie o parámetro relacionado con privilegios y pregunta si el servidor lo valida o solo lo refleja.",
        "La flag llega cuando identificas la fuente exacta de confianza indebida y el recurso que queda expuesto por ella.",
    ),
    "Secreto compartido debil": hs(
        "La pista útil no está en romper el token, sino en entender por qué el secreto que lo protege no inspira confianza.",
        "Busca señales de predictibilidad, reutilización o baja complejidad en el material entregado.",
        "Si ya sabes qué componente depende del secreto, la respuesta final sale de explicar esa debilidad con suficiente precisión.",
    ),
    "Fuente principal": hs(
        "Abre el código fuente completo de la página, no solo lo que el navegador renderiza visualmente.",
        "Comentarios, rutas internas, nombres de archivo o marcas de depuración suelen ser mejores pistas que el texto visible.",
        "La flag o la pista que conduce a ella aparece en la estructura del documento, no en el estilo superficial del sitio.",
    ),
    "Consola curiosa": hs(
        "Abre la consola antes de tocar nada más. Este reto depende de lo que el frontend decide contarte.",
        "No te quedes con el primer `log`; mira mensajes al cargar, avisos, objetos y cualquier salida con referencias internas.",
        "Si el reto se llama así, la señal importante está en la consola o en datos mostrados por scripts cliente, no en la interfaz normal.",
    ),
    "Cookie de rol": hs(
        "Inspecciona qué cookies existen y cuál de ellas parece influir en identidad o privilegios.",
        "Si una cookie contiene un rol legible o fácilmente interpretable, pregúntate quién debería decidir realmente ese valor.",
        "La flag aparece cuando entiendes que la cookie no es solo almacenamiento, sino una fuente de verdad indebida para permisos.",
    ),
    "Cookie firmada debil": hs(
        "Que una cookie esté firmada no significa automáticamente que esté bien protegida.",
        "Revisa formato, consistencia y material contextual para evaluar si la firma depende de un secreto sólido o de una práctica pobre.",
        "La pista valiosa está en la forma en que la aplicación confía en la firma, no en el nombre de la cookie por sí solo.",
    ),
    "Acceso por defecto": hs(
        "Antes de probar credenciales al azar, identifica qué producto, servicio o panel estás viendo.",
        "Busca en el material entregado una pista de fabricante, despliegue o configuración inicial típica.",
        "La solución suele salir de unir el contexto del servicio con su pareja de acceso conocida, no de una lista interminable de intentos.",
    ),
    "Formulario de acceso": hs(
        "Mira cómo responde el login cuando cambias entradas y qué diferencias devuelve.",
        "Los mensajes, la estructura del formulario y el material complementario revelan más sobre el flujo que el botón de envío en sí.",
        "No te piden romper el formulario a ciegas; te piden leerlo como superficie de análisis hasta encontrar la pista que lo acompaña.",
    ),
    "Consulta concatenada": hs(
        "La vulnerabilidad real está donde se construye el SQL, no donde se dibuja el formulario.",
        "Si al revisar el archivo todavía ves variables mezcladas directamente con la cadena de consulta, el problema sigue intacto.",
        "El validador espera una consulta preparada con placeholders y una ejecución separada de los valores. Si no llegaste a eso, aún no está bien.",
    ),
    "Reportes sin parámetros": hs(
        "Empieza por el archivo del backend que arma el filtro de búsqueda.",
        "Un `LIKE` también puede parametrizarse; el valor con comodines se construye fuera del SQL y luego se enlaza.",
        "La solución correcta elimina la concatenación directa y deja una consulta mantenible. Piensa en placeholder, bind y legibilidad.",
    ),
    "Portal PHP heredado": hs(
        "Hay más de un problema: no te quedes solo con la consulta.",
        "Si la verificación de credenciales todavía depende de `md5` o de una comparación simplista, el parche sigue corto.",
        "El reto queda bien resuelto cuando combinas consulta preparada con validación moderna del hash, no cuando solo apagas un síntoma.",
    ),
    "Incidente en formularios": hs(
        "Ordénalo primero por tiempo: logs de aplicación, luego traza SQL y después la nota operativa.",
        "Busca qué cuenta, ruta y resultado aparecen alineados en la misma ventana temporal del incidente.",
        "La respuesta final necesita reconstrucción: qué se tocó, a quién afectó y qué falla de diseño lo permitió. No basta con decir 'hubo un problema en el login'.",
    ),
    "Sesión que confía demasiado": hs(
        "Ubica el punto exacto donde el backend decide el rol o el estado efectivo de la sesión.",
        "Si ese dato nace en el cliente o llega sin verificación fuerte, ya encontraste la frontera de confianza rota.",
        "La corrección útil consiste en recalcular o verificar el privilegio del lado servidor. No maquilles el dato entrante; deja de confiar en él.",
    ),
    "Cookie de rol heredada": hs(
        "Revisa qué información guarda la cookie y qué parte de ella jamás debería decidir permisos por sí sola.",
        "Firmar no basta si el backend sigue usando la cookie como verdad directa para el rol.",
        "Piensa en separar identidad, sesión y privilegio. El parche correcto reduce la responsabilidad de la cookie en decisiones sensibles.",
    ),
    "JWT sin audiencia": hs(
        "No asumas que la firma es el único control importante del token.",
        "Revisa si se validan `aud`, `iss`, expiración y algoritmo permitido, además de la firma.",
        "El validador del reto espera una política completa: aceptar tokens bien formados pero rechazar los que no fueron emitidos para este servicio concreto.",
    ),
    "Restablecimiento abierto": hs(
        "Empieza por cómo se genera y se valida el token de reset, no por la pantalla final del cambio de contraseña.",
        "Si el token puede reutilizarse, no expira bien o no está atado al contexto correcto, el flujo sigue abierto.",
        "La solución valiosa endurece el ciclo entero: emisión, caducidad, un solo uso y verificación del destinatario o cuenta asociada.",
    ),
    "Subida de archivos ansiosa": hs(
        "No te quedes con la extensión. Revisa también tipo, nombre final y destino del archivo.",
        "Una validación de carga útil no es suficiente si guardas el archivo en una ruta peligrosa o conservas nombres controlados por el cliente.",
        "El reto queda bien cuando defines reglas claras de aceptación y almacenamiento, no cuando solo bloqueas un ejemplo llamativo.",
    ),
    "Traversal en miniatura": hs(
        "El problema está en cómo se resuelve la ruta, no en el contenido de los archivos.",
        "Si el código une base y entrada del usuario sin normalizar ni comprobar el resultado final, la exposición sigue abierta.",
        "La mitigación correcta valida la ruta resuelta contra un directorio base permitido. No basta con reemplazar `../` a mano.",
    ),
    "Portal defaceado en PHP": hs(
        "Compara primero qué cambió de verdad entre la versión alterada y la copia legítima.",
        "No todo cambio es malicioso; identifica qué fragmentos introducen comportamiento o contenido ajeno al sitio original.",
        "La respuesta útil reconstruye el alcance del defacement y restaura solo lo comprometido. Piensa como analista, no como quien borra todo por reflejo.",
    ),
    "Cabeceras que revelan de más": hs(
        "Empieza listando qué cabeceras ya expone el servicio y cuáles faltan para endurecer la respuesta.",
        "Busca información de tecnología, caché, framing o contenido activo que no debería quedar tan abierta.",
        "El parche correcto es una política coherente de cabeceras, no una colección aleatoria de valores copiados de Internet.",
    ),
    "Prompt de soporte indiscreto": hs(
        "Antes de pensar en filtros, decide qué contexto jamás debería llegar al modelo.",
        "Revisa prompt base, separación de instrucciones y controles de salida; el problema suele ser de diseño, no de una sola palabra prohibida.",
        "El reto se resuelve cuando el asistente sigue siendo útil pero deja de obedecer instrucciones fuera de alcance y deja de revelar contexto interno.",
    ),
    "Recuperación de contexto": hs(
        "Ordénalo como incidente: qué sabía el sistema, qué recibió y qué terminó filtrando.",
        "Busca el momento exacto en que una memoria, instrucción previa o contexto interno se arrastra más allá de lo debido.",
        "La solución fuerte no solo señala el síntoma; identifica la causa raíz y la medida concreta que corta esa fuga en el punto correcto.",
    ),
    "Linux expuesto: sudoers heredado": hs(
        "No todos los permisos de `sudoers` pesan igual. Empieza por los más amplios o con comodines.",
        "Pregunta qué comandos permiten escalado indirecto o ejecución demasiado abierta y qué usuario los hereda.",
        "El parche útil aplica mínimo privilegio real: no se trata de borrar todo, sino de dejar solo lo estrictamente necesario.",
    ),
    "Linux expuesto: servicio olvidado": hs(
        "Haz inventario antes de corregir: unidades, puertos, binarios y directorios asociados.",
        "Si un servicio ya no cumple función clara pero sigue escuchando o arrancando, probablemente ya tienes el foco del reto.",
        "La respuesta buena no es solo 'apagarlo'; es documentar qué expone, por qué sobra y cómo limitar o retirar esa superficie sin romper lo válido.",
    ),
    "Windows expuesto: share legado": hs(
        "Empieza por los permisos efectivos, no por el nombre simpático del recurso compartido.",
        "Cruza grupos, ACL y necesidad operativa real para ver qué acceso sobra y qué acceso sí debe conservarse.",
        "La solución fuerte reduce exposición sin dejar el share inusable. Piensa en mínimo privilegio, no en cierre total por reflejo.",
    ),
    "Windows expuesto: tareas persistentes": hs(
        "Ordena eventos, usuarios y binarios por tiempo antes de decidir qué tarea es sospechosa.",
        "Fíjate en ejecutables poco habituales, rutas de usuario, repetición temporal y descripciones engañosamente administrativas.",
        "La respuesta correcta distingue operación legítima de persistencia indebida y explica cómo corregirla sin romper lo que sí pertenece al sistema.",
    ),
    "Binario de despacho": hs(
        "Identifica primero dónde compara o transforma la entrada; no te pierdas recorriendo todas las funciones.",
        "Unos pocos saltos y operaciones suelen bastar para reconstruir la lógica si sigues el camino de validación principal.",
        "No hace falta parchear el ejecutable. El reto pide comprender la condición correcta y derivar de ahí la respuesta esperada.",
    ),
    "Licencia bajo revisión": hs(
        "No busques una sola función mágica. Aquí la verificación está repartida.",
        "Traza cómo se pasa y transforma la entrada entre rutinas antes de decidir qué parte del binario importa de verdad.",
        "La clave del reto es recomponer la lógica distribuida. Si solo miras una comparación local, te faltará contexto para la licencia completa.",
    ),
    "Perfil disperso": hs(
        "Empieza por una identidad base: nombre, alias o handle, y sigue solo coincidencias razonables.",
        "Valora patrones repetidos entre perfiles, imágenes, biografías y horarios de publicación antes de asumir que dos cuentas pertenecen a la misma persona.",
        "La respuesta útil sale de la correlación entre varias fuentes. Una sola coincidencia débil no basta para cerrar el reto.",
    ),
    "Agenda filtrada": hs(
        "No leas la agenda solo como calendario; léela como mapa de relaciones y prioridades.",
        "Cruza horarios, asistentes, lugares o notas anexas para detectar qué entrada realmente cambia la lectura del caso.",
        "La flag aparece cuando distingues la pista operacional dentro de la agenda, no cuando resumes todo el documento.",
    ),
    "Foto del laboratorio": hs(
        "Haz una pasada amplia y luego una segunda centrada en detalles textuales, reflejos y pantallas.",
        "Amplía sin perder contexto: etiquetas, documentos visibles, periféricos o lo que asoma en monitores puede ser más valioso que la escena general.",
        "La solución suele salir de combinar dos o tres detalles de la misma foto. Mirar un solo rincón rara vez basta.",
    ),
    "Proveedor fantasma": hs(
        "Sigue primero la pista más concreta: dominio, firma, marca, formato de contacto o documento citado.",
        "No todas las menciones tienen el mismo peso. Prioriza las que conectan una fuente con otra de forma verificable.",
        "La respuesta fuerte sale de atribuir correctamente al proveedor usando varias huellas pequeñas, no una sola mención ambigua.",
    ),
    "Huella de publicación": hs(
        "Empieza comparando fechas, nombres de archivo y forma de publicación entre las evidencias.",
        "Fíjate en residuos de edición, versiones, plataformas o patrones de exportación que puedan apuntar a un origen común.",
        "El reto se resuelve al reconstruir la cadena de publicación con varias señales coherentes, no con una intuición aislada.",
    ),
    "XOR de respaldo": hs(
        "Si dos salidas comparten estructura y contexto, piensa en reutilización antes que en cifrado fuerte roto.",
        "La nota del bundle sobre encabezado común no es decorativa: úsala para interpretar por qué ambos textos se parecen tanto.",
        "La respuesta final pide identificar el problema, recuperar la frase relevante y justificarla con un indicador técnico concreto.",
    ),
    "Firma reciclada": hs(
        "Busca qué pieza de material criptográfico se repite donde no debería hacerlo.",
        "En firmas, una repetición operativa suele importar más que el algoritmo mismo. Examina nonce, reto, semilla o elemento efímero asociado.",
        "La solución no es 'la firma está mal'; es explicar qué se recicló, qué implica y qué evidencia del bundle lo demuestra.",
    ),
    "RSA sin OAEP": hs(
        "No te centres solo en la clave. Aquí importa cómo se está usando RSA.",
        "Revisa si el material sugiere un esquema antiguo o un relleno insuficiente frente a las prácticas modernas.",
        "La respuesta valiosa identifica la debilidad del esquema y la mejora esperada. El reto no premia repetir 'usar RSA es malo', sino precisar por qué el uso actual es débil.",
    ),
    "Derivación lenta": hs(
        "La función crítica es la que deriva el secreto, no la que lo compara o lo serializa.",
        "Si la sal sigue fija o las iteraciones no quedan claras, el cambio todavía no mejora realmente la política.",
        "El validador espera una KDF moderna con parámetros visibles y razonables. Piensa en PBKDF2-HMAC-SHA256, sal aleatoria y costo explícito.",
    ),
    "Bloques repetidos": hs(
        "Cuenta bloques repetidos antes de pensar en una clave o en descifrado.",
        "Cuando la misma huella hexadecimal se repite, el modo de operación suele estar filtrando estructura del contenido.",
        "La respuesta final necesita modo, hallazgo y mitigación. Si solo nombras ECB sin explicar qué se ve y cómo evitarlo, te falta parte del reto.",
    ),
    "CBC sin integridad": hs(
        "Aquí no falta confidencialidad; falta una forma fiable de detectar alteraciones del mensaje.",
        "Si el backend acepta ciphertext modificado y solo cambia el resultado descifrado, piensa en ausencia de autenticación del mensaje.",
        "La respuesta completa distingue modo, riesgo y mitigación. La pista fuerte es que CBC por sí solo no resuelve integridad.",
    ),
    "IV reciclado en reportes": hs(
        "Compara el IV y el primer bloque de ambos reportes antes de revisar cualquier otra cosa.",
        "Si el prefijo del mensaje coincide y también lo hace el primer bloque, pregúntate qué parámetro se reutilizó indebidamente.",
        "La solución fuerte nombra el problema exacto, el hallazgo observable y la política correcta: IV único y aleatorio por mensaje.",
    ),
    "HMAC truncado en gateway": hs(
        "El algoritmo no es el problema principal; revisa cómo se verifica la firma recibida.",
        "Si la comparación usa solo unos pocos caracteres del HMAC o una igualdad ingenua, la garantía de integridad queda degradada.",
        "El parche correcto valida longitud completa y usa comparación constante sobre la firma entera. Cualquier atajo sigue siendo caro en seguridad.",
    ),
    "Semilla predecible": hs(
        "El dato importante no es cuántos bytes salen, sino de dónde sale la aleatoriedad.",
        "Si el generador depende de `time` o de una semilla reproducible, ya tienes el foco del problema.",
        "La solución esperada elimina el PRNG generalista y usa una fuente adecuada para secretos sin perder el formato de salida del sistema.",
    ),
    "Certificados a ciegas": hs(
        "No mires la petición HTTP todavía; mira cómo se construye el contexto TLS.",
        "Si el cliente sigue aceptando cualquier certificado o ignora el hostname, la corrección no está completa.",
        "El reto queda bien resuelto cuando validas cadena y nombre del host con la CA correcta, no cuando solo quitas un warning de compatibilidad.",
    ),
    "Cronología cruzada": hs(
        "Ordena primero las evidencias por tiempo antes de interpretar qué significa cada una.",
        "La publicación pivote no es la primera ni la última, sino la que cambia el estado del artefacto y la acción del actor.",
        "La respuesta final necesita fecha, actor y artefacto. Si no puedes explicar por qué esa secuencia es la única coherente, todavía no cerraste el caso.",
    ),
    "Repositorio fantasma": hs(
        "La captura solo sugiere el nombre; la atribución completa está en la fuente que conserva la ruta exacta.",
        "Cruza el export de issues con el changelog antes de decidir repo, organización y tag.",
        "No entregues un fragmento. La validación espera los tres campos completos: repo, organización y versión exacta.",
    ),
    "Credencial en ponencia": hs(
        "No intentes reconstruir la identidad desde una sola evidencia; este reto exige combinar fragmentos.",
        "La lista de asistentes reduce candidatos, pero la nota de backstage es la que confirma el track correcto.",
        "La respuesta fuerte descarta homónimos o alias parecidos. Necesitas nombre completo, alias exacto y track sin ambigüedad.",
    ),
    "Red de proveedores": hs(
        "Empieza por detectar qué empresa aparece conectada a más de una fuente y no solo mencionada una vez.",
        "El dominio compartido pesa más que una abreviatura comercial cuando toca unir documentos y contactos.",
        "La solución final exige empresa pivote, dominio y documento conector. Si uno sale solo por intuición, vuelve a mapear relaciones.",
    ),
    "Trazas de convocatoria": hs(
        "Lee el PDF como artefacto de producción: propiedades, renombres y versiones importan tanto como el contenido visible.",
        "El nombre público final no es necesariamente el nombre maestro. Cruza versión archivada con nota de distribución.",
        "La validación espera documento maestro, editor y lote interno. La fuente fuerte está en la intersección entre propiedades y archivo archivado.",
    ),
    "Traza en PCAP": hs(
        "No leas la captura como si fuera un bloque de texto plano. Piensa en qué herramienta de Kali te permite filtrar rápido por host y ruta.",
        "Las peticiones de estado están ahí para distraer. La descarga relevante es la que apunta a un recurso exportado y no a una comprobación de salud.",
        "La respuesta final necesita herramienta, host y recurso exacto. Si no puedes explicar por qué esa petición es la importante, todavía no cerraste el triage.",
    ),
    "Firmware en capas": hs(
        "Aquí la pista no está en el encabezado del firmware, sino en lo que aparece embebido al inspeccionarlo por capas.",
        "Busca el artefacto incrustado que sea legible y que revele configuración operativa, no solo estructura del contenedor.",
        "La validación espera herramienta, artefacto y hallazgo. Si solo nombras binwalk sin decir qué encontraste y por qué importa, te falta la mitad del reto.",
    ),
    "Metadatos en cascada": hs(
        "No intentes resolverlo mirando solo la imagen. Este reto vive en los metadatos que sobreviven entre exportaciones.",
        "Autor, comentarios y variantes del nombre apuntan a la misma persona y a una misma ubicación si los correlacionas bien.",
        "La respuesta final necesita herramienta, editor y ubicación exacta. Una coincidencia suelta no basta; necesitas repetición entre archivos.",
    ),
    "Carving de evidencias": hs(
        "Piensa primero en recuperación por firmas y tipos de archivo, no en un visor general de la evidencia.",
        "El archivo importante no es el más vistoso ni el más grande; es el que cambia la comprensión operativa del caso.",
        "La solución fuerte nombra herramienta, archivo y detalle relevante. Si solo dices 'foremost' o solo das el nombre del archivo, te falta contexto crítico.",
    ),
    "Diccionario de laboratorio": hs(
        "No hace falta atacar todos los hashes para resolver el reto. Primero decide qué herramienta y qué contexto hacen más sentido.",
        "La política interna del bundle te dice más sobre la wordlist correcta que cualquier lista genérica enorme.",
        "La validación espera herramienta, cuenta y diccionario concretos. Si tu respuesta ignora el contexto operativo del laboratorio, estás dejando fuera la parte importante.",
    ),
    "Portal sin redirección segura": hs(
        "No pierdas tiempo en la aplicación. Aquí el punto débil está en el borde que todavía permite entrar por HTTP.",
        "Necesitas dos piezas: un bloque que reciba el 80 y un bloque seguro que sirva la app con certificado declarado.",
        "La corrección completa incluye redirección explícita a `https://$host$request_uri`, listener `443 ssl` y referencias a certificado y llave. Si una de esas piezas falta, el tránsito sigue incompleto.",
    ),
    "HSTS pendiente": hs(
        "El sitio ya tiene TLS, pero todavía no le está diciendo al navegador que debe recordarlo.",
        "Busca la forma correcta de anunciar una política de transporte persistente dentro del bloque HTTPS, no como comentario ni como redirect adicional.",
        "La validación espera una cabecera `Strict-Transport-Security` con `max-age=31536000`, `includeSubDomains` y `always`. Si falta uno, la política queda coja para este escenario.",
    ),
    "Cookie de sesión sin Secure": hs(
        "No toques el proxy ni el HTML. El problema vive en cómo la aplicación define su cookie de sesión.",
        "Piensa en los tres atributos básicos que deberían quedar razonables en un portal ya migrado a HTTPS: transporte, acceso desde script y contexto de envío.",
        "La solución fuerte activa `SESSION_COOKIE_SECURE`, mantiene `HttpOnly` y deja `SameSite` en un valor defensivo sin romper navegación normal. Si sigues en modo de pruebas, todavía falta endurecimiento.",
    ),
    "Contenido mixto heredado": hs(
        "Aquí suele haber más de una referencia insegura. Revisa tanto la plantilla como el JavaScript cliente.",
        "Si todavía aparece una sola URL `http://` hacia recursos o API del laboratorio, el navegador seguirá viendo contenido mixto.",
        "La validación comprueba HTML y JS. Necesitas llevar scripts, imágenes y llamada al API a `https://`, no solo arreglar el primer recurso que salta a la vista.",
    ),
    "Credenciales expuestas en tránsito": hs(
        "No busques una explotación complicada. El incidente es más básico: el login viajó por un canal que no debió aceptar credenciales.",
        "Cruza resumen de tráfico, método y proxy para encontrar qué host y qué ruta recibieron el POST en HTTP antes del cierre de la migración.",
        "La respuesta final no pide un payload ni un atacante. Pide portal, ruta sensible e impacto observado: credenciales legibles en texto plano durante el tránsito.",
    ),
}


EXPECTED_CHALLENGE_COUNT = 76
