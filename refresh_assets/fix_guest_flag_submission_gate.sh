#!/usr/bin/env bash
set -euo pipefail

CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}

docker exec -i "${CTFD_CONTAINER}" python3 - <<'PY'
import re
from CTFd import create_app
from CTFd.models import Configs, db

STYLE_BLOCK = r"""
<style id="ctfcu-guest-submission-gate">
  .ctfcu-guest-submit-note {
    margin-top: 14px;
    padding: 14px 16px;
    border-radius: 16px;
    border: 1px solid rgba(122, 205, 255, 0.20);
    background: linear-gradient(180deg, rgba(12, 39, 66, 0.92), rgba(7, 24, 42, 0.96));
    color: #eef7ff;
    box-shadow: 0 14px 28px rgba(0, 0, 0, 0.16);
  }

  .ctfcu-guest-submit-note strong,
  .ctfcu-guest-submit-note span {
    display: block;
    color: inherit;
  }

  .ctfcu-guest-submit-note strong {
    font-size: 0.98rem;
    font-weight: 800;
  }

  .ctfcu-guest-submit-note span {
    margin-top: 4px;
    line-height: 1.6;
    color: rgba(238, 247, 255, 0.88);
    font-size: 0.92rem;
  }

  .challenge-window .challenge-input.ctfcu-guest-disabled {
    opacity: 0.72 !important;
    cursor: not-allowed !important;
  }

  .challenge-window .challenge-submit.ctfcu-login-cta {
    color: #eef7ff !important;
    border-color: rgba(122, 205, 255, 0.30) !important;
    background: linear-gradient(180deg, rgba(17, 76, 123, 0.92), rgba(11, 49, 82, 0.98)) !important;
    box-shadow: 0 12px 26px rgba(0, 0, 0, 0.16) !important;
  }

  .challenge-window .challenge-submit.ctfcu-login-cta:hover {
    background: linear-gradient(180deg, rgba(22, 91, 145, 0.96), rgba(13, 57, 95, 1)) !important;
  }
</style>
"""

SCRIPT_BLOCK = r"""
<script id="ctfcu-guest-submission-gate-script">
(() => {
  function isGuest() {
    return !window.init || !window.init.userId || Number(window.init.userId) === 0;
  }

  function loginTarget() {
    const next = encodeURIComponent('/challenges');
    return `/login?next=${next}`;
  }

  function upgradeGuestModal(modal) {
    if (!modal || modal.dataset.ctfcuGuestGate === '1' || !isGuest()) {
      return;
    }

    const input = modal.querySelector('.challenge-input');
    const button = modal.querySelector('.challenge-submit');
    const submitRow = modal.querySelector('.submit-row');
    if (!input || !button || !submitRow) {
      return;
    }

    input.value = '';
    input.disabled = true;
    input.placeholder = 'Inicia sesión para enviar banderas';
    input.classList.add('ctfcu-guest-disabled');

    button.textContent = 'Iniciar sesión';
    button.classList.add('ctfcu-login-cta');
    button.disabled = false;
    button.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      window.location.href = loginTarget();
    }, true);

    if (!modal.querySelector('.ctfcu-guest-submit-note')) {
      const note = document.createElement('div');
      note.className = 'ctfcu-guest-submit-note';
      note.innerHTML = `
        <strong>Debes iniciar sesión para enviar una bandera</strong>
        <span>Puedes explorar retos y leer descripciones sin sesión, pero el envío de flags y la acreditación de puntos solo se habilitan para participantes autenticados.</span>
      `;
      submitRow.insertAdjacentElement('afterend', note);
    }

    modal.dataset.ctfcuGuestGate = '1';
  }

  function scan() {
    if (!isGuest()) return;
    document.querySelectorAll('.challenge-window, [x-data="Challenge"]').forEach(upgradeGuestModal);
  }

  function observeBodyReady(callback) {
    const start = () => new MutationObserver(callback).observe(document.body, { childList: true, subtree: true });
    if (document.body) {
      start();
      return;
    }
    window.addEventListener('DOMContentLoaded', start, { once: true });
  }

  document.addEventListener('DOMContentLoaded', scan);
  observeBodyReady(scan);
})();
</script>
"""

app = create_app()

with app.app_context():
    cfg = Configs.query.filter_by(key='theme_header').first()
    if cfg is None:
        raise SystemExit('theme_header not found')
    value = cfg.value or ''
    value = re.sub(r'<style id="ctfcu-guest-submission-gate">.*?</style>\s*', '', value, flags=re.S)
    value = re.sub(r'<script id="ctfcu-guest-submission-gate-script">.*?</script>\s*', '', value, flags=re.S)
    cfg.value = value.rstrip() + "\n" + STYLE_BLOCK.strip() + "\n" + SCRIPT_BLOCK.strip() + "\n"
    db.session.commit()
    print('guest submission gate updated')
PY
