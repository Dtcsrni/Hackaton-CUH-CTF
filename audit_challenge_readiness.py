from __future__ import annotations

from pathlib import Path

from CTFd import create_app
from CTFd.models import ChallengeFiles, Challenges, Flags, Hints

from challenge_help_links import HELP_LINKS, REQUIRED_INLINE_ARTIFACTS

REQUIRED_HEADINGS = (
    "### Insumos disponibles",
    "### Objetivo de cierre",
    "### Archivos del reto",
    "### Material de apoyo",
)


def main() -> None:
    app = create_app()
    with app.app_context():
        missing_flags: list[str] = []
        bad_hints: list[str] = []
        bad_sections: list[str] = []
        bad_help_links: list[str] = []
        bad_inline_artifacts: list[str] = []
        missing_files: list[str] = []
        bad_file_mentions: list[str] = []

        for challenge in Challenges.query.order_by(Challenges.id.asc()).all():
            description = challenge.description or ""
            files = ChallengeFiles.query.filter_by(challenge_id=challenge.id).all()
            file_names = [Path(item.location or "").name for item in files if item.location]

            if not Flags.query.filter_by(challenge_id=challenge.id).count():
                missing_flags.append(challenge.name)

            if challenge.state != "hidden" and Hints.query.filter_by(challenge_id=challenge.id).count() != 3:
                bad_hints.append(challenge.name)

            for heading in REQUIRED_HEADINGS:
                if heading not in description:
                    bad_sections.append(f"{challenge.name}: {heading}")

            route_label = HELP_LINKS.get(challenge.name)
            if route_label is None:
                bad_help_links.append(f"{challenge.name}: sin mapeo de ayuda")
            else:
                route, _label = route_label
                if f"](/{route})" not in description:
                    bad_help_links.append(f"{challenge.name}: falta link /{route}")

            required_markers = REQUIRED_INLINE_ARTIFACTS.get(challenge.name, ())
            if required_markers and not any(marker in description for marker in required_markers):
                markers = " | ".join(required_markers)
                bad_inline_artifacts.append(
                    f"{challenge.name}: falta insumo explícito en el enunciado ({markers})"
                )

            if not files and "no depende de adjuntos descargables" not in description.lower():
                bad_file_mentions.append(f"{challenge.name}: falta aclarar que no hay adjuntos")

            for item in files:
                location = item.location or ""
                if not (Path("/var/uploads") / location).exists():
                    missing_files.append(f"{challenge.name}: {location}")

            for file_name in file_names:
                if file_name not in description:
                    bad_file_mentions.append(f"{challenge.name}: no menciona {file_name}")

        if (
            missing_flags
            or bad_hints
            or bad_sections
            or bad_help_links
            or bad_inline_artifacts
            or missing_files
            or bad_file_mentions
        ):
            if missing_flags:
                print("missing_flags", missing_flags)
            if bad_hints:
                print("bad_hints", bad_hints)
            if bad_sections:
                print("bad_sections", bad_sections)
            if bad_help_links:
                print("bad_help_links", bad_help_links)
            if bad_inline_artifacts:
                print("bad_inline_artifacts", bad_inline_artifacts)
            if missing_files:
                print("missing_files", missing_files)
            if bad_file_mentions:
                print("bad_file_mentions", bad_file_mentions)
            raise SystemExit(1)

        print("challenge_readiness_ok")


if __name__ == "__main__":
    main()
