# Reto 1: Puertas abiertas

## Propósito didáctico del reto
Este reto introduce reconocimiento básico de red dentro de un laboratorio académico controlado y autorizado. El alumno debe confirmar conectividad, enumerar puertos abiertos y validar manualmente qué ofrece un servicio expuesto en un puerto no estándar.

## Conocimientos previos requeridos
- Uso básico de terminal en Kali Linux.
- Comprensión elemental de direcciones IP y puertos TCP.
- Manejo inicial de `nmap` y `nc`.

## Qué aprende el alumno
- A comprobar primero la conectividad antes de interpretar resultados.
- A usar `nmap` para enumerar puertos y servicios.
- A confirmar manualmente un hallazgo con `netcat`.
- A no asumir que un servicio relevante vive en un puerto común.

## Ejecución del servidor en Windows
Ubicación del archivo:

`CTF_CUH/01_escaneo_de_puertos_puertas_abiertas/server_31337.py`

Comando recomendado:

```powershell
cd O:\Descargas\hackaton\CTF_CUH\01_escaneo_de_puertos_puertas_abiertas
python .\server_31337.py
```

Comando alternativo si el organizador tiene instalado Python Launcher:

```powershell
py .\server_31337.py
```

Resultado esperado en consola:

```text
[*] Servicio escuchando en 0.0.0.0:31337
[*] Presione Ctrl+C para detener el servicio.
```

## Cómo permitir el puerto en firewall si fuera necesario
Si Windows Defender Firewall bloquea conexiones entrantes, crear una regla temporal para TCP 31337:

```powershell
New-NetFirewallRule -DisplayName "CTF CUH Puerto 31337" -Direction Inbound -Protocol TCP -LocalPort 31337 -Action Allow
```

Para eliminarla al terminar:

```powershell
Remove-NetFirewallRule -DisplayName "CTF CUH Puerto 31337"
```

## Cómo probarlo localmente en Windows
Con el servidor ya iniciado:

```powershell
Test-NetConnection -ComputerName 127.0.0.1 -Port 31337
```

Prueba de banner con PowerShell:

```powershell
$client = [System.Net.Sockets.TcpClient]::new("127.0.0.1",31337)
$stream = $client.GetStream()
$reader = New-Object System.IO.StreamReader($stream)
$reader.ReadToEnd()
$reader.Dispose()
$client.Dispose()
```

Respuesta esperada:

```text
CUH Training Service Ready
flag=CUH{escanear_antes_de_interpretar}
```

## Cómo probarlo desde Kali Linux
En esta documentación se usa `192.168.56.25` como IP de laboratorio de referencia. Debe apuntar a la interfaz Windows visible desde la VM Kali.

Pruebas recomendadas:

```bash
ping -c 3 192.168.56.25
nmap -sS -Pn 192.168.56.25
nmap -sV -p 31337 192.168.56.25
nc 192.168.56.25 31337
```

Resultados esperados:
- `ping` responde si la topología elegida permite ICMP.
- `nmap -sS -Pn` detecta `31337/tcp open`.
- `nmap -sV -p 31337` identifica un servicio TCP accesible y muestra el puerto abierto.
- `nc` devuelve el banner con la flag.

## Cómo cambiar la IP objetivo en la documentación si la red cambia
La IP `192.168.56.25` es solo una referencia documentada. Si el laboratorio usa otra red:

1. Actualice la IP en [DATOS_CTFD.md](./DATOS_CTFD.md).
2. Actualice la IP en [verificacion_local.md](./verificacion_local.md).
3. Actualice la IP en el material global [README_GENERAL_ORGANIZADOR.md](../README_GENERAL_ORGANIZADOR.md).
4. Verifique que la VM Kali puede alcanzar esa nueva IP.

El script no necesita cambios mientras siga escuchando en `0.0.0.0:31337`.

## Errores comunes
- El servidor no está iniciado al momento de probar.
- La VM Kali quedó en un modo de red que no ve al host Windows.
- Firewall de Windows bloquea TCP 31337.
- El organizador documentó una IP que no coincide con la interfaz real del host.
- Se usa `nmap` sobre otra IP por confusión con NAT o adaptadores múltiples.

## Solución rápida de problemas
- Confirmar proceso activo con `Get-Process python`.
- Confirmar escucha del puerto con `Get-NetTCPConnection -LocalPort 31337 -State Listen`.
- Confirmar IP del host con `ipconfig`.
- Si no hay conectividad desde Kali, revisar `Host-only` o `Red interna` en VirtualBox.
- Si `ping` falla pero `nmap -Pn` funciona, el problema puede limitarse a ICMP; el reto sigue siendo válido si TCP 31337 responde.
