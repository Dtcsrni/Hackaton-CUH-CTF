#!/usr/bin/env bash
set -euo pipefail

CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}

docker exec -i "${CTFD_CONTAINER}" python3 - <<'PY'
import re
from CTFd import create_app
from CTFd.models import Configs, db

STYLE_BLOCK = r"""
<style id="ctfcu-success-celebration-style">
  @keyframes ctfcuCelebratePop {
    0% { transform: translateY(10px) scale(0.96); opacity: 0; }
    100% { transform: translateY(0) scale(1); opacity: 1; }
  }

  @keyframes ctfcuCelebrateFloat {
    0% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-8px) scale(1.02); }
    100% { transform: translateY(0) scale(1); }
  }

  @keyframes ctfcuCelebrateShine {
    0% { transform: translateX(-140%) skewX(-18deg); opacity: 0; }
    25% { opacity: 0.22; }
    100% { transform: translateX(220%) skewX(-18deg); opacity: 0; }
  }

  @keyframes ctfcuCelebrateConfetti {
    0% { transform: translateY(-6px) rotate(0deg); opacity: 0; }
    15% { opacity: 1; }
    100% { transform: translateY(18px) rotate(18deg); opacity: 0; }
  }

  .notification-row .alert-success.ctfcu-success-upgraded {
    position: relative;
    overflow: hidden;
  }

  .notification-row .alert-success.ctfcu-success-upgraded::before {
    content: "";
    position: absolute;
    inset: 0 auto 0 -18%;
    width: 28%;
    background: linear-gradient(90deg, rgba(255,255,255,0), rgba(227,255,238,0.18), rgba(255,255,255,0));
    pointer-events: none;
    animation: ctfcuCelebrateShine 3.6s ease-in-out infinite;
  }

  .ctfcu-success-card {
    margin: 14px auto 10px;
    max-width: 440px;
    padding: 16px 16px 14px;
    border-radius: 20px;
    border: 1px solid rgba(162, 255, 201, 0.30);
    background:
      radial-gradient(circle at 50% 16%, rgba(175, 255, 209, 0.16), transparent 28%),
      linear-gradient(180deg, rgba(14, 71, 39, 0.86), rgba(8, 39, 23, 0.92));
    box-shadow:
      0 20px 44px rgba(0, 0, 0, 0.26),
      inset 0 0 0 1px rgba(255,255,255,0.04);
    animation: ctfcuCelebratePop .42s ease-out both;
  }

  .ctfcu-success-card-media {
    position: relative;
    overflow: hidden;
    border-radius: 18px;
    border: 1px solid rgba(191, 255, 217, 0.22);
    background: linear-gradient(180deg, rgba(4,20,12,.66), rgba(4,20,12,.94));
  }

  .ctfcu-success-card-media img {
    display: block;
    width: 100%;
    aspect-ratio: 16 / 10;
    object-fit: cover;
    object-position: center;
    animation: ctfcuCelebrateFloat 4.4s ease-in-out infinite;
  }

  .ctfcu-success-card-media::after {
    content: "Tigrillo victorioso";
    position: absolute;
    left: 12px;
    bottom: 12px;
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(5, 25, 14, 0.74);
    border: 1px solid rgba(179, 255, 213, 0.24);
    color: #effff5;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.03em;
    text-transform: uppercase;
  }

  .ctfcu-success-confetti {
    position: absolute;
    inset: 0;
    pointer-events: none;
    overflow: hidden;
  }

  .ctfcu-success-confetti span {
    position: absolute;
    top: 8px;
    width: 8px;
    height: 18px;
    border-radius: 999px;
    animation: ctfcuCelebrateConfetti 2.2s ease-in-out infinite;
  }

  .ctfcu-success-confetti span:nth-child(1) { left: 14%; background: #72f7b2; animation-delay: 0s; }
  .ctfcu-success-confetti span:nth-child(2) { left: 28%; background: #ffd166; animation-delay: .35s; }
  .ctfcu-success-confetti span:nth-child(3) { left: 47%; background: #7ccfff; animation-delay: .7s; }
  .ctfcu-success-confetti span:nth-child(4) { left: 66%; background: #ff8fb0; animation-delay: 1.05s; }
  .ctfcu-success-confetti span:nth-child(5) { left: 83%; background: #9bff7e; animation-delay: 1.4s; }

  .ctfcu-success-copy {
    margin-top: 14px;
    text-align: center;
  }

  .ctfcu-success-copy strong,
  .ctfcu-success-copy span {
    display: block;
  }

  .ctfcu-success-copy strong {
    color: #f4fff8;
    font-size: 1.02rem;
    line-height: 1.25;
  }

  .ctfcu-success-copy span {
    margin-top: 6px;
    color: rgba(238, 255, 245, 0.86);
    line-height: 1.6;
    font-size: 0.94rem;
  }

  .notification-row .alert-success.ctfcu-success-upgraded > strong {
    text-transform: none !important;
  }

  @media (prefers-reduced-motion: reduce) {
    .notification-row .alert-success.ctfcu-success-upgraded::before,
    .ctfcu-success-card,
    .ctfcu-success-card-media img,
    .ctfcu-success-confetti span {
      animation: none !important;
    }
  }
</style>
"""

