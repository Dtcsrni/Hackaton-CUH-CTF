#!/usr/bin/env bash
set -euo pipefail

CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}
WORKDIR=/tmp/cuh_ctfd_guest_challenges
mkdir -p "$WORKDIR"
trap 'rm -rf "$WORKDIR"' EXIT

cat > "$WORKDIR/apply_guest_challenges_blur.py" <<'PY'
import re
from CTFd import create_app
from CTFd.models import Configs, db

BLOCK = r'''<!-- CTFCU_GUEST_CHALLENGES_START --><style id="ctfcu-guest-challenges-style">
  body.ctfcu-guest-challenges-view [x-data="ChallengeBoard"] {
    position: relative;
    isolation: isolate;
  }

  body.ctfcu-guest-challenges-view [x-data="ChallengeBoard"] .challenges-row,
  body.ctfcu-guest-challenges-view [x-data="ChallengeBoard"] .challenge-button,
  body.ctfcu-guest-challenges-view [x-data="ChallengeBoard"] .challenge-inner {
    filter: blur(8px) saturate(0.72);
    pointer-events: none !important;
    user-select: none;
  }

  body.ctfcu-guest-challenges-view [x-data="ChallengeBoard"] .category-header {
    opacity: 0.74;
  }

  body.ctfcu-guest-challenges-view [x-data="ChallengeBoard"] .challenge-button {
    transform: none !important;
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.24) !important;
  }

  .ctfcu-guest-challenge-overlay {
    position: sticky;
    top: calc(var(--nav-height) + 18px);
    z-index: 8;
    width: min(760px, calc(100% - 20px));
    margin: 24px auto 0;
    padding: 22px 24px;
    border-radius: 26px;
    border: 1px solid rgba(114, 244, 255, 0.18);
    background:
      radial-gradient(circle at 18% 18%, rgba(114, 244, 255, 0.16), transparent 24%),
      linear-gradient(180deg, rgba(17, 31, 60, 0.94), rgba(6, 12, 25, 0.97));
    box-shadow: 0 22px 60px rgba(0, 0, 0, 0.34);
    backdrop-filter: blur(12px);
    animation: ctfcuGuestOverlayFloat 3.8s ease-in-out infinite;
  }

  .ctfcu-guest-challenge-overlay h2 {
    margin: 0 0 10px;
    color: #fff;
    font-size: clamp(1.35rem, 2.8vw, 2rem);
    line-height: 1.12;
  }

  .ctfcu-guest-challenge-overlay p {
    margin: 0;
    color: rgba(217, 232, 251, 0.84);
    line-height: 1.8;
    font-size: 0.98rem;
  }

  .ctfcu-guest-challenge-overlay .ctfcu-overlay-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 16px;
  }

  .ctfcu-overlay-login,
  .ctfcu-overlay-login:visited {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 48px;
    padding: 0 18px;
    border-radius: 16px;
    color: #04121f;
    text-decoration: none;
    font-weight: 800;
    background: linear-gradient(135deg, #72f4ff, #73ffb3);
    box-shadow: 0 14px 32px rgba(114, 244, 255, 0.20);
  }

  .ctfcu-overlay-note {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    min-height: 48px;
    padding: 0 16px;
    border-radius: 16px;
    color: #eef6ff;
    font-weight: 700;
    background: linear-gradient(180deg, rgba(17, 30, 58, 0.88), rgba(7, 14, 28, 0.96));
    border: 1px solid rgba(177, 224, 255, 0.14);
  }

  .ctfcu-login-arrow {
    position: fixed;
    top: calc(var(--nav-height) + 8px);
    left: 16px;
    z-index: 10060;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 999px;
    color: #04131f;
    font-weight: 900;
    letter-spacing: 0.01em;
    background: linear-gradient(135deg, #73ffb3, #72f4ff);
    box-shadow:
      0 14px 36px rgba(115, 255, 179, 0.22),
      0 0 0 1px rgba(255, 255, 255, 0.10);
    transform-origin: center;
    animation: ctfcuArrowBounce 1.45s ease-in-out infinite;
  }

  .ctfcu-login-arrow::after {
    content: "";
    position: absolute;
    left: 26px;
    top: -18px;
    width: 2px;
    height: 22px;
    background: linear-gradient(180deg, rgba(115,255,179,0), rgba(115,255,179,0.94));
  }

  .ctfcu-login-arrow .ctfcu-arrow-icon {
    width: 28px;
    height: 28px;
    border-radius: 999px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: rgba(4, 19, 31, 0.12);
    font-size: 0.95rem;
  }

  .ctfcu-login-arrow[data-target="toggler"] {
    background: linear-gradient(135deg, #ffe271, #73ffb3);
  }

  @keyframes ctfcuGuestOverlayFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-3px); }
  }

  @keyframes ctfcuArrowBounce {
    0%, 100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-6px) scale(1.04); }
  }

  @media (max-width: 1399.98px) {
    .ctfcu-guest-challenge-overlay {
      top: calc(var(--nav-height) + 8px);
    }
  }

  @media (max-width: 767.98px) {
    .ctfcu-guest-challenge-overlay {
      width: calc(100% - 8px);
      padding: 18px;
    }

    .ctfcu-login-arrow {
      max-width: calc(100vw - 20px);
      padding: 10px 12px;
      font-size: 0.9rem;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .ctfcu-guest-challenge-overlay,
    .ctfcu-login-arrow {
      animation: none !important;
      transition: none !important;
    }
  }
</style>
<script id="ctfcu-guest-challenges-script">
(() => {
  function isGuestChallengesView() {
    const nav = document.querySelector('.navbar[data-auth="0"]');
    if (!nav) return false;
    return window.location.pathname === '/challenges';
  }

  function ensureOverlay(board) {
    if (!board || board.querySelector(':scope > .ctfcu-guest-challenge-overlay')) return;
    const overlay = document.createElement('div');
    overlay.className = 'ctfcu-guest-challenge-overlay';
    overlay.innerHTML = `
      <h2>Primero inicia sesión; después se desbloquea el tablero completo de misiones.</h2>
      <p>En esta vista de invitado los desafíos aparecen difuminados a propósito. El objetivo es que el participante entre con su cuenta para registrar solves, ver progreso, desbloquear interacción completa y acreditar puntos dentro del laboratorio controlado.</p>
      <div class="ctfcu-overlay-actions">
        <a class="ctfcu-overlay-login" href="/login?next=/challenges"><i class="fa-solid fa-right-to-bracket"></i>&nbsp;Ir a Inicio de sesión</a>
        <span class="ctfcu-overlay-note"><i class="fa-solid fa-circle-info"></i> El marcador, los envíos de bandera y el progreso solo se registran con sesión activa.</span>
      </div>
    `;
    board.prepend(overlay);
  }

  function ensureArrow() {
    let arrow = document.querySelector('.ctfcu-login-arrow');
    if (!arrow) {
      arrow = document.createElement('div');
      arrow.className = 'ctfcu-login-arrow';
      arrow.innerHTML = `<span class="ctfcu-arrow-icon"><i class="fa-solid fa-arrow-up"></i></span><span class="ctfcu-arrow-label">Inicia sesión para entrar al laboratorio</span>`;
      document.body.appendChild(arrow);
    }
    return arrow;
  }

  function positionArrow() {
    const arrow = ensureArrow();
    const login = document.querySelector('.ctfcu-login-link');
    const toggler = document.querySelector('.navbar-toggler');
    const loginRect = login ? login.getBoundingClientRect() : null;
    const loginVisible = loginRect && loginRect.width > 0 && loginRect.height > 0;
    const target = loginVisible ? login : toggler;
    if (!target) return;
    const rect = target.getBoundingClientRect();
    const left = Math.max(12, Math.min(window.innerWidth - arrow.offsetWidth - 12, rect.left + (rect.width / 2) - (arrow.offsetWidth / 2)));
    const top = Math.max(10, rect.bottom + 10);
    arrow.style.left = `${left}px`;
    arrow.style.top = `${top}px`;
    arrow.dataset.target = loginVisible ? 'login' : 'toggler';
    const label = arrow.querySelector('.ctfcu-arrow-label');
    if (label) {
      label.textContent = loginVisible
        ? 'Inicia sesión para entrar al laboratorio'
        : 'Abre el menú y entra a Inicio de sesión';
    }
  }

  function mount() {
    if (!isGuestChallengesView()) return;
    document.body.classList.add('ctfcu-guest-challenges-view');
    const board = document.querySelector('[x-data="ChallengeBoard"]');
    if (board) ensureOverlay(board);
    positionArrow();
  }

  function observeBodyReady(callback) {
    const start = () => new MutationObserver(callback).observe(document.body, { childList: true, subtree: true });
    if (document.body) {
      start();
      return;
    }
    window.addEventListener('DOMContentLoaded', start, { once: true });
  }

  document.addEventListener('DOMContentLoaded', mount);
  window.addEventListener('resize', () => {
    if (document.body.classList.contains('ctfcu-guest-challenges-view')) {
      positionArrow();
    }
  });
  window.addEventListener('scroll', () => {
    if (document.body.classList.contains('ctfcu-guest-challenges-view')) {
      positionArrow();
    }
  }, { passive: true });
  observeBodyReady(() => {
    if (document.body.classList.contains('ctfcu-guest-challenges-view')) {
      const board = document.querySelector('[x-data="ChallengeBoard"]');
      if (board) ensureOverlay(board);
      positionArrow();
    } else {
      mount();
    }
  });
})();
</script><!-- CTFCU_GUEST_CHALLENGES_END -->'''


def upsert(value, start, end, block):
    value = re.sub(re.escape(start) + r'.*?' + re.escape(end), '', str(value), flags=re.S).strip()
    return (value + '\n' if value else '') + block + '\n'


app = create_app()
with app.app_context():
    header = Configs.query.filter_by(key='theme_header').first()
    header.value = upsert(
        header.value,
        '<!-- CTFCU_GUEST_CHALLENGES_START -->',
        '<!-- CTFCU_GUEST_CHALLENGES_END -->',
        BLOCK,
    )
    db.session.commit()
    print('guest challenges blur synced')
PY

docker cp "$WORKDIR/apply_guest_challenges_blur.py" "$CTFD_CONTAINER:/tmp/apply_guest_challenges_blur.py"
docker exec -e PYTHONPATH=/opt/CTFd "$CTFD_CONTAINER" python3 /tmp/apply_guest_challenges_blur.py
