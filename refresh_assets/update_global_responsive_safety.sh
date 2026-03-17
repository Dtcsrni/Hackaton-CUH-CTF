#!/usr/bin/env bash
set -euo pipefail

CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}
WORKDIR=/tmp/cuh_ctfd_responsive_safety
mkdir -p "$WORKDIR"
trap 'rm -rf "$WORKDIR"' EXIT

cat > "$WORKDIR/apply_global_responsive_safety.py" <<'PY'
import re
from CTFd import create_app
from CTFd.models import Configs, db

BLOCK = r'''<!-- CTFCU_RESPONSIVE_SAFETY_START --><style id="ctfcu-responsive-safety">
  html, body {
    max-width: 100%;
    overflow-x: hidden !important;
  }

  main,
  .jumbotron,
  .container,
  .container-fluid,
  .row,
  [class*="col-"] {
    min-width: 0;
  }

  img,
  video,
  canvas,
  svg,
  iframe {
    max-width: 100%;
    height: auto;
  }

  .cuhv-page,
  .ctfcu-scoreboard-page,
  .ctfcu-user-page,
  .ctfcu-challenges-page {
    width: 100%;
    max-width: min(100%, 1680px);
  }

  .challenge-window .modal-dialog,
  .modal-dialog {
    max-width: min(980px, calc(100vw - 24px));
  }

  .challenge-window.modal .modal-content,
  .modal .modal-content {
    width: 100%;
    max-width: 100%;
  }

  #base-navbars {
    min-width: 0 !important;
  }

  .navbar .navbar-nav {
    min-width: 0 !important;
  }

  @media (max-width: 991.98px) {
    .table {
      display: block;
      width: 100%;
      overflow-x: auto;
      white-space: nowrap;
      -webkit-overflow-scrolling: touch;
    }

    .jumbotron {
      padding-top: 8px !important;
      padding-bottom: 8px !important;
    }

    .jumbotron h1 {
      font-size: clamp(1.8rem, 7.8vw, 2.7rem) !important;
      line-height: 1.04 !important;
      margin: 0 !important;
    }

    .cuhv-page,
    .ctfcu-scoreboard-page,
    .ctfcu-user-page,
    .ctfcu-challenges-page {
      padding-left: 14px !important;
      padding-right: 14px !important;
    }

    .cuhv-grid-4,
    .ctfcu-user-awards-grid,
    .ctfcu-user-insights-grid,
    .ctfcu-challenges-grid {
      grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    }
  }

  @media (max-width: 767.98px) {
    :root {
      --nav-height: 88px;
    }

    body {
      padding-top: 102px !important;
    }

    .navbar {
      min-height: var(--nav-height) !important;
      padding-top: 8px !important;
      padding-bottom: 8px !important;
    }

    .navbar > .container.ctfcu-navbar-shell {
      max-width: calc(100vw - 8px) !important;
      padding-left: 10px !important;
      padding-right: 10px !important;
    }

    .navbar-brand {
      height: 60px !important;
    }

    .navbar-brand img {
      height: 52px !important;
    }

    .navbar-toggler {
      min-width: 64px;
      min-height: 52px;
    }

    #base-navbars {
      max-height: calc(100vh - var(--nav-height) - 18px);
      overflow-y: auto;
      overflow-x: hidden;
      border-radius: 18px;
    }

    .jumbotron .container,
    main > .container {
      padding-left: 12px !important;
      padding-right: 12px !important;
    }

    .cuhv-page,
    .ctfcu-scoreboard-page,
    .ctfcu-user-page,
    .ctfcu-challenges-page {
      padding: 14px 10px 52px !important;
    }

    .cuhv-hero,
    .cuhv-section,
    .ctfcu-score-shell,
    .ctfcu-score-hero,
    .ctfcu-score-status,
    .ctfcu-user-shell,
    .ctfcu-user-card,
    .ctfcu-user-stat-card,
    .ctfcu-user-chart-card,
    .ctfcu-user-chart-wide,
    .ctfcu-user-award-card,
    .ctfcu-user-solves-card,
    .ctfcu-user-insight-card,
    .ctfcu-category-shell,
    .ctfcu-category-nav,
    .ctfcu-challenges-card,
    .ctfcu-challenge-stat,
    .ctfcu-board-empty,
    .card,
    .challenge-button,
    .ctfcu-guest-challenge-overlay,
    .ctfcu-score-row,
    .ctfcu-podium-card {
      border-radius: 18px !important;
    }

    .challenge-button {
      min-height: 106px !important;
    }

    .ctfcu-user-hero,
    .ctfcu-user-analytics,
    .ctfcu-user-evidence-grid,
    .ctfcu-challenges-hero,
    .ctfcu-modal-hero,
    .ctfcu-modal-layout {
      grid-template-columns: 1fr !important;
    }

    .challenge-inner p {
      margin-bottom: 8px !important;
      line-height: 1.2 !important;
      word-break: break-word;
    }

    .ctfcu-guest-challenge-overlay {
      position: relative !important;
      top: 0 !important;
      width: calc(100% - 6px) !important;
      margin-top: 14px !important;
      padding: 18px !important;
    }

    .ctfcu-login-arrow {
      max-width: calc(100vw - 20px);
      z-index: 10080 !important;
    }
  }

  @media (max-width: 575.98px) {
    body {
      padding-top: 96px !important;
    }

    .navbar {
      min-height: 82px !important;
    }

    .navbar-brand {
      height: 54px !important;
    }

    .navbar-brand img {
      height: 46px !important;
    }

    .navbar-toggler {
      min-width: 58px;
      min-height: 48px;
      padding: 8px 10px !important;
    }

    .cuhv-page,
    .ctfcu-scoreboard-page,
    .ctfcu-user-page,
    .ctfcu-challenges-page {
      padding: 12px 8px 44px !important;
    }

    .cuhv-hero h1,
    .ctfcu-score-hero h1 {
      font-size: clamp(1.9rem, 11vw, 2.8rem) !important;
      line-height: 1.02 !important;
    }

    .cuhv-actions,
    .ctfcu-overlay-actions {
      flex-direction: column;
      align-items: stretch;
    }

    .cuhv-button,
    .ctfcu-overlay-login,
    .ctfcu-overlay-note {
      width: 100%;
      justify-content: center;
      text-align: center;
    }

    .cuhv-hero-mini-grid,
    .ctfcu-score-summary,
    .ctfcu-score-status-grid,
    .ctfcu-podium,
    .ctfcu-user-awards-grid,
    .ctfcu-user-insights-grid,
    .ctfcu-user-evidence-grid,
    .ctfcu-user-stat-grid,
    .ctfcu-challenges-grid,
    .ctfcu-challenge-stat-grid,
    .ctfcu-modal-stat-grid {
      grid-template-columns: 1fr !important;
    }

    .ctfcu-user-stats {
      margin-left: 0 !important;
    }

    .cuhv-reveal {
      opacity: 1 !important;
      transform: none !important;
      transition: none !important;
    }
  }
</style>
<script id="ctfcu-responsive-safety-script">
(() => {
  function forceVisible() {
    document.querySelectorAll('.cuhv-reveal').forEach((node) => node.classList.add('is-visible'));
  }
  document.addEventListener('DOMContentLoaded', forceVisible);
  window.addEventListener('load', forceVisible);
  setTimeout(forceVisible, 1200);
})();
</script><!-- CTFCU_RESPONSIVE_SAFETY_END -->'''


def upsert(value, start, end, block):
    value = re.sub(re.escape(start) + r'.*?' + re.escape(end), '', str(value), flags=re.S).strip()
    return (value + '\n' if value else '') + block + '\n'


app = create_app()
with app.app_context():
    header = Configs.query.filter_by(key='theme_header').first()
    header.value = upsert(
        header.value,
        '<!-- CTFCU_RESPONSIVE_SAFETY_START -->',
        '<!-- CTFCU_RESPONSIVE_SAFETY_END -->',
        BLOCK,
    )
    db.session.commit()
    print('responsive safety synced')
PY

docker cp "$WORKDIR/apply_global_responsive_safety.py" "$CTFD_CONTAINER:/tmp/apply_global_responsive_safety.py"
docker exec -e PYTHONPATH=/opt/CTFd "$CTFD_CONTAINER" python3 /tmp/apply_global_responsive_safety.py
