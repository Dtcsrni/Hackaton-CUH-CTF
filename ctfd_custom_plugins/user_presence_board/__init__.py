from __future__ import annotations

from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request

from CTFd.models import Awards, Solves, Tracking, Users

ONLINE_WINDOW = timedelta(minutes=10)
RECENT_WINDOW = timedelta(hours=1)
TODAY_WINDOW = timedelta(hours=24)


def visible_users_query():
    return Users.query.filter_by(hidden=False, banned=False)


def last_seen_for_user(user_id: int):
    candidates = []

    latest_tracking = (
        Tracking.query.filter_by(user_id=user_id)
        .order_by(Tracking.date.desc(), Tracking.id.desc())
        .first()
    )
    if latest_tracking and latest_tracking.date:
        candidates.append(latest_tracking.date)

    latest_solve = (
        Solves.query.filter_by(user_id=user_id)
        .order_by(Solves.date.desc(), Solves.id.desc())
        .first()
    )
    if latest_solve and latest_solve.date:
        candidates.append(latest_solve.date)

    latest_award = (
        Awards.query.filter_by(user_id=user_id)
        .order_by(Awards.date.desc(), Awards.id.desc())
        .first()
    )
    if latest_award and latest_award.date:
        candidates.append(latest_award.date)

    return max(candidates) if candidates else None


def classify_presence(last_seen: datetime | None):
    if last_seen is None:
        return "unknown", "Sin actividad registrada"

    now = datetime.utcnow()
    age = now - last_seen

    if age <= ONLINE_WINDOW:
        return "online", "En línea ahora"
    if age <= RECENT_WINDOW:
        minutes = max(int(age.total_seconds() // 60), 1)
        return "recent", f"Activo hace {minutes} min"
    if age <= TODAY_WINDOW:
        hours = max(int(age.total_seconds() // 3600), 1)
        return "today", f"Activo hace {hours} h"
    days = max(int(age.total_seconds() // 86400), 1)
    return "away", f"Última actividad hace {days} día{'s' if days != 1 else ''}"


def build_blueprint():
    blueprint = Blueprint("ctfcu_user_presence_board", __name__)

    @blueprint.get("/api/users")
    def users_presence():
        ids_param = request.args.get("ids", "").strip()
        ids: list[int] = []
        if ids_param:
            for raw in ids_param.split(","):
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    ids.append(int(raw))
                except ValueError:
                    continue

        query = visible_users_query()
        if ids:
            query = query.filter(Users.id.in_(ids))

        payload = []
        for user in query.order_by(Users.id.asc()).all():
            last_seen = last_seen_for_user(user.id)
            status, label = classify_presence(last_seen)
            payload.append(
                {
                    "user_id": user.id,
                    "status": status,
                    "label": label,
                    "last_seen": last_seen.isoformat() if last_seen else None,
                }
            )

        counts = {
            "online": sum(1 for item in payload if item["status"] == "online"),
            "recent": sum(1 for item in payload if item["status"] in {"online", "recent"}),
            "today": sum(1 for item in payload if item["status"] in {"online", "recent", "today"}),
        }
        return jsonify({"success": True, "data": {"users": payload, "counts": counts}})

    return blueprint


def load(app):
    app.register_blueprint(build_blueprint(), url_prefix="/plugins/user_presence_board")
