# Verificación local del reto Puertas abiertas

## Pasos exactos para validar el reto antes del evento
1. Abrir PowerShell en `O:\Descargas\hackaton\CTF_CUH\01_escaneo_de_puertos_puertas_abiertas`.
2. Iniciar el servicio:

```powershell
python .\server_31337.py
```

3. Confirmar desde otra consola de PowerShell que el proceso está corriendo:

```powershell
Get-Process python
```

4. Confirmar que el puerto 31337 está en escucha:

```powershell
Get-NetTCPConnection -LocalPort 31337 -State Listen
```

5. Confirmar conectividad local al puerto:

```powershell
Test-NetConnection -ComputerName 127.0.0.1 -Port 31337
```

6. Confirmar el banner recibido:

```powershell
$client = [System.Net.Sockets.TcpClient]::new("127.0.0.1",31337)
$stream = $client.GetStream()
$reader = New-Object System.IO.StreamReader($stream)
$reader.ReadToEnd()
$reader.Dispose()
$client.Dispose()
```

## Comandos de Kali esperados

```bash
ping -c 3 192.168.56.25
nmap -sS -Pn 192.168.56.25
nmap -sV -p 31337 192.168.56.25
nc 192.168.56.25 31337
```

## Resultado esperado de cada prueba
### `Get-Process python`
Debe mostrar al menos un proceso `python` asociado a la ejecución del servidor.

### `Get-NetTCPConnection -LocalPort 31337 -State Listen`
Debe mostrar `LocalPort` igual a `31337` y estado `Listen`.

### `Test-NetConnection -ComputerName 127.0.0.1 -Port 31337`
`TcpTestSucceeded` debe ser `True`.

### Lectura del banner en PowerShell
Debe devolver exactamente:

```text
CUH Training Service Ready
flag=CUH{escanear_antes_de_interpretar}
```

### `ping -c 3 192.168.56.25`
Debe responder si la red del laboratorio permite ICMP. Si ICMP no responde, el reto aún puede validarse con `nmap -Pn` y `nc`.

### `nmap -sS -Pn 192.168.56.25`
Debe listar `31337/tcp open`.

### `nmap -sV -p 31337 192.168.56.25`
Debe confirmar que el puerto `31337/tcp` está abierto y accesible.

### `nc 192.168.56.25 31337`
Debe mostrar exactamente:

```text
CUH Training Service Ready
flag=CUH{escanear_antes_de_interpretar}
```

## Checklist de aprobación del reto
- El script inicia sin error en Windows.
- El puerto `31337` aparece en escucha.
- El banner entrega la flag correcta.
- La IP documentada coincide con la topología elegida o ya fue actualizada.
- Kali Linux puede alcanzar el servicio por TCP.
- El texto de CTFd no revela el puerto explícitamente.
