from __future__ import annotations

from CTFd import create_app
from CTFd.models import Challenges, Hints, db

from challenge_hint_overrides import EXPECTED_CHALLENGE_COUNT, HINTS


def main() -> None:
    app = create_app()
    with app.app_context():
        missing = []
        updated = 0
        for name, hints in HINTS.items():
            challenge = Challenges.query.filter_by(name=name).first()
            if challenge is None:
                missing.append(name)
                continue
            Hints.query.filter_by(challenge_id=challenge.id).delete()
            db.session.flush()
            for hint in hints:
                db.session.add(
                    Hints(
                        challenge_id=challenge.id,
                        type="standard",
                        content=hint["content"],
                        cost=hint["cost"],
                        requirements=None,
                    )
                )
            updated += 1
        if missing:
            raise SystemExit(f"Challenges without DB row: {missing}")
        db.session.commit()
        print(f"hints updated {updated}")
        if updated != EXPECTED_CHALLENGE_COUNT:
            raise SystemExit(
                f"Expected {EXPECTED_CHALLENGE_COUNT} updated challenges, got {updated}"
            )


if __name__ == "__main__":
    main()
