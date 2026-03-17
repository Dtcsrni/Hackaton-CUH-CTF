from __future__ import annotations

import hashlib
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from flask import Blueprint, abort, jsonify, render_template, request, send_file, url_for
from sqlalchemy import inspect, text
from werkzeug.utils import secure_filename

from CTFd.api.v1.challenges import ChallengeAttempt, ChallengeSolution
from CTFd.cache import cache
from CTFd.models import Challenges, Solves, Teams, Tracking, Users, db
from CTFd.plugins.challenges import BaseChallenge
from CTFd.utils import get_app_config
from CTFd.utils.decorators import admins_only
from CTFd.utils.user import authed, get_current_user, is_admin

HIGH_VALUE_THRESHOLD = 300
MIN_EVIDENCE_FILES = 4
MAX_EVIDENCE_FILES = 8
MAX_FILE_BYTES = 12 * 1024 * 1024
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".pdf", ".txt", ".log", ".md"}
REVIEW_STATES = {"unreviewed", "reviewed", "needs_follow_up", "rejected"}
SOLUTION_REQUEST_WINDOW_SECONDS = 60
SOLUTION_MAX_REQUESTS = 3


class SolveEvidenceRequirement(db.Model):
    __tablename__ = "ctfcu_solve_evidence_requirements"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id", ondelete="SET NULL"), nullable=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False, index=True)
    solve_id = db.Column(db.Integer, db.ForeignKey("solves.id", ondelete="CASCADE"), nullable=False, unique=True)
    minimum_files = db.Column(db.Integer, nullable=False, default=MIN_EVIDENCE_FILES)
    status = db.Column(db.String(32), nullable=False, default="pending", index=True)
    reason = db.Column(db.String(32), nullable=False)
    opened_at = db.Column(db.DateTime, nullable=True)
    solved_at = db.Column(db.DateTime, nullable=False)
    elapsed_seconds = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)
    review_status = db.Column(db.String(32), nullable=False, default="unreviewed", index=True)
    review_notes = db.Column(db.Text, nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    reviewed_by_id = db.Column(db.Integer, nullable=True, index=True)

    user = db.relationship("Users", foreign_keys="SolveEvidenceRequirement.user_id", lazy="select")
    team = db.relationship("Teams", foreign_keys="SolveEvidenceRequirement.team_id", lazy="select")
    challenge = db.relationship("Challenges", foreign_keys="SolveEvidenceRequirement.challenge_id", lazy="select")
    solve = db.relationship("Solves", foreign_keys="SolveEvidenceRequirement.solve_id", lazy="select")
    evidences = db.relationship(
        "SolveEvidenceAsset",
        back_populates="requirement",
        cascade="all, delete-orphan",
        lazy="select",
    )

    @property
    def uploaded_files(self) -> int:
        return len(self.evidences or [])

    @property
    def remaining_files(self) -> int:
        return max(int(self.minimum_files or 0) - self.uploaded_files, 0)


class SolveEvidenceAsset(db.Model):
    __tablename__ = "ctfcu_solve_evidence_assets"

    id = db.Column(db.Integer, primary_key=True)
    requirement_id = db.Column(
        db.Integer,
        db.ForeignKey("ctfcu_solve_evidence_requirements.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    original_name = db.Column(db.String(255), nullable=False)
    stored_name = db.Column(db.String(255), nullable=False, unique=True)
    sha1sum = db.Column(db.String(40), nullable=False)
    mime_type = db.Column(db.String(120), nullable=True)
    size_bytes = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    requirement = db.relationship("SolveEvidenceRequirement", back_populates="evidences", lazy="select")


def ensure_schema():
    inspector = inspect(db.engine)
    if SolveEvidenceRequirement.__tablename__ not in inspector.get_table_names():
        db.create_all()
        inspector = inspect(db.engine)

    columns = {item["name"] for item in inspector.get_columns(SolveEvidenceRequirement.__tablename__)}
    missing_sql = {
        "review_status": "ALTER TABLE ctfcu_solve_evidence_requirements ADD COLUMN review_status VARCHAR(32) NOT NULL DEFAULT 'unreviewed'",
        "review_notes": "ALTER TABLE ctfcu_solve_evidence_requirements ADD COLUMN review_notes TEXT",
        "reviewed_at": "ALTER TABLE ctfcu_solve_evidence_requirements ADD COLUMN reviewed_at DATETIME",
        "reviewed_by_id": "ALTER TABLE ctfcu_solve_evidence_requirements ADD COLUMN reviewed_by_id INTEGER",
    }
    changed = False
    for column, sql in missing_sql.items():
        if column not in columns:
            db.session.execute(text(sql))
            changed = True
    if changed:
        db.session.commit()


def private_evidence_root() -> Path:
    upload_root = Path(get_app_config("UPLOAD_FOLDER") or "/var/uploads")
    root = upload_root / "_private_evidence"
    root.mkdir(parents=True, exist_ok=True)
    return root


def sha1_file_storage(file_storage) -> tuple[str, int]:
    stream = file_storage.stream
    stream.seek(0)
    digest = hashlib.sha1()  # nosec - integrity and dedup only
    size = 0
    while True:
        chunk = stream.read(1024 * 1024)
        if not chunk:
            break
        digest.update(chunk)
        size += len(chunk)
    stream.seek(0)
    return digest.hexdigest(), size


def allowed_extension(filename: str) -> str:
    suffix = Path(filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError("Formato no permitido. Usa PNG, JPG, WEBP, PDF o archivos de texto/log.")
    return suffix


def ensure_authenticated_user():
    if authed() is False:
        return None
    return get_current_user()


def earliest_open(user_id: int, challenge_id: int):
    if not user_id:
        return None
    return (
        Tracking.query.filter_by(type="challenges.open", user_id=user_id, target=challenge_id)
        .order_by(Tracking.date.asc(), Tracking.id.asc())
        .first()
    )


def get_latest_solve(user_id: int | None, challenge_id: int):
    if not user_id:
        return None
    return (
        Solves.query.filter_by(user_id=user_id, challenge_id=challenge_id)
        .order_by(Solves.date.desc(), Solves.id.desc())
        .first()
    )


def existing_requirement_for_solve(solve_id: int):
    return SolveEvidenceRequirement.query.filter_by(solve_id=solve_id).first()


def user_has_solved_challenge(user_id: int | None, challenge_id: int) -> bool:
    if not user_id:
        return False
    return Solves.query.filter_by(user_id=user_id, challenge_id=challenge_id).first() is not None


def challenge_elapsed_seconds(solve: Solves, challenge: Challenges) -> tuple[datetime | None, int]:
    open_track = earliest_open(solve.user_id, challenge.id)
    opened_at = open_track.date if open_track else None
    if opened_at is None:
        return None, 0
    return opened_at, max(int((solve.date - opened_at).total_seconds()), 0)


def should_require_evidence(challenge: Challenges) -> tuple[bool, str]:
    if int(challenge.value or 0) > HIGH_VALUE_THRESHOLD:
        return True, "value-threshold"
    return False, "below-threshold"


def create_requirement_for_solve(solve: Solves, challenge: Challenges, *, commit: bool = False):
    if not solve or not solve.user_id or existing_requirement_for_solve(solve.id):
        return None
    should_require, reason = should_require_evidence(challenge)
    if not should_require:
        return None
    opened_at, elapsed_seconds = challenge_elapsed_seconds(solve, challenge)
    requirement = SolveEvidenceRequirement(
        user_id=solve.user_id,
        team_id=solve.team_id,
        challenge_id=challenge.id,
        solve_id=solve.id,
        minimum_files=MIN_EVIDENCE_FILES,
        status="pending",
        reason=reason,
        opened_at=opened_at,
        solved_at=solve.date,
        elapsed_seconds=elapsed_seconds,
    )
    db.session.add(requirement)
    if commit:
        db.session.commit()
    return requirement


def delete_requirement_storage(requirement: SolveEvidenceRequirement):
    target_dir = private_evidence_root() / f"user-{requirement.user_id}" / f"req-{requirement.id}"
    if not target_dir.exists():
        return
    for item in sorted(target_dir.rglob("*"), reverse=True):
        if item.is_file():
            item.unlink(missing_ok=True)
        elif item.is_dir():
            item.rmdir()
    target_dir.rmdir()


def reconcile_requirements():
    valid_solves = (
        Solves.query.join(Challenges, Challenges.id == Solves.challenge_id)
        .filter(Challenges.value > HIGH_VALUE_THRESHOLD)
        .order_by(Solves.date.asc(), Solves.id.asc())
        .all()
    )
    valid_ids = {solve.id for solve in valid_solves}
    created = 0
    updated = 0
    removed = 0
    existing = {item.solve_id: item for item in SolveEvidenceRequirement.query.all()}

    for solve in valid_solves:
        challenge = Challenges.query.filter_by(id=solve.challenge_id).first()
        if challenge is None:
            continue
        requirement = existing.get(solve.id)
        if requirement is None:
            create_requirement_for_solve(solve, challenge, commit=False)
            created += 1
            continue
        opened_at, elapsed_seconds = challenge_elapsed_seconds(solve, challenge)
        desired_status = "fulfilled" if requirement.uploaded_files >= MIN_EVIDENCE_FILES else "pending"
        changed = False
        if requirement.minimum_files != MIN_EVIDENCE_FILES:
            requirement.minimum_files = MIN_EVIDENCE_FILES
            changed = True
        if requirement.reason != "value-threshold":
            requirement.reason = "value-threshold"
            changed = True
        if requirement.status != desired_status:
            requirement.status = desired_status
            requirement.resolved_at = datetime.utcnow() if desired_status == "fulfilled" else None
            changed = True
        if requirement.opened_at != opened_at:
            requirement.opened_at = opened_at
            changed = True
        if requirement.elapsed_seconds != elapsed_seconds:
            requirement.elapsed_seconds = elapsed_seconds
            changed = True
        if requirement.review_status not in REVIEW_STATES:
            requirement.review_status = "unreviewed"
            changed = True
        if changed:
            db.session.add(requirement)
            updated += 1

    for requirement in SolveEvidenceRequirement.query.all():
        if requirement.solve_id in valid_ids:
            continue
        delete_requirement_storage(requirement)
        db.session.delete(requirement)
        removed += 1

    db.session.commit()
    print(f"solve evidence requirements reconciled created={created} updated={updated} removed={removed}")


def get_pending_requirement(user_id: int):
    return (
        SolveEvidenceRequirement.query.filter_by(user_id=user_id, status="pending")
        .order_by(SolveEvidenceRequirement.created_at.asc(), SolveEvidenceRequirement.id.asc())
        .first()
    )


def reason_label(reason: str) -> str:
    if reason == "value-threshold":
        return f"Reto de más de {HIGH_VALUE_THRESHOLD} puntos"
    return "Revisión documental requerida"


def review_label(state: str) -> str:
    labels = {
        "unreviewed": "Sin revisar",
        "reviewed": "Revisado",
        "needs_follow_up": "Requiere seguimiento",
        "rejected": "Rechazado",
    }
    return labels.get(state, state)


def file_size_label(size_bytes: int) -> str:
    value = int(size_bytes or 0)
    if value >= 1024 * 1024:
        return f"{value / (1024 * 1024):.1f} MB"
    if value >= 1024:
        return f"{round(value / 1024)} KB"
    return f"{value} B"


def serialize_requirement(requirement: SolveEvidenceRequirement, *, admin: bool = False) -> dict:
    reviewed_by = Users.query.filter_by(id=requirement.reviewed_by_id).first() if requirement.reviewed_by_id else None
    files = sorted(requirement.evidences, key=lambda item: (item.created_at, item.id))
    payload = {
        "id": requirement.id,
        "user_id": requirement.user_id,
        "user_name": requirement.user.name if requirement.user else "Participante",
        "team_name": requirement.team.name if requirement.team else None,
        "challenge_id": requirement.challenge_id,
        "challenge_name": requirement.challenge.name if requirement.challenge else "Desafío",
        "challenge_value": int(requirement.challenge.value or 0) if requirement.challenge else 0,
        "minimum_files": requirement.minimum_files,
        "uploaded_files": len(files),
        "remaining_files": requirement.remaining_files,
        "status": requirement.status,
        "reason": requirement.reason,
        "reason_label": reason_label(requirement.reason),
        "opened_at": requirement.opened_at.isoformat() if requirement.opened_at else None,
        "solved_at": requirement.solved_at.isoformat() if requirement.solved_at else None,
        "elapsed_seconds": requirement.elapsed_seconds,
        "created_at": requirement.created_at.isoformat() if requirement.created_at else None,
        "resolved_at": requirement.resolved_at.isoformat() if requirement.resolved_at else None,
        "review_status": requirement.review_status,
        "review_label": review_label(requirement.review_status),
        "review_notes": requirement.review_notes or "",
        "reviewed_at": requirement.reviewed_at.isoformat() if requirement.reviewed_at else None,
        "reviewed_by_name": reviewed_by.name if reviewed_by else None,
        "files": [
            {
                "id": item.id,
                "original_name": item.original_name,
                "size_bytes": item.size_bytes,
                "size_label": file_size_label(item.size_bytes),
                "mime_type": item.mime_type,
                "created_at": item.created_at.isoformat(),
                "sha1_prefix": item.sha1sum[:12],
            }
            for item in files
        ],
    }
    if admin:
        for item in payload["files"]:
            item["download_url"] = url_for("ctfcu_solve_evidence_guard_admin.admin_requirement_asset", asset_id=item["id"])
    return payload


def save_evidence_file(requirement: SolveEvidenceRequirement, file_storage) -> SolveEvidenceAsset:
    original_name = secure_filename(file_storage.filename or "")
    if not original_name:
        raise ValueError("Cada evidencia necesita un nombre de archivo válido.")
    extension = allowed_extension(original_name)
    sha1sum, size_bytes = sha1_file_storage(file_storage)
    if size_bytes <= 0:
        raise ValueError("No se aceptan evidencias vacías.")
    if size_bytes > MAX_FILE_BYTES:
        raise ValueError("Cada evidencia debe pesar 12 MB o menos.")
    duplicate = SolveEvidenceAsset.query.filter_by(requirement_id=requirement.id, sha1sum=sha1sum).first()
    if duplicate:
        raise ValueError(f"La evidencia {original_name} ya fue subida anteriormente.")

    target_dir = private_evidence_root() / f"user-{requirement.user_id}" / f"req-{requirement.id}"
    target_dir.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid4().hex}{extension}"
    file_storage.save(target_dir / stored_name)
    asset = SolveEvidenceAsset(
        requirement_id=requirement.id,
        original_name=original_name,
        stored_name=str(Path(f"user-{requirement.user_id}") / f"req-{requirement.id}" / stored_name),
        sha1sum=sha1sum,
        mime_type=file_storage.mimetype,
        size_bytes=size_bytes,
    )
    db.session.add(asset)
    db.session.flush()
    return asset


def satisfy_requirement_if_ready(requirement: SolveEvidenceRequirement):
    if requirement.uploaded_files >= int(requirement.minimum_files or MIN_EVIDENCE_FILES):
        requirement.status = "fulfilled"
        requirement.resolved_at = requirement.resolved_at or datetime.utcnow()
    else:
        requirement.status = "pending"
        requirement.resolved_at = None
    db.session.add(requirement)
    return requirement


def patch_challenge_solve():
    if getattr(BaseChallenge, "__ctfcu_solve_evidence_patched__", False):
        return
    original_solve = BaseChallenge.solve.__func__

    @classmethod
    def wrapped_solve(cls, user, team, challenge, request):
        original_solve(cls, user=user, team=team, challenge=challenge, request=request)
        solve = get_latest_solve(user.id if user else None, challenge.id)
        if solve:
            create_requirement_for_solve(solve=solve, challenge=challenge, commit=True)

    BaseChallenge.solve = wrapped_solve
    BaseChallenge.__ctfcu_solve_evidence_patched__ = True


def patch_attempt_post():
    if getattr(ChallengeAttempt, "__ctfcu_solve_evidence_attempt_patched__", False):
        return
    original_post = ChallengeAttempt.post

    def wrapped_post(self, *args, **kwargs):
        if authed() is False:
            return original_post(self, *args, **kwargs)
        user = get_current_user()
        if user is None or is_admin():
            return original_post(self, *args, **kwargs)
        pending = get_pending_requirement(user.id)
        if pending:
            challenge = Challenges.query.filter_by(id=pending.challenge_id).first()
            message = (
                f"Antes de enviar flags nuevas debes cargar al menos {pending.minimum_files} evidencias "
                f"para {challenge.name if challenge else 'el reto pendiente'} en /user. "
                f"Llevas {pending.uploaded_files}/{pending.minimum_files}."
            )
            return ({
                "success": True,
                "data": {
                    "status": "evidence_required",
                    "message": message,
                    "requirement_id": pending.id,
                    "uploaded_files": pending.uploaded_files,
                    "minimum_files": pending.minimum_files,
                    "challenge_id": pending.challenge_id,
                    "challenge_name": challenge.name if challenge else None,
                },
            }, 403)
        return original_post(self, *args, **kwargs)

    ChallengeAttempt.post = wrapped_post
    ChallengeAttempt.__ctfcu_solve_evidence_attempt_patched__ = True


def patch_solution_get():
    if getattr(ChallengeSolution, "__ctfcu_solution_guard_patched__", False):
        return
    original_get = ChallengeSolution.get

    def wrapped_get(self, challenge_id, *args, **kwargs):
        if authed() is False:
            return original_get(self, challenge_id, *args, **kwargs)

        user = get_current_user()
        if user is None or is_admin():
            return original_get(self, challenge_id, *args, **kwargs)

        try:
            normalized_challenge_id = int(challenge_id)
        except (TypeError, ValueError):
            abort(404)

        rate_key = f"ctfcu_solution_guard:{user.id}:{normalized_challenge_id}"
        recent_requests = int(cache.get(rate_key) or 0)
        if recent_requests >= SOLUTION_MAX_REQUESTS:
            return jsonify({
                "success": False,
                "message": (
                    "Demasiadas consultas de solución para el mismo reto. "
                    "Espera un momento antes de volver a intentarlo."
                ),
            }), 429
        cache.inc(rate_key)
        cache.expire(rate_key, SOLUTION_REQUEST_WINDOW_SECONDS)

        challenge = Challenges.query.filter_by(id=normalized_challenge_id).first()
        if challenge is None or challenge.state == "hidden":
            abort(404)

        # Avoid using this endpoint as an oracle for unsolved challenges.
        if not user_has_solved_challenge(user.id, normalized_challenge_id):
            abort(404)

        return original_get(self, normalized_challenge_id, *args, **kwargs)

    ChallengeSolution.get = wrapped_get
    ChallengeSolution.__ctfcu_solution_guard_patched__ = True


def build_admin_payload():
    participants: dict[int, dict] = {}
    requirements = (
        SolveEvidenceRequirement.query.order_by(
            SolveEvidenceRequirement.solved_at.desc(),
            SolveEvidenceRequirement.id.desc(),
        ).all()
    )
    for requirement in requirements:
        key = requirement.user_id
        user_name = requirement.user.name if requirement.user else f"Usuario {requirement.user_id}"
        if key not in participants:
            participants[key] = {
                "user_id": requirement.user_id,
                "user_name": user_name,
                "team_name": requirement.team.name if requirement.team else None,
                "pending_count": 0,
                "fulfilled_count": 0,
                "unreviewed_count": 0,
                "requirements": [],
            }
        participants[key]["requirements"].append(serialize_requirement(requirement, admin=True))
        if requirement.status == "pending":
            participants[key]["pending_count"] += 1
        if requirement.status == "fulfilled":
            participants[key]["fulfilled_count"] += 1
        if requirement.review_status == "unreviewed":
            participants[key]["unreviewed_count"] += 1
    return sorted(participants.values(), key=lambda item: item["user_name"].lower())


def build_user_blueprint() -> Blueprint:
    blueprint = Blueprint("ctfcu_solve_evidence_guard", __name__)

    @blueprint.get("/api/status")
    def evidence_status():
        user = ensure_authenticated_user()
        if user is None:
            return jsonify({"success": False, "message": "authentication required"}), 403
        requirements = (
            SolveEvidenceRequirement.query.filter_by(user_id=user.id)
            .order_by(SolveEvidenceRequirement.created_at.desc(), SolveEvidenceRequirement.id.desc())
            .all()
        )
        return jsonify({
            "success": True,
            "data": {
                "blocked": any(item.status == "pending" for item in requirements),
                "threshold": HIGH_VALUE_THRESHOLD,
                "minimum_files": MIN_EVIDENCE_FILES,
                "pending_requirements": [serialize_requirement(item) for item in requirements if item.status == "pending"],
                "recently_fulfilled": [serialize_requirement(item) for item in requirements if item.status == "fulfilled"][:3],
            },
        })

    @blueprint.post("/api/requirements/<int:requirement_id>/upload")
    def upload_requirement_evidence(requirement_id: int):
        user = ensure_authenticated_user()
        if user is None:
            return jsonify({"success": False, "message": "authentication required"}), 403
        requirement = SolveEvidenceRequirement.query.filter_by(id=requirement_id, user_id=user.id).first()
        if requirement is None:
            return jsonify({"success": False, "message": "Requisito de evidencia no encontrado."}), 404

        files = request.files.getlist("evidence")
        if not files:
            return jsonify({"success": False, "message": "Debes adjuntar al menos un archivo."}), 400
        existing = requirement.uploaded_files
        if existing >= MAX_EVIDENCE_FILES:
            return jsonify({"success": False, "message": "Ya alcanzaste el máximo de evidencias para este requisito."}), 400
        if existing + len(files) > MAX_EVIDENCE_FILES:
            return jsonify({"success": False, "message": f"Puedes tener como máximo {MAX_EVIDENCE_FILES} evidencias por requisito."}), 400

        saved = []
        errors = []
        seen_sha1 = {item.sha1sum for item in requirement.evidences}
        for file_storage in files:
            try:
                original_name = secure_filename(file_storage.filename or "")
                if not original_name:
                    raise ValueError("Hay un archivo sin nombre válido.")
                allowed_extension(original_name)
                sha1sum, size_bytes = sha1_file_storage(file_storage)
                if sha1sum in seen_sha1:
                    raise ValueError(f"{original_name} repite una evidencia ya cargada.")
                if size_bytes <= 0:
                    raise ValueError(f"{original_name} está vacío.")
                if size_bytes > MAX_FILE_BYTES:
                    raise ValueError(f"{original_name} supera el límite de 12 MB.")
                seen_sha1.add(sha1sum)
                asset = save_evidence_file(requirement, file_storage)
                saved.append(asset.original_name)
            except ValueError as error:
                errors.append(str(error))

        satisfy_requirement_if_ready(requirement)
        db.session.commit()
        payload = {"requirement": serialize_requirement(requirement), "saved": saved, "errors": errors}
        if not saved:
            return jsonify({"success": False, "message": "No se pudo guardar ninguna evidencia.", "data": payload}), 400
        message = "Evidencias guardadas."
        if requirement.status == "fulfilled":
            message = "Evidencias guardadas. Ya puedes volver a enviar flags."
        return jsonify({"success": True, "message": message, "data": payload})

    return blueprint


def build_admin_blueprint() -> Blueprint:
    blueprint = Blueprint("ctfcu_solve_evidence_guard_admin", __name__)

    @blueprint.get("/admin/evidence-review")
    @admins_only
    def admin_evidence_review():
        return render_template("admin/evidence_review.html", threshold=HIGH_VALUE_THRESHOLD, minimum_files=MIN_EVIDENCE_FILES)

    @blueprint.get("/admin/evidence-review/data")
    @admins_only
    def admin_evidence_review_data():
        return jsonify({"success": True, "data": build_admin_payload()})

    @blueprint.post("/admin/evidence-review/requirements/<int:requirement_id>/review")
    @admins_only
    def admin_review_requirement(requirement_id: int):
        requirement = SolveEvidenceRequirement.query.filter_by(id=requirement_id).first()
        if requirement is None:
            return jsonify({"success": False, "message": "Expediente no encontrado."}), 404
        data = request.get_json(silent=True) or request.form.to_dict()
        review_status = (data.get("review_status") or "unreviewed").strip()
        review_notes = (data.get("review_notes") or "").strip()
        if review_status not in REVIEW_STATES:
            return jsonify({"success": False, "message": "Dictamen inválido."}), 400
        admin = get_current_user()
        requirement.review_status = review_status
        requirement.review_notes = review_notes
        if review_status == "unreviewed":
            requirement.reviewed_at = None
            requirement.reviewed_by_id = None
        else:
            requirement.reviewed_at = datetime.utcnow()
            requirement.reviewed_by_id = admin.id if admin else None
        db.session.add(requirement)
        db.session.commit()
        return jsonify({"success": True, "message": "Dictamen guardado.", "data": serialize_requirement(requirement, admin=True)})

    @blueprint.get("/admin/evidence-review/files/<int:asset_id>")
    @admins_only
    def admin_requirement_asset(asset_id: int):
        asset = SolveEvidenceAsset.query.filter_by(id=asset_id).first()
        if asset is None:
            abort(404)
        path = private_evidence_root() / asset.stored_name
        if not path.exists():
            abort(404)
        return send_file(path, mimetype=asset.mime_type or "application/octet-stream", as_attachment=False, download_name=asset.original_name)

    @blueprint.get("/admin/requirements")
    @admins_only
    def admin_requirements():
        requirements = (
            SolveEvidenceRequirement.query.order_by(
                SolveEvidenceRequirement.created_at.desc(),
                SolveEvidenceRequirement.id.desc(),
            ).all()
        )
        return jsonify({"success": True, "data": [serialize_requirement(item, admin=True) for item in requirements]})

    return blueprint


def load(app):
    with app.app_context():
        ensure_schema()
        patch_challenge_solve()
        patch_attempt_post()
        patch_solution_get()
        reconcile_requirements()
        app.register_blueprint(build_user_blueprint(), url_prefix="/plugins/solve_evidence_guard")
        app.register_blueprint(build_admin_blueprint(), url_prefix="")
