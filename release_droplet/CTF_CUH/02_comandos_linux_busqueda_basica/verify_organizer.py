from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile


EXPECTED_FILES = {
    "reto_linux/README.txt",
    "reto_linux/notas/sistema.log",
    "reto_linux/notas/usuarios.txt",
    "reto_linux/evidencia/instrucciones.txt",
    "reto_linux/evidencia/pista.tmp",
    "reto_linux/evidencia/oculto/flag.txt",
}
EXPECTED_FLAG = "CUH{linux_tambien_se_investiga}"


def main() -> None:
    zip_path = Path(__file__).resolve().parent / "reto_archivos_linux.zip"
    if not zip_path.exists():
        raise SystemExit(f"No existe el ZIP esperado: {zip_path}")

    with ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        missing = sorted(EXPECTED_FILES - names)
        if missing:
            raise SystemExit(f"Faltan archivos en el ZIP: {missing}")

        flag_text = archive.read("reto_linux/evidencia/oculto/flag.txt").decode("utf-8").strip()
        if flag_text != EXPECTED_FLAG:
            raise SystemExit(f"Flag inesperada dentro del ZIP: {flag_text!r}")

    print(EXPECTED_FLAG)
    print("OK")


if __name__ == "__main__":
    main()
