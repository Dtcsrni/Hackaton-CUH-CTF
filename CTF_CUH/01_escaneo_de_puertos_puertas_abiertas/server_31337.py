"""Servidor TCP simple para el reto \"Puertas abiertas\"."""

from __future__ import annotations

import socketserver


HOST = "0.0.0.0"
PORT = 31337
RESPONSE = (
    "CUH Training Service Ready\n"
    "flag=CUH{escanear_antes_de_interpretar}\n"
).encode("utf-8")


class TrainingRequestHandler(socketserver.BaseRequestHandler):
    """Entrega un banner fijo a cada cliente que se conecta."""

    def handle(self) -> None:
        client_ip, client_port = self.client_address
        print(f"[+] Conexion entrante desde {client_ip}:{client_port}")
        try:
            self.request.sendall(RESPONSE)
        except OSError as exc:
            print(f"[!] Error al responder a {client_ip}:{client_port}: {exc}")


class ReusableThreadingTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


def main() -> None:
    try:
        with ReusableThreadingTCPServer((HOST, PORT), TrainingRequestHandler) as server:
            print(f"[*] Servicio escuchando en {HOST}:{PORT}")
            print("[*] Presione Ctrl+C para detener el servicio.")
            server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Servicio detenido por el organizador.")
    except OSError as exc:
        print(f"[!] No fue posible iniciar el servicio en {HOST}:{PORT}: {exc}")


if __name__ == "__main__":
    main()
