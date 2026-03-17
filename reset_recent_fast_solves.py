import argparse
import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

from CTFd import create_app
from CTFd.models import Awards, Challenges, Solves, Tracking, Users, db


def recent_target_dates():
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    return {today.isoformat(), yesterday.isoformat()}


def first_seen_for_challenge(challenge_id: int):
    first_solve = (
        Solves.query.filter_by(challenge_id=challenge_id)
        .order_by(Solves.date.asc(), Solves.id.asc())
        .first()
    )
    first_open = (
        Tracking.query.filter_by(type="challenges.open", target=challenge_id)
        .order_by(Tracking.date.asc(), Tracking.id.asc())
        .first()
    )
    dates = [row.date for row in (first_solve, first_open) if row]
    return min(dates) if dates else None


def earliest_open(user_id: int, challenge_id: int):
    return (
        Tracking.query.filter_by(type="challenges.open", user_id=user_id, target=challenge_id)
        .order_by(Tracking.date.asc(), Tracking.id.asc())
        .first()
    )


def delete_private_evidence_files(app, assets):
    private_root = Path(app.config["UPLOAD_FOLDER"]) / "_private_evidence"
    for asset in assets:
        if not asset.stored_name:
            continue
        target = private_root / asset.stored_name
        try:
            if target.exists():
                target.unlink()
        except OSError:
            pass


def collect_recent_fast_solves(app):
    from CTFd.plugins.solve_evidence_guard import FAST_SOLVE_SECONDS
    from CTFd.plugins.solve_evidence_guard import SolveEvidenceAsset, SolveEvidenceRequirement

    target_days = recent_target_dates()
    recent_challenges = {}
    for challenge in Challenges.query.order_by(Challenges.id.asc()).all():
        first_seen = first_seen_for_challenge(challenge.id)
        if first_seen and first_seen.date().isoformat() in target_days:
            recent_challenges[challenge.id] = {
                "challenge": challenge,
                "first_seen": first_seen,
            }

    entries = []
    for challenge_id, meta in recent_challenges.items():
        challenge = meta["challenge"]
        if int(challenge.value or 0) <= 200:
            continue

        solves = (
            Solves.query.filter_by(challenge_id=challenge_id)
            .order_by(Solves.date.asc(), Solves.id.asc())
            .all()
        )
        for solve in solves:
            open_track = earliest_open(solve.user_id, challenge_id)
            if not open_track:
                continue
            elapsed = max(int((solve.date - open_track.date).total_seconds()), 0)
            if elapsed >= FAST_SOLVE_SECONDS:
                continue

            user = Users.query.filter_by(id=solve.user_id).first()
            requirements = SolveEvidenceRequirement.query.filter_by(solve_id=solve.id).all()
            assets = []
            for requirement in requirements:
                assets.extend(
                    SolveEvidenceAsset.query.filter_by(requirement_id=requirement.id).all()
                )

            award_name = f"Primer solve · {challenge.name}"
            awards = Awards.query.filter_by(user_id=solve.user_id, name=award_name).all()

            entries.append(
                {
                    "solve_id": solve.id,
                    "user_id": solve.user_id,
                    "user_name": user.name if user else f"user-{solve.user_id}",
                    "challenge_id": challenge.id,
                    "challenge_name": challenge.name,
                    "challenge_value": int(challenge.value or 0),
                    "challenge_first_seen": meta["first_seen"].isoformat(),
                    "solved_at": solve.date.isoformat(),
                    "opened_at": open_track.date.isoformat(),
                    "elapsed_seconds": elapsed,
                    "requirements": requirements,
                    "assets": assets,
                    "awards": awards,
                }
            )

    return entries


def summarize(entries):
    by_user = defaultdict(lambda: {"solves": 0, "points_removed": 0, "bonus_removed": 0})
    for entry in entries:
        bucket = by_user[entry["user_name"]]
        bucket["solves"] += 1
        bucket["points_removed"] += entry["challenge_value"]
        bucket["bonus_removed"] += sum(int(award.value or 0) for award in entry["awards"])
    return {
        "affected_solves": len(entries),
        "affected_users": len(by_user),
        "by_user": by_user,
    }


def apply_reset(app, entries):
    from CTFd.plugins.solve_evidence_guard import SolveEvidenceAsset, SolveEvidenceRequirement

    for entry in entries:
        delete_private_evidence_files(app, entry["assets"])

        for award in entry["awards"]:
            db.session.delete(award)

        for asset in entry["assets"]:
            db.session.delete(asset)

        for requirement in entry["requirements"]:
            db.session.delete(requirement)

        solve = Solves.query.filter_by(id=entry["solve_id"]).first()
        if solve:
            db.session.delete(solve)

    db.session.commit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Apply deletions instead of dry-run.")
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        entries = collect_recent_fast_solves(app)
        report = []
        for entry in entries:
            report.append(
                {
                    "user": entry["user_name"],
                    "challenge": entry["challenge_name"],
                    "value": entry["challenge_value"],
                    "elapsed_seconds": entry["elapsed_seconds"],
                    "bonus_removed": sum(int(award.value or 0) for award in entry["awards"]),
                    "solve_id": entry["solve_id"],
                }
            )

        summary = summarize(entries)
        printable = {
            "mode": "apply" if args.apply else "dry-run",
            "summary": {
                "affected_solves": summary["affected_solves"],
                "affected_users": summary["affected_users"],
                "by_user": {
                    user: values for user, values in sorted(summary["by_user"].items())
                },
            },
            "entries": report,
        }
        print(json.dumps(printable, ensure_ascii=False, indent=2))

        if args.apply:
            apply_reset(app, entries)


if __name__ == "__main__":
    main()
