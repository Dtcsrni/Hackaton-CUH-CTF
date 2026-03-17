#!/usr/bin/env bash
set -euo pipefail

CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}

docker exec -i "${CTFD_CONTAINER}" python3 - <<'PY'
import re
from CTFd import create_app
from CTFd.models import Configs, db

STYLE_BLOCK = r"""
<style id="ctfcu-solved-challenge-fix">
  @keyframes ctfcuSolvedPulse {
    0% {
      box-shadow:
        0 14px 30px rgba(3, 18, 11, 0.24),
        0 0 0 0 rgba(63, 255, 132, 0.26),
        inset 0 0 0 1px rgba(255, 255, 255, 0.04);
    }
    70% {
      box-shadow:
        0 18px 38px rgba(3, 18, 11, 0.30),
        0 0 0 14px rgba(63, 255, 132, 0),
        inset 0 0 0 1px rgba(255, 255, 255, 0.05);
    }
    100% {
      box-shadow:
        0 14px 30px rgba(3, 18, 11, 0.24),
        0 0 0 0 rgba(63, 255, 132, 0),
        inset 0 0 0 1px rgba(255, 255, 255, 0.04);
    }
  }

  @keyframes ctfcuSolvedSweep {
    0% {
      transform: translateX(-135%) skewX(-18deg);
      opacity: 0;
    }
    18% {
      opacity: 0.22;
    }
    42% {
      opacity: 0.34;
    }
    100% {
      transform: translateX(245%) skewX(-18deg);
      opacity: 0;
    }
  }

  .challenge-button.challenge-solved,
  .challenge-button.challenge-solved.btn,
  .challenge-button.challenge-solved.btn-dark,
  .challenge-button.challenge-solved:hover,
  .challenge-button.challenge-solved:focus,
  .challenge-button.challenge-solved:active {
    position: relative !important;
    overflow: hidden !important;
    background:
      radial-gradient(circle at 18% 18%, rgba(110, 255, 170, 0.18), transparent 34%),
      linear-gradient(180deg, rgba(13, 58, 31, 0.96), rgba(6, 31, 18, 0.98)) !important;
    border: 1px solid rgba(110, 255, 170, 0.34) !important;
    color: #f3fff8 !important;
    box-shadow:
      0 14px 30px rgba(3, 18, 11, 0.24),
      0 0 0 0 rgba(63, 255, 132, 0.22),
      inset 0 0 0 1px rgba(255, 255, 255, 0.04) !important;
    transform: none !important;
    filter: none !important;
    animation: ctfcuSolvedPulse 2.8s ease-in-out infinite !important;
  }

  .challenge-button.challenge-solved::before {
    content: "";
    position: absolute;
    inset: -20% auto -20% -30%;
    width: 42%;
    background: linear-gradient(90deg, rgba(255,255,255,0), rgba(210,255,228,0.20), rgba(255,255,255,0));
    pointer-events: none;
    animation: ctfcuSolvedSweep 4.4s ease-in-out infinite;
  }

  .challenge-button.challenge-solved .challenge-inner,
  .challenge-button.challenge-solved .challenge-inner p,
  .challenge-button.challenge-solved .challenge-inner span {
    color: inherit !important;
    opacity: 1 !important;
  }

  .challenge-button.challenge-solved::after {
    content: "Derrotada";
    position: absolute;
    top: 10px;
    right: 10px;
    padding: 5px 10px;
    border-radius: 999px;
    background: rgba(124, 255, 177, 0.16);
    border: 1px solid rgba(151, 255, 196, 0.32);
    color: #effff6;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    line-height: 1;
    pointer-events: none;
    text-transform: uppercase;
  }

  .challenge-button.challenge-solved .challenge-inner p {
    color: #ebfff2 !important;
  }

  .challenge-button.challenge-solved .challenge-inner span {
    color: #d5ffe4 !important;
  }

  .challenge-button.challenge-solved .challenge-inner {
    transform: translateZ(0);
  }

  @media (prefers-reduced-motion: reduce) {
    .challenge-button.challenge-solved,
    .challenge-button.challenge-solved::before {
      animation: none !important;
    }
  }
</style>
"""

app = create_app()

with app.app_context():
    cfg = Configs.query.filter_by(key='theme_header').first()
    if cfg is None:
        raise SystemExit('theme_header not found')
    value = cfg.value or ''
    value = re.sub(r'<style id="ctfcu-solved-challenge-fix">.*?</style>\s*', '', value, flags=re.S)
    cfg.value = value.rstrip() + "\n" + STYLE_BLOCK.strip() + "\n"
    db.session.commit()
    print('completed challenge style updated')
PY
