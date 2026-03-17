#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
NAVBAR_SOURCE="${SCRIPT_DIR}/components/navbar.html"
if [[ ! -f "$NAVBAR_SOURCE" && -f "${SCRIPT_DIR}/navbar.html" ]]; then
  NAVBAR_SOURCE="${SCRIPT_DIR}/navbar.html"
fi
CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}
WORKDIR=/tmp/cuh_ctfd_navbar_experience
mkdir -p "$WORKDIR"
trap 'rm -rf "$WORKDIR"' EXIT

if [[ ! -f "$NAVBAR_SOURCE" ]]; then
  echo "Navbar component not found: $NAVBAR_SOURCE" >&2
  exit 1
fi

cat > "$WORKDIR/apply_navbar_experience.py" <<'PY'
import re
from CTFd import create_app
from CTFd.cache import clear_config, clear_pages
from CTFd.models import Configs, db

STYLE = r'''<!-- CTFCU_NAVBAR_EXPERIENCE_START --><style id="ctfcu-navbar-experience">
  :root {
    --ctfcu-nav-auth-top: #4a5561;
    --ctfcu-nav-auth-mid: #353c45;
    --ctfcu-nav-auth-bottom: #1f2328;
    --ctfcu-nav-guest-top: #55525b;
    --ctfcu-nav-guest-mid: #3e4048;
    --ctfcu-nav-guest-bottom: #282a30;
    --ctfcu-login-a: #46627f;
    --ctfcu-login-b: #7b92ac;
    --ctfcu-rank-a: rgba(70, 98, 127, 0.18);
    --ctfcu-rank-b: rgba(123, 146, 172, 0.18);
    --ctfcu-nav-line: rgba(172, 185, 198, 0.18);
    --ctfcu-nav-line-strong: rgba(198, 209, 220, 0.30);
    --ctfcu-nav-text: #eef1f3;
    --ctfcu-nav-text-soft: rgba(222, 229, 235, 0.76);
  }

  body {
    padding-top: 112px !important;
  }

  .navbar {
    overflow: visible !important;
    min-height: 100px !important;
    padding-top: 8px !important;
    padding-bottom: 8px !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 1030 !important;
    backdrop-filter: blur(18px) saturate(1.14);
    box-shadow:
      0 20px 44px rgba(0, 0, 0, 0.34),
      inset 0 -1px 0 rgba(255, 255, 255, 0.08) !important;
  }

  .navbar::before,
  .navbar::after {
    content: "" !important;
    position: absolute !important;
    pointer-events: none !important;
  }

  .navbar::before {
    inset: 0 !important;
    background:
      radial-gradient(circle at 12% 28%, rgba(70, 98, 127, 0.15), transparent 24%),
      radial-gradient(circle at 84% 18%, rgba(123, 146, 172, 0.12), transparent 20%),
      linear-gradient(90deg, rgba(28, 36, 46, 0.22), rgba(28, 36, 46, 0)) !important;
    opacity: 0.98 !important;
  }

  .navbar::after {
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    height: 3px !important;
    background: linear-gradient(90deg, rgba(70, 98, 127, 0.0), rgba(70, 98, 127, 0.82), rgba(123, 146, 172, 0.74), rgba(180, 194, 207, 0.44), rgba(70, 98, 127, 0.0)) !important;
    box-shadow: 0 0 20px rgba(70, 98, 127, 0.24) !important;
  }

  .navbar > * {
    position: relative !important;
    z-index: 1 !important;
  }

  .navbar.ctfcu-navbar-auth {
    background: linear-gradient(180deg, var(--ctfcu-nav-auth-top) 0%, var(--ctfcu-nav-auth-mid) 54%, var(--ctfcu-nav-auth-bottom) 100%) !important;
  }

  .navbar.ctfcu-navbar-guest {
    background: linear-gradient(180deg, var(--ctfcu-nav-guest-top) 0%, var(--ctfcu-nav-guest-mid) 54%, var(--ctfcu-nav-guest-bottom) 100%) !important;
  }

  .navbar > .container.ctfcu-navbar-shell {
    width: 100% !important;
    max-width: calc(100vw - 8px) !important;
    padding-left: clamp(18px, 1.9vw, 38px) !important;
    padding-right: clamp(18px, 1.9vw, 38px) !important;
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
  }

  .navbar-brand {
    flex: 0 0 auto !important;
    height: auto !important;
    margin-right: 0 !important;
    padding: 0 !important;
  }

  .ctfcu-brand-link {
    display: inline-flex !important;
    align-items: center !important;
    text-decoration: none !important;
  }

  .ctfcu-brand-frame {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-width: 0 !important;
    padding: 0 !important;
    border-radius: 0 !important;
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
    animation: ctfcuBrandFloat 7.2s ease-in-out infinite !important;
  }

  .ctfcu-brand-image {
    display: block !important;
    width: auto !important;
    height: 70px !important;
    max-width: min(8vw, 88px) !important;
    filter:
      drop-shadow(0 0 18px rgba(255, 255, 255, 0.18))
      drop-shadow(0 0 24px rgba(114, 244, 255, 0.16)) !important;
  }

  #base-navbars.ctfcu-navbar-panel {
    min-width: 0 !important;
    flex: 1 1 auto !important;
  }

  .navbar .navbar-nav {
    min-width: 0 !important;
    gap: 6px !important;
  }

  .navbar .ctfcu-navbar-links,
  .navbar .ctfcu-navbar-actions {
    display: flex !important;
    align-items: center !important;
  }

  .navbar .ctfcu-navbar-links {
    flex: 1 1 auto !important;
    justify-content: flex-start !important;
    flex-wrap: wrap !important;
    row-gap: 4px !important;
  }

  .navbar .ctfcu-navbar-actions {
    flex: 0 0 auto !important;
    min-width: 0 !important;
    justify-content: flex-end !important;
    gap: 6px !important;
    margin-left: auto !important;
  }

  .navbar .nav-item {
    margin-right: 0 !important;
  }

  .navbar .nav-link,
  .navbar .dropdown-toggle {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    gap: 8px !important;
    font-size: clamp(0.86rem, 0.18vw + 0.82rem, 0.94rem) !important;
    font-weight: 800 !important;
    letter-spacing: 0.01em !important;
    line-height: 1 !important;
    color: var(--ctfcu-nav-text) !important;
    padding: 8px 10px !important;
    min-height: 40px !important;
    border-radius: 14px !important;
    border: 1px solid rgba(182, 222, 255, 0.12) !important;
    background:
      linear-gradient(180deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.015)),
      rgba(6, 14, 28, 0.12) !important;
    box-shadow:
      0 14px 26px rgba(0, 0, 0, 0.16),
      inset 0 1px 0 rgba(255, 255, 255, 0.04) !important;
    white-space: nowrap !important;
    transition:
      transform 0.18s ease,
      border-color 0.18s ease,
      background 0.18s ease,
      box-shadow 0.18s ease !important;
  }

  .navbar .nav-link:hover,
  .navbar .nav-link:focus,
  .navbar .dropdown-toggle:hover,
  .navbar .dropdown-toggle:focus,
  .navbar .dropdown-toggle.show,
  .navbar .nav-item.show > .nav-link {
    transform: translateY(-3px) !important;
    border-color: rgba(114, 244, 255, 0.34) !important;
    background:
      linear-gradient(180deg, rgba(114, 244, 255, 0.14), rgba(114, 244, 255, 0.04)),
      rgba(10, 20, 38, 0.34) !important;
    box-shadow:
      0 18px 34px rgba(0, 0, 0, 0.24),
      0 0 0 1px rgba(114, 244, 255, 0.10),
      inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
  }

  .navbar .dropdown-toggle::after {
    display: none !important;
  }

  .ctfcu-nav-icon {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 26px !important;
    height: 26px !important;
    flex: 0 0 26px !important;
    border-radius: 9px !important;
    background:
      linear-gradient(180deg, rgba(114, 244, 255, 0.20), rgba(114, 244, 255, 0.06)),
      rgba(6, 16, 28, 0.44) !important;
    color: #ffffff !important;
    box-shadow:
      0 10px 22px rgba(0, 0, 0, 0.22),
      inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
    animation: ctfcuIconDrift 5.2s ease-in-out infinite !important;
  }

  .ctfcu-nav-icon i {
    font-size: 0.76rem !important;
  }

  .ctfcu-nav-icon-guias,
  .ctfcu-nav-icon-language,
  .ctfcu-nav-icon-theme {
    animation-delay: 0.55s !important;
  }

  .ctfcu-nav-icon-users,
  .ctfcu-nav-icon-scoreboard,
  .ctfcu-nav-icon-account {
    animation-delay: 1.1s !important;
  }

  .ctfcu-nav-icon-challenges,
  .ctfcu-nav-icon-login,
  .ctfcu-nav-icon-register,
  .ctfcu-nav-icon-mas {
    animation-delay: 1.65s !important;
  }

  .navbar .nav-link:hover .ctfcu-nav-icon,
  .navbar .nav-link:focus .ctfcu-nav-icon,
  .navbar .dropdown-toggle:hover .ctfcu-nav-icon,
  .navbar .dropdown-toggle:focus .ctfcu-nav-icon,
  .navbar .dropdown-toggle.show .ctfcu-nav-icon {
    transform: translateY(-2px) scale(1.08) rotate(6deg) !important;
  }

  .ctfcu-nav-text {
    display: inline-flex !important;
    align-items: center !important;
  }

  .ctfcu-challenges-link {
    position: relative !important;
    gap: 9px !important;
  }

  .ctfcu-nav-badge {
    position: relative !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-height: 20px !important;
    padding: 0 10px !important;
    border-radius: 999px !important;
    font-size: 0.58rem !important;
    font-weight: 900 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    white-space: nowrap !important;
    line-height: 1 !important;
  }

  .ctfcu-nav-badge-new {
    color: #f8f2eb !important;
    background: linear-gradient(135deg, rgba(143, 48, 65, 0.98), rgba(102, 119, 137, 0.96)) !important;
    box-shadow:
      0 8px 18px rgba(143, 48, 65, 0.24),
      0 0 0 1px rgba(241, 236, 228, 0.18),
      inset 0 1px 0 rgba(241, 236, 228, 0.20) !important;
    animation: ctfcuNewBadgePulse 2.3s ease-in-out infinite !important;
  }

  .ctfcu-nav-badge-new::before {
    content: "" !important;
    position: absolute !important;
    inset: -2px !important;
    border-radius: inherit !important;
    background: radial-gradient(circle, rgba(184, 169, 154, 0.26) 0, rgba(184, 169, 154, 0) 72%) !important;
    opacity: 0.8 !important;
    z-index: -1 !important;
    animation: ctfcuNewBadgeGlow 2.3s ease-in-out infinite !important;
  }

  @keyframes ctfcuNewBadgePulse {
    0%, 100% {
      transform: translateY(0) scale(1) !important;
    }
    50% {
      transform: translateY(-1px) scale(1.04) !important;
    }
  }

  @keyframes ctfcuNewBadgeGlow {
    0%, 100% {
      transform: scale(0.94) !important;
      opacity: 0.42 !important;
    }
    50% {
      transform: scale(1.08) !important;
      opacity: 0.82 !important;
    }
  }

  .ctfcu-nav-arrow {
    width: 11px !important;
    height: 11px !important;
    flex: 0 0 11px !important;
    margin-left: 2px !important;
    border-right: 2px solid currentColor !important;
    border-bottom: 2px solid currentColor !important;
    transform: rotate(45deg) translateY(-1px) !important;
    transform-origin: center !important;
    opacity: 0.72 !important;
    transition: transform 0.18s ease, opacity 0.18s ease !important;
  }

  .navbar .nav-item.show .ctfcu-nav-arrow,
  .navbar .dropdown-toggle.show .ctfcu-nav-arrow {
    transform: rotate(225deg) translateY(-1px) !important;
    opacity: 1 !important;
  }

  .navbar-toggler {
    align-items: center !important;
    justify-content: center !important;
    margin-left: auto !important;
    min-width: 50px !important;
    min-height: 40px !important;
    border-radius: 14px !important;
    border-color: rgba(177, 224, 255, 0.16) !important;
    background: rgba(8, 18, 34, 0.28) !important;
    box-shadow:
      0 10px 22px rgba(0, 0, 0, 0.18),
      inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
  }

  .navbar .dropdown-menu {
    position: absolute !important;
    top: calc(100% + 10px) !important;
    left: 0 !important;
    display: none;
    border-radius: 22px !important;
    border: 1px solid rgba(173, 216, 255, 0.20) !important;
    background:
      radial-gradient(circle at top left, rgba(114, 244, 255, 0.14), transparent 36%),
      linear-gradient(180deg, rgba(8, 18, 34, 0.98), rgba(6, 12, 24, 0.98)) !important;
    box-shadow:
      0 26px 56px rgba(0, 0, 0, 0.42),
      0 0 0 1px rgba(255, 255, 255, 0.04) !important;
    padding: 10px !important;
    min-width: 210px !important;
    margin-top: 0 !important;
    z-index: 1085 !important;
  }

  .navbar .dropdown-menu.show {
    display: block !important;
  }

  .navbar .dropdown-toggle.show + .dropdown-menu,
  .navbar .dropdown-toggle[aria-expanded="true"] + .dropdown-menu,
  .navbar .nav-item.show > .dropdown-menu,
  .navbar .dropdown.show > .dropdown-menu,
  .navbar .nav-item:focus-within > .dropdown-menu,
  .navbar .dropdown:focus-within > .dropdown-menu {
    display: block !important;
  }

  .navbar .dropdown-menu.dropdown-menu-end {
    left: auto !important;
    right: 0 !important;
  }

  .navbar .dropdown-item,
  .navbar .dropdown-item:visited {
    color: #eef6ff !important;
    border-radius: 16px !important;
    padding: 12px 14px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    white-space: normal !important;
    transition: transform 0.16s ease, background 0.16s ease !important;
  }

  .navbar .dropdown-item:hover,
  .navbar .dropdown-item:focus {
    background: rgba(114, 244, 255, 0.14) !important;
    color: #ffffff !important;
    transform: translateX(4px) !important;
  }

  .navbar .dropdown-divider {
    border-top-color: rgba(255, 255, 255, 0.10) !important;
  }

  .navbar .ctfcu-user-link {
    min-width: 236px !important;
    justify-content: flex-start !important;
    padding: 7px 10px !important;
    gap: 8px !important;
    background:
      radial-gradient(circle at 14% 18%, rgba(115, 255, 179, 0.18), transparent 26%),
      linear-gradient(180deg, rgba(14, 32, 62, 0.94), rgba(9, 20, 41, 0.94)) !important;
    border-color: rgba(115, 255, 179, 0.22) !important;
    box-shadow:
      0 18px 34px rgba(0, 0, 0, 0.22),
      0 0 28px rgba(115, 255, 179, 0.08) !important;
  }

  .ctfcu-login-item .ctfcu-login-link {
    color: #04131f !important;
    background: linear-gradient(135deg, var(--ctfcu-login-a), var(--ctfcu-login-b)) !important;
    border: 1px solid rgba(255, 255, 255, 0.26) !important;
    box-shadow:
      0 16px 32px rgba(114, 244, 255, 0.24),
      0 0 0 1px rgba(255, 255, 255, 0.08) !important;
    animation: ctfcuLoginPulse 2.8s ease-in-out infinite !important;
  }

  .ctfcu-login-item .ctfcu-login-link .ctfcu-nav-icon {
    background:
      linear-gradient(180deg, rgba(4, 19, 31, 0.20), rgba(4, 19, 31, 0.08)),
      rgba(255, 255, 255, 0.32) !important;
    color: #04131f !important;
  }

  .ctfcu-navbar-guest .ctfcu-register-link {
    border: 1px solid rgba(114, 244, 255, 0.22) !important;
    background:
      linear-gradient(180deg, rgba(114, 244, 255, 0.10), rgba(114, 244, 255, 0.03)),
      rgba(255, 255, 255, 0.03) !important;
  }

  .ctfcu-avatar-shell {
    position: relative !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 40px !important;
    height: 40px !important;
    flex: 0 0 40px !important;
    overflow: hidden !important;
    border-radius: 999px !important;
    background:
      radial-gradient(circle at 50% 32%, rgba(255, 255, 255, 0.22), transparent 42%),
      linear-gradient(180deg, rgba(114, 244, 255, 0.36), rgba(115, 255, 179, 0.14)) !important;
    border: 1px solid rgba(196, 236, 255, 0.22) !important;
    box-shadow:
      0 18px 34px rgba(0, 0, 0, 0.28),
      0 0 24px rgba(114, 244, 255, 0.16) !important;
  }

  .ctfcu-avatar-shell::after {
    content: "" !important;
    position: absolute !important;
    inset: -32% !important;
    background: conic-gradient(from 180deg, rgba(114, 244, 255, 0.0), rgba(114, 244, 255, 0.32), rgba(115, 255, 179, 0.0), rgba(114, 244, 255, 0.0)) !important;
    animation: ctfcuAvatarAura 4.8s linear infinite !important;
  }

  .ctfcu-user-avatar {
    position: relative !important;
    z-index: 1 !important;
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    object-position: 50% 60% !important;
    transform: scale(1.46) !important;
    border-radius: 999px !important;
  }

  .ctfcu-user-meta {
    display: flex !important;
    flex-direction: column !important;
    min-width: 0 !important;
    gap: 4px !important;
  }

  .ctfcu-user-label {
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.3rem !important;
    max-width: 14ch !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
    font-size: 0.9rem !important;
    font-weight: 800 !important;
  }

  .ctfcu-user-caption {
    font-size: 0.56rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: rgba(218, 240, 255, 0.66) !important;
  }

  .ctfcu-user-stats {
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    margin-left: auto !important;
  }

  .ctfcu-user-score,
  .ctfcu-user-rank {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-height: 24px !important;
    padding: 0 8px !important;
    border-radius: 999px !important;
    border: 1px solid rgba(177, 224, 255, 0.16) !important;
    font-size: 0.72rem !important;
    font-weight: 900 !important;
    line-height: 1 !important;
    white-space: nowrap !important;
    box-shadow: 0 10px 22px rgba(0, 0, 0, 0.18) !important;
  }

  .ctfcu-user-score {
    color: #03131f !important;
    background: linear-gradient(135deg, #7bf6ff, #7dffc7) !important;
    animation: ctfcuChipPulse 3s ease-in-out infinite !important;
  }

  .ctfcu-user-rank {
    color: #eff7ff !important;
    background: linear-gradient(180deg, rgba(30, 55, 97, 0.92), rgba(14, 27, 53, 0.96)) !important;
    animation: ctfcuRankGlow 3.6s ease-in-out infinite !important;
  }

  .ctfcu-account-menu > .nav-link,
  .ctfcu-language-item > .nav-link,
  .theme-switch {
    min-width: 0 !important;
  }

  .theme-switch:hover .ctfcu-nav-icon,
  .theme-switch:focus .ctfcu-nav-icon {
    transform: translateY(-2px) rotate(18deg) scale(1.08) !important;
  }

  .ctfcu-profile-mascot {
    display: flex !important;
    justify-content: center !important;
    margin: 0 auto 22px !important;
  }

  .ctfcu-profile-mascot-badge {
    position: relative !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 156px !important;
    height: 156px !important;
    border-radius: 999px !important;
    overflow: hidden !important;
    padding: 10px !important;
    background:
      radial-gradient(circle at 50% 18%, rgba(255, 255, 255, 0.28), transparent 30%),
      linear-gradient(180deg, rgba(17, 37, 71, 0.88), rgba(8, 18, 37, 0.94)) !important;
    border: 1px solid rgba(190, 232, 255, 0.22) !important;
    box-shadow:
      0 24px 44px rgba(0, 0, 0, 0.24),
      0 0 32px rgba(114, 244, 255, 0.16) !important;
    animation: ctfcuBrandFloat 7.2s ease-in-out infinite !important;
  }

  .ctfcu-profile-mascot-badge img,
  img.ctfcu-mascot-avatar {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    object-position: 50% 60% !important;
    border-radius: 999px !important;
  }

  .ctfcu-profile-mascot-badge img {
    transform: scale(1.48) !important;
  }

  img.ctfcu-mascot-avatar {
    transform: scale(1.22) !important;
  }

  @keyframes ctfcuBrandFloat {
    0%, 100% { transform: translateY(0); box-shadow: 0 24px 44px rgba(0, 0, 0, 0.32), 0 0 36px rgba(114, 244, 255, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.12); }
    50% { transform: translateY(-4px); box-shadow: 0 28px 48px rgba(0, 0, 0, 0.36), 0 0 40px rgba(114, 244, 255, 0.18), inset 0 1px 0 rgba(255, 255, 255, 0.14); }
  }

  @keyframes ctfcuIconDrift {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-2px) rotate(4deg); }
  }

  @keyframes ctfcuAvatarAura {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  @keyframes ctfcuLoginPulse {
    0%, 100% {
      box-shadow:
        0 16px 32px rgba(114, 244, 255, 0.20),
        0 0 0 1px rgba(255, 255, 255, 0.08);
    }
    50% {
      box-shadow:
        0 22px 40px rgba(114, 244, 255, 0.30),
        0 0 0 1px rgba(255, 255, 255, 0.14);
    }
  }

  @keyframes ctfcuChipPulse {
    0%, 100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-1px) scale(1.05); }
  }

  @keyframes ctfcuRankGlow {
    0%, 100% {
      box-shadow: 0 10px 22px rgba(0, 0, 0, 0.18);
      border-color: rgba(177, 224, 255, 0.16);
    }
    50% {
      box-shadow: 0 12px 28px rgba(114, 244, 255, 0.16);
      border-color: rgba(114, 244, 255, 0.30);
    }
  }

  @media (min-width: 992px) {
    .navbar-expand-lg .navbar-toggler {
      display: none !important;
    }

    .navbar-expand-lg .navbar-collapse.ctfcu-navbar-panel {
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      gap: 18px !important;
    }

    .navbar-expand-lg .navbar-nav {
      flex-direction: row !important;
      align-items: center !important;
    }

    .navbar-expand-lg .ctfcu-navbar-panel {
      margin-top: 0 !important;
      padding: 0 !important;
      border-top: 0 !important;
      background: transparent !important;
      border-radius: 0 !important;
      max-height: none !important;
      overflow: visible !important;
    }

    .navbar-expand-lg .ctfcu-account-menu .dropdown-menu,
    .navbar-expand-lg .ctfcu-language-item .dropdown-menu {
      right: 0 !important;
      left: auto !important;
    }
  }

  @media (max-width: 1399.98px) {
    body {
      padding-top: 104px !important;
    }

    .navbar {
      min-height: 94px !important;
    }

    .ctfcu-brand-image {
      height: 60px !important;
      max-width: min(8vw, 74px) !important;
    }

    .ctfcu-user-item .ctfcu-user-link {
      min-width: 220px !important;
    }
  }

  @media (max-width: 991.98px) {
    body {
      padding-top: 88px !important;
    }

    .navbar {
      min-height: 82px !important;
      padding-top: 7px !important;
      padding-bottom: 7px !important;
    }

    .navbar > .container.ctfcu-navbar-shell {
      flex-wrap: wrap !important;
      gap: 12px !important;
    }

    .ctfcu-brand-frame {
      min-width: 0 !important;
      padding: 0 !important;
      border-radius: 0 !important;
    }

    .ctfcu-brand-image {
      height: 52px !important;
      max-width: 62px !important;
    }

    .navbar-collapse.ctfcu-navbar-panel:not(.show) {
      display: none !important;
    }

    .navbar-collapse.ctfcu-navbar-panel.show,
    .navbar-collapse.ctfcu-navbar-panel.collapsing {
      display: flex !important;
      flex-direction: column !important;
      align-items: stretch !important;
    }

    .navbar-collapse.ctfcu-navbar-panel.collapsing {
      height: auto !important;
      overflow: hidden !important;
    }

    #base-navbars.ctfcu-navbar-panel {
      width: 100% !important;
      flex-basis: 100% !important;
      margin-top: 6px !important;
      padding: 10px 0 4px !important;
      border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
      background: linear-gradient(180deg, rgba(8, 16, 31, 0.96), rgba(8, 16, 31, 0.90)) !important;
      border-radius: 18px !important;
      max-height: calc(100vh - 96px) !important;
      overflow-y: auto !important;
      overflow-x: hidden !important;
    }

    .navbar .navbar-nav,
    .navbar .ctfcu-navbar-links,
    .navbar .ctfcu-navbar-actions,
    .navbar .ms-md-auto,
    .navbar .ctfcu-navbar-user {
      width: 100% !important;
      flex-direction: column !important;
      align-items: stretch !important;
    }

    .navbar .nav-item {
      width: 100% !important;
    }

    .navbar .nav-link,
    .navbar .dropdown-toggle {
      display: flex !important;
      width: 100% !important;
      justify-content: flex-start !important;
      font-size: 0.9rem !important;
      padding: 9px 10px !important;
      min-height: 42px !important;
      white-space: normal !important;
    }

    .ctfcu-challenges-link {
      flex-wrap: wrap !important;
      row-gap: 6px !important;
    }

    .ctfcu-nav-badge {
      margin-left: 34px !important;
    }

    .navbar .dropdown-menu {
      position: static !important;
      inset: auto !important;
      transform: none !important;
      float: none !important;
      width: 100% !important;
      min-width: 0 !important;
      margin-top: 6px !important;
    }

    .ctfcu-user-item .ctfcu-user-link {
      min-width: 0 !important;
      flex-wrap: wrap !important;
      row-gap: 6px !important;
    }

    .ctfcu-user-stats {
      width: 100% !important;
      margin-left: 0 !important;
      gap: 8px !important;
    }
  }

  @media (max-width: 575.98px) {
    body {
      padding-top: 80px !important;
    }

    .navbar > .container.ctfcu-navbar-shell {
      max-width: calc(100vw - 10px) !important;
      padding-left: 10px !important;
      padding-right: 10px !important;
    }

    .ctfcu-brand-image {
      height: 44px !important;
      max-width: 52px !important;
    }

    .ctfcu-nav-icon {
      width: 24px !important;
      height: 24px !important;
      flex-basis: 24px !important;
    }

    .ctfcu-avatar-shell {
      width: 36px !important;
      height: 36px !important;
      flex-basis: 36px !important;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .ctfcu-brand-frame,
    .ctfcu-nav-icon,
    .ctfcu-avatar-shell::after,
    .ctfcu-profile-mascot-badge,
    .ctfcu-login-item .ctfcu-login-link,
    .ctfcu-user-score,
    .ctfcu-user-rank {
      animation: none !important;
    }
  }
  .navbar,
  .navbar.ctfcu-navbar-auth,
  .navbar.ctfcu-navbar-guest {
    box-shadow:
      0 20px 44px rgba(18, 12, 10, 0.24),
      inset 0 -1px 0 rgba(255, 245, 232, 0.05) !important;
  }

  .navbar::before {
    background:
      radial-gradient(circle at 12% 28%, rgba(79, 101, 125, 0.14), transparent 24%),
      radial-gradient(circle at 84% 18%, rgba(127, 147, 168, 0.12), transparent 20%),
      linear-gradient(90deg, rgba(52, 57, 64, 0.20), rgba(52, 57, 64, 0)) !important;
  }

  .navbar::after {
    height: 2px !important;
    background: linear-gradient(90deg, rgba(183, 197, 211, 0), rgba(183, 197, 211, 0.72), rgba(79, 101, 125, 0.64), rgba(127, 147, 168, 0.58), rgba(183, 197, 211, 0)) !important;
    box-shadow: 0 0 14px rgba(79, 101, 125, 0.18) !important;
  }

  .navbar .nav-link,
  .navbar .dropdown-toggle,
  .navbar-toggler,
  .navbar .dropdown-menu,
  .ctfcu-user-link,
  .ctfcu-login-link,
  .ctfcu-user-score,
  .ctfcu-user-rank {
    border-color: rgba(194, 173, 145, 0.14) !important;
  }

  .navbar .nav-link,
  .navbar .dropdown-toggle {
    background:
      linear-gradient(180deg, rgba(255, 248, 240, 0.04), rgba(255, 248, 240, 0.012)),
      rgba(53, 41, 34, 0.22) !important;
    box-shadow:
      0 14px 26px rgba(18, 12, 10, 0.14),
      inset 0 1px 0 rgba(255, 248, 240, 0.04) !important;
  }

  .navbar .nav-link:hover,
  .navbar .nav-link:focus,
  .navbar .dropdown-toggle:hover,
  .navbar .dropdown-toggle:focus,
  .navbar .dropdown-toggle.show,
  .navbar .nav-item.show > .nav-link {
    border-color: rgba(195, 163, 110, 0.28) !important;
    background:
      linear-gradient(180deg, rgba(79, 101, 125, 0.14), rgba(127, 147, 168, 0.07)),
      rgba(68, 76, 86, 0.42) !important;
    box-shadow:
      0 18px 34px rgba(18, 12, 10, 0.18),
      0 0 0 1px rgba(195, 163, 110, 0.08),
      inset 0 1px 0 rgba(255, 248, 240, 0.06) !important;
  }

  .ctfcu-nav-icon {
    background:
      linear-gradient(180deg, rgba(79, 101, 125, 0.18), rgba(127, 147, 168, 0.08)),
      rgba(58, 63, 72, 0.44) !important;
    box-shadow:
      0 10px 22px rgba(18, 12, 10, 0.2),
      inset 0 1px 0 rgba(255, 248, 240, 0.10) !important;
  }

  .ctfcu-nav-badge-new {
    color: #231711 !important;
    background: linear-gradient(135deg, rgba(79, 101, 125, 0.98), rgba(127, 147, 168, 0.96)) !important;
    box-shadow:
      0 8px 18px rgba(79, 101, 125, 0.18),
      0 0 0 1px rgba(255, 245, 232, 0.12),
      inset 0 1px 0 rgba(255, 245, 232, 0.28) !important;
  }

  .ctfcu-nav-badge-new::before {
    background: radial-gradient(circle, rgba(184, 169, 154, 0.26) 0, rgba(184, 169, 154, 0) 72%) !important;
  }

  .navbar .dropdown-menu {
    background:
      radial-gradient(circle at top left, rgba(143, 48, 65, 0.12), transparent 36%),
      linear-gradient(180deg, rgba(68, 76, 86, 0.98), rgba(31, 35, 40, 0.98)) !important;
    box-shadow:
      0 26px 56px rgba(16, 18, 22, 0.32),
      0 0 0 1px rgba(241, 236, 228, 0.03) !important;
  }

  .navbar .dropdown-item:hover,
  .navbar .dropdown-item:focus {
    background: rgba(79, 101, 125, 0.14) !important;
    color: #f8f2eb !important;
  }
</style><script id="ctfcu-navbar-experience-script">
(() => {
  let raf = 0;
  const dropdownSelector = ".navbar .dropdown-toggle[data-bs-toggle='dropdown']";

  function resolveDropdownParts(toggle) {
    const item = toggle ? toggle.closest(".dropdown, .nav-item") : null;
    const menu = item
      ? Array.from(item.children).find((child) => child.classList && child.classList.contains("dropdown-menu"))
      : null;
    return { item, menu };
  }

  function closeNavbarMenus(exceptItem = null) {
    document.querySelectorAll(".navbar .dropdown.show, .navbar .nav-item.show").forEach((node) => {
      if (node !== exceptItem) node.classList.remove("show");
    });
    document.querySelectorAll(".navbar .dropdown-menu.show").forEach((node) => {
      if (!exceptItem || !exceptItem.contains(node)) node.classList.remove("show");
    });
    document.querySelectorAll(dropdownSelector).forEach((node) => {
      if (!exceptItem || node.closest(".dropdown, .nav-item") !== exceptItem) {
        node.setAttribute("aria-expanded", "false");
      }
    });
  }

  function toggleNavbarMenu(toggle) {
    const { item, menu } = resolveDropdownParts(toggle);
    if (!item || !menu) return;
    const willOpen = !menu.classList.contains("show");
    closeNavbarMenus(item);
    item.classList.toggle("show", willOpen);
    menu.classList.toggle("show", willOpen);
    toggle.classList.toggle("show", willOpen);
    toggle.setAttribute("aria-expanded", willOpen ? "true" : "false");
  }

  function getMascotSrc() {
    const brand = document.querySelector(".ctfcu-brand-image, .navbar-brand img");
    return brand ? (brand.currentSrc || brand.src || "") : "";
  }

  function injectProfileMascot(src) {
    const path = window.location.pathname || "";
    const isProfile = /^\/(?:users|teams)(?:\/|$)/.test(path);
    if (!isProfile) return;

    document.querySelectorAll(".jumbotron .container").forEach((container) => {
      const title = container.querySelector(":scope > h1");
      if (!title || container.querySelector(".ctfcu-profile-mascot")) return;
      const hero = document.createElement("div");
      hero.className = "ctfcu-profile-mascot";
      hero.innerHTML = '<span class="ctfcu-profile-mascot-badge"><img src="' + src + '" alt="Tigrillo mascota del hackatón"></span>';
      container.insertBefore(hero, title);
    });
  }

  function replaceGenericAvatars(src) {
    document.querySelectorAll('img[src*="gravatar"], img[src*="avatar"], img[src*="identicon"]').forEach((img) => {
      if (img.closest(".ctfcu-brand-frame")) return;
      if (img.dataset.ctfcuMascotApplied === "1") return;
      img.src = src;
      img.removeAttribute("srcset");
      img.classList.add("ctfcu-mascot-avatar");
      img.dataset.ctfcuMascotApplied = "1";
      if (!img.alt) img.alt = "Tigrillo mascota";
    });
  }

  function applyMascotBranding() {
    const src = getMascotSrc();
    if (!src) return;
    injectProfileMascot(src);
    replaceGenericAvatars(src);
  }

  function scheduleApply() {
    if (raf) return;
    raf = window.requestAnimationFrame(() => {
      raf = 0;
      applyMascotBranding();
    });
  }

  document.addEventListener("click", (event) => {
    const toggle = event.target.closest(dropdownSelector);
    if (toggle) {
      event.preventDefault();
      event.stopPropagation();
      toggleNavbarMenu(toggle);
      return;
    }

    if (!event.target.closest(".navbar .dropdown-menu")) {
      closeNavbarMenus();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeNavbarMenus();
    }
  });

  document.addEventListener("DOMContentLoaded", scheduleApply);
  if (document.body) {
    new MutationObserver(scheduleApply).observe(document.body, { childList: true, subtree: true });
  } else {
    window.addEventListener("load", scheduleApply, { once: true });
  }
})();
</script><!-- CTFCU_NAVBAR_EXPERIENCE_END -->'''


