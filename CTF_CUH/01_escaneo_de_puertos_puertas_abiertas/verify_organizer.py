from __future__ import annotations

import socket
import threading
import time

from server_31337 import RESPONSE, ReusableThreadingTCPServer, TrainingRequestHandler


def main() -> None:
    with ReusableThreadingTCPServer(("127.0.0.1", 0), TrainingRequestHandler) as server:
        port = server.server_address[1]
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()

        deadline = time.time() + 5
        payload = b""
        while time.time() < deadline:
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=1.0) as conn:
                    payload = conn.recv(4096)
                break
            except OSError:
                time.sleep(0.1)

        server.shutdown()
        worker.join(timeout=2)

    text = payload.decode("utf-8")
    if text != RESPONSE.decode("utf-8"):
        raise SystemExit(f"Respuesta inesperada: {text!r}")

    if "CUH{" not in text:
        raise SystemExit("No se encontró la flag en el banner.")

    flag = next(line.split("=", 1)[1] for line in text.splitlines() if line.startswith("flag="))
    print(flag)
    print("OK")


if __name__ == "__main__":
    main()
