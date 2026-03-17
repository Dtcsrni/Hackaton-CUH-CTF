#!/usr/bin/env bash
set -euo pipefail

CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}

docker exec -i "${CTFD_CONTAINER}" python3 - <<'PY'
import re
from CTFd import create_app
from CTFd.models import Configs, db

STYLE_BLOCK = r"""
<style id="ctfcu-challenge-notification-fix">
  .notification-row .alert {
    border-radius: 18px !important;
    border-width: 1px !important;
    border-style: solid !important;
    box-shadow: 0 18px 34px rgba(0, 0, 0, 0.18) !important;
    padding: 18px 18px 16px !important;
    line-height: 1.6 !important;
    backdrop-filter: blur(10px);
  }

  .notification-row .alert strong,
  .notification-row .alert small,
  .notification-row .alert p,
  .notification-row .alert span,
  .notification-row .alert div {
    color: inherit !important;
    opacity: 1 !important;
  }

  .notification-row .alert strong {
    display: block !important;
    font-size: 1.08rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.01em;
  }

  .notification-row .alert-success {
    color: #effff5 !important;
    background:
      radial-gradient(circle at 18% 18%, rgba(132, 255, 184, 0.18), transparent 34%),
      linear-gradient(180deg, rgba(11, 58, 31, 0.96), rgba(6, 33, 19, 0.98)) !important;
    border-color: rgba(135, 255, 187, 0.34) !important;
  }

  .notification-row .alert-info {
    color: #eef7ff !important;
    background:
      radial-gradient(circle at 18% 18%, rgba(122, 205, 255, 0.18), transparent 34%),
      linear-gradient(180deg, rgba(15, 50, 78, 0.96), rgba(8, 28, 45, 0.98)) !important;
    border-color: rgba(122, 205, 255, 0.30) !important;
  }

  .notification-row .alert-danger {
    color: #fff0f2 !important;
    background:
      radial-gradient(circle at 18% 18%, rgba(255, 136, 158, 0.18), transparent 34%),
      linear-gradient(180deg, rgba(78, 20, 31, 0.96), rgba(43, 10, 18, 0.98)) !important;
    border-color: rgba(255, 136, 158, 0.30) !important;
  }

  .notification-row .alert-warning {
    color: #fff7ea !important;
    background:
      radial-gradient(circle at 18% 18%, rgba(255, 204, 117, 0.18), transparent 34%),
      linear-gradient(180deg, rgba(84, 53, 14, 0.96), rgba(49, 31, 8, 0.98)) !important;
    border-color: rgba(255, 204, 117, 0.28) !important;
  }

  .notification-row .alert .btn,
  .notification-row .alert .btn-outline-info,
  .notification-row .alert .btn-outline-secondary,
  .notification-row .alert .btn-primary {
    color: #f6fffb !important;
    border-color: rgba(230, 255, 241, 0.26) !important;
  }

  .notification-row .alert .btn-outline-info:hover,
  .notification-row .alert .btn-outline-secondary:hover,
  .notification-row .alert .btn-primary:hover {
    background: rgba(255, 255, 255, 0.12) !important;
  }
</style>
"""

app = create_app()

with app.app_context():
    cfg = Configs.query.filter_by(key='theme_header').first()
    if cfg is None:
        raise SystemExit('theme_header not found')
    value = cfg.value or ''
    value = re.sub(r'<style id="ctfcu-challenge-notification-fix">.*?</style>\s*', '', value, flags=re.S)
    cfg.value = value.rstrip() + "\n" + STYLE_BLOCK.strip() + "\n"
    db.session.commit()
    print('challenge notification style updated')
PY
