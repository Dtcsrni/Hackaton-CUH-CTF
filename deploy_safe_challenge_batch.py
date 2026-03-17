from __future__ import annotations

import json
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parent
REFRESH_ROOT = ROOT / "refresh_assets"
MANIFEST = ROOT / "safe_challenges_manifest.json"
DESCRIPTION_OVERRIDES = ROOT / "challenge_description_overrides.py"
APPLY_DESCRIPTIONS = ROOT / "apply_challenge_description_overrides.py"
HINT_OVERRIDES = ROOT / "challenge_hint_overrides.py"
APPLY_HINTS = ROOT / "apply_challenge_hint_overrides.py"
FIRST_BLOOD_PLUGIN = ROOT / "ctfd_custom_plugins" / "first_blood_bonus" / "__init__.py"
SOLVE_EVIDENCE_PLUGIN = ROOT / "ctfd_custom_plugins" / "solve_evidence_guard" / "__init__.py"
USER_PRESENCE_PLUGIN = ROOT / "ctfd_custom_plugins" / "user_presence_board" / "__init__.py"
ADMIN_NOTIFICATIONS_PLUGIN = ROOT / "ctfd_custom_plugins" / "admin_notifications_console" / "__init__.py"
ADMIN_NOTIFICATIONS_TEMPLATE = ROOT / "refresh_assets" / "templates" / "admin" / "notifications.html"
ADMIN_EVIDENCE_REVIEW_TEMPLATE = ROOT / "refresh_assets" / "templates" / "admin" / "evidence_review.html"
CHALLENGES_TEMPLATE = ROOT / "refresh_assets" / "templates" / "challenges.html"
NOTIFICATIONS_TEMPLATE = ROOT / "refresh_assets" / "templates" / "notifications.html"
USER_PRIVATE_TEMPLATE = ROOT / "refresh_assets" / "templates" / "users" / "private.html"
KEY = Path(r"C:\Users\evega\.ssh\codex_ctfd_cuh")
REMOTE = "codexdeploy@45.55.49.111"
CONTAINER = "ctfd-ctfd-1"


def run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)


