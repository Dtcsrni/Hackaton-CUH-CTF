from __future__ import annotations

from datetime import datetime

from flask import Blueprint, current_app, jsonify, request
from sqlalchemy import inspect, text

from CTFd.api.v1.challenges import ChallengeAttempt
from CTFd.models import Notifications, Users, db
from CTFd.plugins import bypass_csrf_protection
from CTFd.utils.decorators import admins_only
from CTFd.utils.user import authed, get_current_user, is_admin

DEFAULT_ACK_LABEL = "Acepto"
ALLOWED_ACCENTS = {"default", "red", "warning", "info", "success"}


class NotificationAcknowledgement(db.Model):
    __tablename__ = "ctfcu_notification_acknowledgements"

    id = db.Column(db.Integer, primary_key=True)
    notification_id = db.Column(
        db.Integer,
        db.ForeignKey("notifications.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    requires_ack = db.Column(db.Boolean, nullable=False, default=False)
    block_challenges = db.Column(db.Boolean, nullable=False, default=False)
    accent = db.Column(db.String(24), nullable=False, default="default")
    ack_label = db.Column(db.String(48), nullable=False, default=DEFAULT_ACK_LABEL)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    accepted_at = db.Column(db.DateTime, nullable=True)

    notification = db.relationship("Notifications", lazy="select")
    user = db.relationship("Users", lazy="select")


def parse_bool(value, *, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() not in {"", "0", "false", "off", "no"}


def normalize_accent(value: str | None) -> str:
    accent = (value or "default").strip().lower()
    if accent not in ALLOWED_ACCENTS:
        return "default"
    return accent


def ensure_schema():
    inspector = inspect(db.engine)
    if NotificationAcknowledgement.__tablename__ not in inspector.get_table_names():
        db.create_all()
        inspector = inspect(db.engine)

    columns = {item["name"] for item in inspector.get_columns(NotificationAcknowledgement.__tablename__)}
    missing_sql = {
        "requires_ack": "ALTER TABLE ctfcu_notification_acknowledgements ADD COLUMN requires_ack BOOLEAN NOT NULL DEFAULT 0",
        "block_challenges": "ALTER TABLE ctfcu_notification_acknowledgements ADD COLUMN block_challenges BOOLEAN NOT NULL DEFAULT 0",
        "accent": "ALTER TABLE ctfcu_notification_acknowledgements ADD COLUMN accent VARCHAR(24) NOT NULL DEFAULT 'default'",
        "ack_label": f"ALTER TABLE ctfcu_notification_acknowledgements ADD COLUMN ack_label VARCHAR(48) NOT NULL DEFAULT '{DEFAULT_ACK_LABEL}'",
        "created_at": "ALTER TABLE ctfcu_notification_acknowledgements ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
        "accepted_at": "ALTER TABLE ctfcu_notification_acknowledgements ADD COLUMN accepted_at DATETIME NULL",
    }
    changed = False
    for column, sql in missing_sql.items():
        if column not in columns:
            db.session.execute(text(sql))
            changed = True
    if changed:
        db.session.commit()


def serialize_acknowledgement(item: NotificationAcknowledgement) -> dict:
    notification = item.notification
    return {
        "notification_id": item.notification_id,
        "title": notification.title if notification else "Notificación",
        "content": notification.content if notification else "",
        "date": notification.date.isoformat() if notification and notification.date else None,
        "accent": item.accent,
        "requires_ack": bool(item.requires_ack),
        "block_challenges": bool(item.block_challenges),
        "ack_label": item.ack_label or DEFAULT_ACK_LABEL,
        "accepted_at": item.accepted_at.isoformat() if item.accepted_at else None,
    }


def get_pending_acknowledgement(user_id: int, *, blocking_only: bool = False):
    query = NotificationAcknowledgement.query.filter_by(user_id=user_id, requires_ack=True, accepted_at=None)
    if blocking_only:
        query = query.filter_by(block_challenges=True)
    return query.order_by(NotificationAcknowledgement.created_at.asc(), NotificationAcknowledgement.id.asc()).first()


def patch_attempt_post():
    if getattr(ChallengeAttempt, "__ctfcu_notification_ack_patched__", False):
        return
    original_post = ChallengeAttempt.post

    def wrapped_post(self, *args, **kwargs):
        if authed() is False:
            return original_post(self, *args, **kwargs)
        user = get_current_user()
        if user is None or is_admin():
            return original_post(self, *args, **kwargs)

        pending = get_pending_acknowledgement(user.id, blocking_only=True)
        if pending:
            notification = pending.notification
            title = notification.title if notification else "Notificación pendiente"
            message = (
                f"Debes revisar y aceptar la notificación '{title}' desde /notifications "
                "antes de poder enviar nuevas flags."
            )
            return ({
                "success": True,
                "data": {
                    "status": "notification_ack_required",
                    "message": message,
                    "notification": serialize_acknowledgement(pending),
                },
            }, 403)

        return original_post(self, *args, **kwargs)

    ChallengeAttempt.post = wrapped_post
    ChallengeAttempt.__ctfcu_notification_ack_patched__ = True


def build_blueprint():
    blueprint = Blueprint("ctfcu_admin_notifications_console", __name__)

    @blueprint.get("/api/users")
    @admins_only
    def notification_users():
        users = (
            Users.query.filter_by(hidden=False, banned=False)
            .order_by(Users.name.asc())
            .all()
        )
        payload = [
            {
                "id": user.id,
                "name": user.name,
                "affiliation": user.affiliation or "",
            }
            for user in users
        ]
        return jsonify({"success": True, "data": payload})

    @blueprint.get("/api/pending-ack")
    def pending_ack():
        if authed() is False:
            return jsonify({"success": False, "message": "authentication required"}), 403
        user = get_current_user()
        if user is None:
            return jsonify({"success": False, "message": "authentication required"}), 403
        pending = get_pending_acknowledgement(user.id)
        return jsonify({
            "success": True,
            "data": {
                "pending": pending is not None,
                "notification": serialize_acknowledgement(pending) if pending else None,
            },
        })

    @blueprint.post("/api/acknowledge/<int:notification_id>")
    @bypass_csrf_protection
    def acknowledge_notification(notification_id: int):
        if authed() is False:
            return jsonify({"success": False, "message": "authentication required"}), 403
        user = get_current_user()
        if user is None:
            return jsonify({"success": False, "message": "authentication required"}), 403

        item = NotificationAcknowledgement.query.filter_by(
            notification_id=notification_id,
            user_id=user.id,
            requires_ack=True,
        ).first()
        if item is None:
            return jsonify({"success": False, "message": "La notificación ya no requiere confirmación."}), 404

        if item.accepted_at is None:
            item.accepted_at = datetime.utcnow()
            db.session.add(item)
            db.session.commit()

        return jsonify({"success": True, "data": serialize_acknowledgement(item)})

    @blueprint.post("/api/send")
    @admins_only
    def send_notification():
        data = request.get_json(silent=True) or request.form.to_dict()

        title = (data.get("title") or "").strip()
        content = (data.get("content") or "").strip()
        target_mode = (data.get("target_mode") or "broadcast").strip()
        notif_type = (data.get("type") or "alert").strip()
        notif_sound = parse_bool(data.get("sound", True), default=True)
        requires_ack = parse_bool(data.get("requires_ack"), default=False)
        block_challenges = parse_bool(data.get("block_challenges"), default=requires_ack)
        ack_label = (data.get("ack_label") or DEFAULT_ACK_LABEL).strip() or DEFAULT_ACK_LABEL
        accent = normalize_accent(data.get("accent"))

        if len(title) < 3:
            return jsonify({"success": False, "message": "El título debe tener al menos 3 caracteres."}), 400
        if len(content) < 8:
            return jsonify({"success": False, "message": "El contenido debe tener al menos 8 caracteres."}), 400
        if target_mode not in {"broadcast", "user"}:
            return jsonify({"success": False, "message": "Destino inválido."}), 400
        if requires_ack and target_mode != "user":
            return jsonify({"success": False, "message": "Las notificaciones con Acepto solo pueden enviarse a un participante específico."}), 400

        notification = Notifications(title=title, content=content)
        target_label = "General"
        user = None

        if target_mode == "user":
            try:
                user_id = int(data.get("user_id"))
            except (TypeError, ValueError):
                return jsonify({"success": False, "message": "Selecciona un participante válido."}), 400

            user = Users.query.filter_by(id=user_id, hidden=False, banned=False).first()
            if user is None:
                return jsonify({"success": False, "message": "El participante ya no está disponible."}), 404

            notification.user_id = user.id
            target_label = user.name

        db.session.add(notification)
        db.session.flush()

        ack_item = None
        if requires_ack and user is not None:
            ack_item = NotificationAcknowledgement(
                notification_id=notification.id,
                user_id=user.id,
                requires_ack=True,
                block_challenges=block_challenges,
                accent=accent,
                ack_label=ack_label,
            )
            db.session.add(ack_item)

        db.session.commit()

        response_data = {
            "id": notification.id,
            "title": notification.title,
            "content": notification.content,
            "html": notification.content,
            "date": notification.date.isoformat() if notification.date else None,
            "user_id": notification.user_id,
            "team_id": notification.team_id,
            "target_label": target_label,
            "type": notif_type,
            "sound": notif_sound,
            "requires_ack": requires_ack,
            "block_challenges": block_challenges if requires_ack else False,
            "accent": ack_item.accent if ack_item else accent,
            "ack_label": ack_item.ack_label if ack_item else ack_label,
        }

        current_app.events_manager.publish(data=response_data, type="notification")
        return jsonify({"success": True, "data": response_data})

    @blueprint.post("/api/clear-all")
    @admins_only
    def clear_all_notifications():
        deleted = Notifications.query.count()
        NotificationAcknowledgement.query.delete()
        Notifications.query.delete()
        db.session.commit()
        return jsonify({"success": True, "data": {"deleted": deleted}})

    return blueprint


def load(app):
    with app.app_context():
        ensure_schema()
        patch_attempt_post()
    app.register_blueprint(build_blueprint(), url_prefix="/plugins/admin_notifications_console")