SCRIPT_BLOCK = r"""
<script id="ctfcu-success-celebration-script">
(() => {
  const TIGRILLO_URL = "https://commons.wikimedia.org/wiki/Special:Redirect/file/Ocelot.jpg";

  function upgradeSuccessAlert(alert) {
    if (!alert || alert.dataset.ctfcuSuccessDone === "1") {
      return;
    }

    const strong = alert.querySelector("strong");
    if (strong) {
      strong.textContent = "Bandera correcta";
    }

    alert.classList.add("ctfcu-success-upgraded");

    const shareTrigger = Array.from(alert.querySelectorAll("button, a")).find((el) => {
      const txt = (el.textContent || "").trim().toLowerCase();
      return txt === "share" || txt === "compartir";
    });
    if (shareTrigger) {
      shareTrigger.textContent = "Compartir logro";
    }

    Array.from(alert.querySelectorAll("*")).forEach((node) => {
      if (!node || !node.textContent) return;
      const txt = node.textContent.trim();
      if (txt === "Rate this challenge:") node.textContent = "¿Qué te pareció este reto?";
      if (txt === "Write a review (optional)") node.textContent = "Escribe una reseña breve (opcional)";
      if (txt === "Submit") node.textContent = "Enviar opinión";
      if (txt === "Thank you for your rating!") node.textContent = "Gracias por calificar este reto";
      if (txt === "Next Challenge") node.textContent = "Siguiente reto";
    });

    const review = alert.querySelector('textarea[placeholder="Write a review (optional)"]');
    if (review) {
      review.placeholder = "Escribe una reseña breve (opcional)";
    }

    const existingNote = alert.querySelector(".ctfcu-share-note");
    if (existingNote) {
      existingNote.textContent = "En esta instancia del laboratorio, Facebook y LinkedIn no generan una vista previa fiable con enlaces sobre IP pública. Usa Copiar enlace, Compartir desde el navegador o X.";
    }

    if (!alert.querySelector(".ctfcu-success-card")) {
      const card = document.createElement("div");
      card.className = "ctfcu-success-card";
      card.innerHTML = `
        <div class="ctfcu-success-card-media">
          <img src="${TIGRILLO_URL}" alt="Tigrillo hacker victorioso del laboratorio">
          <div class="ctfcu-success-confetti">
            <span></span><span></span><span></span><span></span><span></span>
          </div>
        </div>
        <div class="ctfcu-success-copy">
          <strong>Reto derrotado y puntos acreditados</strong>
          <span>Tu bandera fue validada correctamente. Sigue con el siguiente desafío o comparte el logro usando las opciones del laboratorio.</span>
        </div>`;

      const firstHr = alert.querySelector("hr");
      if (firstHr) {
        firstHr.parentNode.insertBefore(card, firstHr);
      } else {
        alert.appendChild(card);
      }
    }

    alert.dataset.ctfcuSuccessDone = "1";
  }

  function scan() {
    document.querySelectorAll(".notification-row .alert-success").forEach(upgradeSuccessAlert);
  }

  function observeBodyReady(callback) {
    const start = () => {
      if (!(document.body instanceof Node)) {
        return;
      }
      new MutationObserver(callback).observe(document.body, { childList: true, subtree: true });
    };
    if (document.body instanceof Node) {
      start();
      return;
    }
    window.addEventListener("DOMContentLoaded", start, { once: true });
  }

  document.addEventListener("DOMContentLoaded", scan);
  observeBodyReady(scan);
})();
</script>
"""

app = create_app()

with app.app_context():
    cfg = Configs.query.filter_by(key='theme_footer').first()
    if cfg is None:
        raise SystemExit('theme_footer not found')
    value = cfg.value or ''
    value = re.sub(r'<style id="ctfcu-success-celebration-style">.*?</style>\s*', '', value, flags=re.S)
    value = re.sub(r'<script id="ctfcu-success-celebration-script">.*?</script>\s*', '', value, flags=re.S)
    cfg.value = value.rstrip() + "\n" + STYLE_BLOCK.strip() + "\n" + SCRIPT_BLOCK.strip() + "\n"
    db.session.commit()
    print('success celebration updated')
PY