def write_tmp(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    generated_pages = json.loads((REFRESH_ROOT / "generated_safe_pages.json").read_text(encoding="utf-8"))

    with TemporaryDirectory() as tmp_raw:
        tmp = Path(tmp_raw)
        upload_root = tmp / "cuh_safe_upload"
        pages_dir = upload_root / "refresh_assets" / "pages"
        bundles_dir = upload_root / "bundles"
        plugin_dir = upload_root / "plugins" / "first_blood_bonus"
        solve_evidence_plugin_dir = upload_root / "plugins" / "solve_evidence_guard"
        user_presence_plugin_dir = upload_root / "plugins" / "user_presence_board"
        admin_notifications_plugin_dir = upload_root / "plugins" / "admin_notifications_console"
        admin_templates_dir = upload_root / "templates" / "admin"
        user_templates_dir = upload_root / "templates" / "users"
        pages_dir.mkdir(parents=True, exist_ok=True)
        bundles_dir.mkdir(parents=True, exist_ok=True)
        plugin_dir.mkdir(parents=True, exist_ok=True)
        solve_evidence_plugin_dir.mkdir(parents=True, exist_ok=True)
        user_presence_plugin_dir.mkdir(parents=True, exist_ok=True)
        admin_notifications_plugin_dir.mkdir(parents=True, exist_ok=True)
        admin_templates_dir.mkdir(parents=True, exist_ok=True)
        user_templates_dir.mkdir(parents=True, exist_ok=True)

        write_tmp(
            upload_root / "refresh_assets" / "actualizar_paginas_ctfd.sh",
            (REFRESH_ROOT / "actualizar_paginas_ctfd.sh").read_text(encoding="utf-8"),
        )
        shutil.copy2(REFRESH_ROOT / "generated_safe_pages.json", upload_root / "refresh_assets" / "generated_safe_pages.json")
        shutil.copy2(MANIFEST, upload_root / "safe_challenges_manifest.json")
        shutil.copy2(DESCRIPTION_OVERRIDES, upload_root / "challenge_description_overrides.py")
        shutil.copy2(APPLY_DESCRIPTIONS, upload_root / "apply_challenge_description_overrides.py")
        shutil.copy2(HINT_OVERRIDES, upload_root / "challenge_hint_overrides.py")
        shutil.copy2(APPLY_HINTS, upload_root / "apply_challenge_hint_overrides.py")
        shutil.copy2(FIRST_BLOOD_PLUGIN, plugin_dir / "__init__.py")
        shutil.copy2(SOLVE_EVIDENCE_PLUGIN, solve_evidence_plugin_dir / "__init__.py")
        shutil.copy2(USER_PRESENCE_PLUGIN, user_presence_plugin_dir / "__init__.py")
        shutil.copy2(ADMIN_NOTIFICATIONS_PLUGIN, admin_notifications_plugin_dir / "__init__.py")
        shutil.copy2(ADMIN_NOTIFICATIONS_TEMPLATE, admin_templates_dir / "notifications.html")
        shutil.copy2(ADMIN_EVIDENCE_REVIEW_TEMPLATE, admin_templates_dir / "evidence_review.html")
        shutil.copy2(CHALLENGES_TEMPLATE, upload_root / "templates" / "challenges.html")
        shutil.copy2(NOTIFICATIONS_TEMPLATE, upload_root / "templates" / "notifications.html")
        shutil.copy2(USER_PRIVATE_TEMPLATE, user_templates_dir / "private.html")

        for page_file in (REFRESH_ROOT / "pages").glob("*.html"):
            shutil.copy2(page_file, pages_dir / page_file.name)
        for spec in manifest["challenges"]:
            bundle = ROOT / spec["attachment"]
            shutil.copy2(bundle, bundles_dir / Path(spec["attachment"]).name)

        apply_script = textwrap.dedent(
            """
            import json
            from pathlib import Path
            from werkzeug.datastructures import FileStorage
            from CTFd import create_app
            from CTFd.cache import clear_challenges
            from CTFd.models import Challenges, Flags, Hints, ChallengeFiles, db
            from CTFd.utils.uploads import upload_file

            manifest = json.loads(Path('/tmp/safe_challenges_manifest.json').read_text(encoding='utf-8'))
            app = create_app()
            with app.app_context():
                for spec in manifest['challenges']:
                    chal = Challenges.query.filter_by(name=spec['name']).first()
                    if chal is None:
                        chal = Challenges()
                        db.session.add(chal)
                        db.session.flush()
                    chal.name = spec['name']
                    chal.category = spec['category']
                    chal.value = spec['value']
                    chal.type = spec['type']
                    chal.state = spec['state']
                    chal.description = spec['description']
                    Flags.query.filter_by(challenge_id=chal.id).delete()
                    Hints.query.filter_by(challenge_id=chal.id).delete()
                    ChallengeFiles.query.filter_by(challenge_id=chal.id).delete()
                    db.session.flush()
                    db.session.add(Flags(challenge_id=chal.id, type='static', content=spec['flag'], data='case_insensitive'))
                    for hint in spec['hints']:
                        db.session.add(Hints(challenge_id=chal.id, type='standard', content=hint['content'], cost=hint['cost'], requirements=None))
                    db.session.commit()
                    bundle = Path('/tmp/cuh-bundles') / Path(spec['attachment']).name
                    with bundle.open('rb') as fh:
                        fs = FileStorage(stream=fh, filename=bundle.name, name='file', content_type='application/zip')
                        upload_file(file=fs, type='challenge', challenge_id=chal.id)
                    db.session.commit()
                clear_challenges()
                print('safe challenges synced', len(manifest['challenges']))
            """
        ).strip() + "\n"
        write_tmp(upload_root / "apply_safe_challenges.py", apply_script)

        remote_script = textwrap.dedent(
            f"""
            #!/usr/bin/env bash
            set -euo pipefail
            WORK=/tmp/cuh_safe_batch
            rm -rf "$WORK"
            mkdir -p "$WORK"
            cp -r /tmp/cuh_safe_upload/refresh_assets "$WORK/refresh_assets"
            cp /tmp/cuh_safe_upload/safe_challenges_manifest.json "$WORK/safe_challenges_manifest.json"
            cp /tmp/cuh_safe_upload/apply_safe_challenges.py "$WORK/apply_safe_challenges.py"
            cp /tmp/cuh_safe_upload/challenge_description_overrides.py "$WORK/challenge_description_overrides.py"
            cp /tmp/cuh_safe_upload/apply_challenge_description_overrides.py "$WORK/apply_challenge_description_overrides.py"
            cp /tmp/cuh_safe_upload/challenge_hint_overrides.py "$WORK/challenge_hint_overrides.py"
            cp /tmp/cuh_safe_upload/apply_challenge_hint_overrides.py "$WORK/apply_challenge_hint_overrides.py"
            cp -r /tmp/cuh_safe_upload/plugins "$WORK/plugins"
            cp -r /tmp/cuh_safe_upload/templates "$WORK/templates"
            cp -r /tmp/cuh_safe_upload/bundles "$WORK/bundles"
            chmod +x "$WORK/refresh_assets/actualizar_paginas_ctfd.sh"
            docker exec {CONTAINER} mkdir -p /opt/CTFd/CTFd/plugins/first_blood_bonus
            docker exec {CONTAINER} mkdir -p /opt/CTFd/CTFd/plugins/solve_evidence_guard
            docker exec {CONTAINER} mkdir -p /opt/CTFd/CTFd/plugins/user_presence_board
            docker exec {CONTAINER} mkdir -p /opt/CTFd/CTFd/plugins/admin_notifications_console
            docker exec {CONTAINER} mkdir -p /opt/CTFd/CTFd/themes/admin/templates
            docker exec {CONTAINER} mkdir -p /opt/CTFd/CTFd/themes/core/templates/users
            docker cp "$WORK/plugins/first_blood_bonus/__init__.py" "{CONTAINER}:/opt/CTFd/CTFd/plugins/first_blood_bonus/__init__.py"
            docker cp "$WORK/plugins/solve_evidence_guard/__init__.py" "{CONTAINER}:/opt/CTFd/CTFd/plugins/solve_evidence_guard/__init__.py"
            docker cp "$WORK/plugins/user_presence_board/__init__.py" "{CONTAINER}:/opt/CTFd/CTFd/plugins/user_presence_board/__init__.py"
            docker cp "$WORK/plugins/admin_notifications_console/__init__.py" "{CONTAINER}:/opt/CTFd/CTFd/plugins/admin_notifications_console/__init__.py"
            docker cp "$WORK/templates/admin/notifications.html" "{CONTAINER}:/opt/CTFd/CTFd/themes/admin/templates/notifications.html"
            docker cp "$WORK/templates/admin/evidence_review.html" "{CONTAINER}:/opt/CTFd/CTFd/themes/admin/templates/evidence_review.html"
            docker cp "$WORK/templates/challenges.html" "{CONTAINER}:/opt/CTFd/CTFd/themes/core/templates/challenges.html"
            docker cp "$WORK/templates/notifications.html" "{CONTAINER}:/opt/CTFd/CTFd/themes/core/templates/notifications.html"
            docker cp "$WORK/templates/users/private.html" "{CONTAINER}:/opt/CTFd/CTFd/themes/core/templates/users/private.html"
            docker restart "{CONTAINER}" >/dev/null
            docker exec {CONTAINER} mkdir -p /tmp/cuh-bundles
            find "$WORK/bundles" -maxdepth 1 -type f -name '*.zip' -print0 | while IFS= read -r -d '' file; do
              docker cp "$file" "{CONTAINER}:/tmp/cuh-bundles/$(basename "$file")"
            done
            docker cp "$WORK/safe_challenges_manifest.json" "{CONTAINER}:/tmp/safe_challenges_manifest.json"
            docker cp "$WORK/apply_safe_challenges.py" "{CONTAINER}:/tmp/apply_safe_challenges.py"
            docker cp "$WORK/challenge_description_overrides.py" "{CONTAINER}:/tmp/challenge_description_overrides.py"
            docker cp "$WORK/apply_challenge_description_overrides.py" "{CONTAINER}:/tmp/apply_challenge_description_overrides.py"
            docker cp "$WORK/challenge_hint_overrides.py" "{CONTAINER}:/tmp/challenge_hint_overrides.py"
            docker cp "$WORK/apply_challenge_hint_overrides.py" "{CONTAINER}:/tmp/apply_challenge_hint_overrides.py"
            docker exec -e PYTHONPATH=/opt/CTFd "{CONTAINER}" python3 /tmp/apply_safe_challenges.py
            docker exec -e PYTHONPATH=/opt/CTFd "{CONTAINER}" python3 /tmp/apply_challenge_description_overrides.py
            docker exec -e PYTHONPATH=/opt/CTFd "{CONTAINER}" python3 /tmp/apply_challenge_hint_overrides.py
            cd "$WORK/refresh_assets"
            bash ./actualizar_paginas_ctfd.sh
            """
        ).strip() + "\n"
        write_tmp(upload_root / "remote_deploy.sh", remote_script)

        verify_python = textwrap.dedent(
            """
            from pathlib import Path
            import json
            from CTFd import create_app
            from CTFd.models import Challenges, Hints, ChallengeFiles, Pages
            manifest = json.loads(Path('/tmp/safe_challenges_manifest.json').read_text(encoding='utf-8'))
            app = create_app()
            with app.app_context():
                for spec in manifest['challenges']:
                    chal = Challenges.query.filter_by(name=spec['name']).first()
                    assert chal is not None, spec['name']
                    assert chal.category == spec['category']
                    assert chal.value == spec['value']
                    assert Hints.query.filter_by(challenge_id=chal.id).count() == 3
                    assert ChallengeFiles.query.filter_by(challenge_id=chal.id).count() >= 1
                    assert Pages.query.filter_by(route=spec['page_route']).first() is not None
                print('verified', len(manifest['challenges']))
            """
        ).strip() + "\n"
        write_tmp(upload_root / "verify_safe_challenges.py", verify_python)

        run(["ssh", "-i", str(KEY), "-o", "StrictHostKeyChecking=no", REMOTE, "rm -rf /tmp/cuh_safe_upload"])
        run(["scp", "-i", str(KEY), "-o", "StrictHostKeyChecking=no", "-r", str(upload_root), f"{REMOTE}:/tmp/"])
        run(["ssh", "-i", str(KEY), "-o", "StrictHostKeyChecking=no", REMOTE, "bash /tmp/cuh_safe_upload/remote_deploy.sh"])
        run(
            [
                "ssh",
                "-i",
                str(KEY),
                "-o",
                "StrictHostKeyChecking=no",
                REMOTE,
                f"docker cp /tmp/cuh_safe_upload/safe_challenges_manifest.json {CONTAINER}:/tmp/safe_challenges_manifest.json && docker cp /tmp/cuh_safe_upload/verify_safe_challenges.py {CONTAINER}:/tmp/verify_safe_challenges.py && docker exec -e PYTHONPATH=/opt/CTFd {CONTAINER} python3 /tmp/verify_safe_challenges.py",
            ]
        )


if __name__ == "__main__":
    main()
