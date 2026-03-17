from __future__ import annotations

from challenge_description_overrides import DESCRIPTIONS, EXPECTED_CHALLENGE_COUNT
from challenge_help_links import HELP_LINKS, REQUIRED_INLINE_ARTIFACTS
from challenge_hint_overrides import HINTS


def main() -> None:
    problems: list[str] = []

    if len(DESCRIPTIONS) != EXPECTED_CHALLENGE_COUNT:
        problems.append(
            f"DESCRIPTIONS tiene {len(DESCRIPTIONS)} entradas y esperaba {EXPECTED_CHALLENGE_COUNT}"
        )

    if len(HINTS) != 76:
        problems.append(f"HINTS tiene {len(HINTS)} entradas y esperaba 76")

    missing_help_links = sorted(name for name in DESCRIPTIONS if name not in HELP_LINKS)
    if missing_help_links:
        problems.append(
            "Misiones sin página de ayuda asociada: " + ", ".join(missing_help_links)
        )

    missing_inline_artifacts = []
    for challenge_name, markers in REQUIRED_INLINE_ARTIFACTS.items():
        description = DESCRIPTIONS.get(challenge_name, "")
        if description and not any(marker in description for marker in markers):
            missing_inline_artifacts.append(
                f"{challenge_name} (faltan marcadores: {', '.join(markers)})"
            )
    if missing_inline_artifacts:
        problems.append(
            "Misiones con insumo explícito pendiente en el enunciado: "
            + ", ".join(missing_inline_artifacts)
        )

    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)

    print("challenge_sources_ok")


if __name__ == "__main__":
    main()
