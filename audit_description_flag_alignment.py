from __future__ import annotations

import base64
import re
from pathlib import Path

from challenge_description_overrides import DESCRIPTIONS


EXPECTED_INLINE_RESULTS = {
    "Base64 no es cifrado": "CUH{base64_es_solo_codificacion}",
    "César escolar": "CUH{cesar_es_inicio}",
}


def _decode_caesar(text: str, shift: int) -> str:
    out: list[str] = []
    for ch in text:
        if "a" <= ch <= "z":
            out.append(chr((ord(ch) - 97 - shift) % 26 + 97))
        elif "A" <= ch <= "Z":
            out.append(chr((ord(ch) - 65 - shift) % 26 + 65))
        else:
            out.append(ch)
    return "".join(out)


def main() -> None:
    errors: list[str] = []

    base64_desc = DESCRIPTIONS["Base64 no es cifrado"]
    base64_match = re.search(r"Cadena Base64:\s*`([^`]+)`", base64_desc)
    if not base64_match:
        errors.append("Base64 no es cifrado: falta la cadena Base64 inline")
    else:
        decoded = base64.b64decode(base64_match.group(1)).decode("utf-8")
        if decoded != EXPECTED_INLINE_RESULTS["Base64 no es cifrado"]:
            errors.append(
                "Base64 no es cifrado: "
                f"decodifica a {decoded} y no a "
                f"{EXPECTED_INLINE_RESULTS['Base64 no es cifrado']}"
            )

    caesar_desc = DESCRIPTIONS["César escolar"]
    caesar_match = re.search(r"Texto cifrado:\s*`([^`]+)`", caesar_desc)
    if not caesar_match:
        errors.append("César escolar: falta el texto cifrado inline")
    else:
        cipher = caesar_match.group(1)
        candidates = {_decode_caesar(cipher, shift) for shift in range(26)}
        if EXPECTED_INLINE_RESULTS["César escolar"] not in candidates:
            errors.append(
                "César escolar: ninguna rotación produce "
                f"{EXPECTED_INLINE_RESULTS['César escolar']}"
            )

    if errors:
        print("INLINE_FLAG_ALIGNMENT_FAILED")
        for error in errors:
            print(error)
        raise SystemExit(1)

    print(
        f"OK descriptions_checked={len(DESCRIPTIONS)} "
        f"source={Path(__file__).name}"
    )


if __name__ == "__main__":
    main()