def upsert(value, start, end, block):
    value = re.sub(re.escape(start) + r'.*?' + re.escape(end), '', str(value), flags=re.S).strip()
    return (value + '\n' if value else '') + block + '\n'


def strip_legacy_navbar(value):
    value = str(value)
    # Old header package that keeps forcing the navbar into a single row.
    value = re.sub(r'<style id="ctf-cuheader-pro">.*?</style>\s*', '', value, flags=re.S)
    value = re.sub(r'<style id="ctfcu-modal-offset-fix">.*?</style>\s*', '', value, flags=re.S)
    return value.strip()


app = create_app()
with app.app_context():
    header = Configs.query.filter_by(key='theme_header').first()
    header.value = strip_legacy_navbar(header.value)
    header.value = upsert(
        header.value,
        '<!-- CTFCU_NAVBAR_EXPERIENCE_START -->',
        '<!-- CTFCU_NAVBAR_EXPERIENCE_END -->',
        STYLE,
    )
    db.session.commit()
    clear_config()
    clear_pages()
    print('navbar experience synced')
PY

docker cp "$WORKDIR/apply_navbar_experience.py" "$CTFD_CONTAINER:/tmp/apply_navbar_experience.py"
docker cp "$NAVBAR_SOURCE" "$CTFD_CONTAINER:/tmp/navbar.html"

for target in \
  /opt/CTFd/CTFd/themes/core/templates/components/navbar.html \
  /opt/CTFd/CTFd/themes/core-beta/templates/components/navbar.html
do
  if docker exec "$CTFD_CONTAINER" sh -lc "[ -f '$target' ]"; then
    docker cp "$NAVBAR_SOURCE" "$CTFD_CONTAINER:$target"
  fi
done

docker exec -e PYTHONPATH=/opt/CTFd "$CTFD_CONTAINER" python3 /tmp/apply_navbar_experience.py
