# Datos para CTFd: Puertas abiertas

## Name
Puertas abiertas

## Category
Reconocimiento

## Value
300

## Type
standard

## State
visible

## Description final lista para pegar en CTFd
En este entorno autorizado del hackathon CUH se ha publicado un servicio de laboratorio en la IP `192.168.56.25`. Tu objetivo es observar, enumerar e interpretar lo que realmente está expuesto antes de sacar conclusiones. Usa herramientas de reconocimiento desde Kali Linux y valida manualmente cualquier hallazgo relevante dentro de este laboratorio académico controlado.

## Flag
`CUH{escanear_antes_de_interpretar}`

## Hints
1. Antes de interpretar un servicio, enumera qué puertos están abiertos.
2. Un servicio útil no siempre está en un puerto estándar.
3. Después de identificar el puerto, una conexión manual puede aclarar el hallazgo.

## Dinámica esperada del alumno
- Confirmar conectividad con la IP de laboratorio.
- Enumerar puertos con `nmap`.
- Detectar que existe un servicio accesible.
- Abrir una conexión manual con `nc`.
- Leer el banner y enviar la flag a CTFd.

## Herramientas esperadas en Kali
- `ping`
- `nmap`
- `nc`

## Nota pedagógica breve para el organizador
Este reto refuerza la secuencia correcta de trabajo: primero enumerar, luego interpretar. La flag no requiere explotación; solo observación técnica dentro del laboratorio controlado.
