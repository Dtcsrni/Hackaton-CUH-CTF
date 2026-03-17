from __future__ import annotations

from datetime import datetime, timezone

from CTFd.cache import clear_challenges, clear_standings
from CTFd.models import Awards, Challenges, Solves, db
from CTFd.plugins.challenges import BaseChallenge
from sqlalchemy import text

PLUGIN_KEY = "ctfcu_first_blood_bonus"
BONUS_CATEGORY = "Primer solve"
BONUS_MIN = 20
BONUS_MAX = 100
LOOPBACK_IPS = {"127.0.0.1", "::1", "localhost"}
MANUAL_SUBMISSION_PREFIX = "[admin-"


def award_name(challenge: Challenges) -> str:
    return f"{BONUS_CATEGORY} · {challenge.name}"


def award_description(challenge: Challenges, bonus: int) -> str:
    return (
        f"Primer solve de {challenge.name}. "
        f"Este bonus reconoce a la cuenta que abrió el marcador de la misión con {bonus} pts extra."
    )


def compute_bonus(base_value: int | None) -> int:
    base = max(int(base_value or 0), 0)
    scaled = int(round((base * 0.20) / 5.0) * 5)
    return max(BONUS_MIN, min(BONUS_MAX, scaled))


def get_existing_award(challenge: Challenges):
    return Awards.query.filter_by(category=BONUS_CATEGORY, name=award_name(challenge)).first()


def get_first_solve(challenge_id: int):
    return (
        Solves.query.filter_by(challenge_id=challenge_id)
        .order_by(Solves.date.asc(), Solves.id.asc())
        .first()
    )


def is_hidden_or_manual_award(challenge: Challenges, solve: Solves) -> bool:
    if challenge is None or solve is None or not solve.user_id:
        return True
    if getattr(challenge, "state", None) == "hidden":
        return True

    rows = db.session.execute(
        text(
            """
            SELECT ip, provided, date
            FROM submissions
            WHERE challenge_id = :challenge_id
              AND user_id = :user_id
              AND type = 'correct'
            ORDER BY date DESC, id DESC
            LIMIT 10
            """
        ),
        {"challenge_id": challenge.id, "user_id": solve.user_id},
    ).mappings().all()
    if not rows:
        return True

    solve_date = getattr(solve, "date", None)
    for row in rows:
        row_date = row.get("date")
        if solve_date and row_date and abs((solve_date - row_date).total_seconds()) > 30:
            continue
        ip_value = str(row.get("ip") or "").strip().lower()
        provided_value = str(row.get("provided") or "").strip().lower()
        if ip_value in LOOPBACK_IPS:
            return True
        if provided_value.startswith(MANUAL_SUBMISSION_PREFIX):
            return True
        return False

    latest = rows[0]
    latest_ip = str(latest.get("ip") or "").strip().lower()
    latest_provided = str(latest.get("provided") or "").strip().lower()
    return latest_ip in LOOPBACK_IPS or latest_provided.startswith(MANUAL_SUBMISSION_PREFIX)


def delete_award(award: Awards) -> bool:
    if award is None:
        return False
    db.session.delete(award)
    db.session.commit()
    return True


def create_first_blood_award(challenge: Challenges, solve: Solves, bonus_value: int | None = None):
    if get_existing_award(challenge):
        return None

    first = get_first_solve(challenge.id)
    if not first or first.id != solve.id:
        return None
    if is_hidden_or_manual_award(challenge, solve):
        return None

    bonus = compute_bonus(bonus_value if bonus_value is not None else challenge.value)
    award = Awards(
        user_id=solve.user_id,
        team_id=solve.team_id,
        type="standard",
        name=award_name(challenge),
        description=award_description(challenge, bonus),
        value=bonus,
        category=BONUS_CATEGORY,
        icon="bolt",
        requirements={
            "type": PLUGIN_KEY,
            "challenge_id": challenge.id,
            "challenge_name": challenge.name,
            "awarded_at": datetime.now(timezone.utc).isoformat(),
        },
    )
    db.session.add(award)
    db.session.commit()
    return award


def backfill_first_blood_awards():
    created = 0
    removed = 0
    for challenge in Challenges.query.order_by(Challenges.id.asc()).all():
        existing_award = get_existing_award(challenge)
        first = get_first_solve(challenge.id)
        if existing_award and (not first or is_hidden_or_manual_award(challenge, first)):
            if delete_award(existing_award):
                removed += 1
            continue
        if get_existing_award(challenge):
            continue
        if not first:
            continue
        if is_hidden_or_manual_award(challenge, first):
            continue
        if create_first_blood_award(challenge, first, bonus_value=challenge.value):
            created += 1
    if created or removed:
        clear_standings()
        clear_challenges()
    print(f"first blood awards backfilled {created} removed={removed}")


def patch_challenge_solve():
    if getattr(BaseChallenge, "__ctfcu_first_blood_patched__", False):
        return

    original_solve = BaseChallenge.solve.__func__

    @classmethod
    def wrapped_solve(cls, user, team, challenge, request):
        base_value = challenge.value
        original_solve(cls, user=user, team=team, challenge=challenge, request=request)
        solve = (
            Solves.query.filter_by(
                challenge_id=challenge.id,
                user_id=user.id if user else None,
                team_id=team.id if team else None,
            )
            .order_by(Solves.id.desc())
            .first()
        )
        if solve and create_first_blood_award(challenge, solve, bonus_value=base_value):
            clear_standings()
            clear_challenges()

    BaseChallenge.solve = wrapped_solve
    BaseChallenge.__ctfcu_first_blood_patched__ = True


def load(app):
    with app.app_context():
        patch_challenge_solve()
        backfill_first_blood_awards()
