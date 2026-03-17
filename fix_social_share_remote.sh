#!/usr/bin/env bash
set -euo pipefail

CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}
WORKDIR=/tmp/cuh_ctfd_social_fix
mkdir -p "$WORKDIR"
trap 'rm -rf "$WORKDIR"' EXIT

cat > "$WORKDIR/apply_social_fix.py" <<'PY'
from CTFd import create_app
from CTFd.models import Configs, db

FIX_BLOCK = """
<style id="ctfcu-social-share-fix">
  .ctfcu-share-note {
    margin-top: 0.55rem;
    font-size: 0.85rem;
    line-height: 1.45;
    color: rgba(255, 255, 255, 0.84);
  }

  .ctfcu-native-share {
    border-left: 0 !important;
  }
</style>
<script id="ctfcu-social-share-fix-script">
(() => {
  function isIpv4Host(hostname) {
    return /^\\d{1,3}(?:\\.\\d{1,3}){3}$/.test(hostname || "");
  }

  function decodeShareUrl(anchor) {
    if (!anchor) {
      return "";
    }
    try {
      const href = anchor.getAttribute("href") || "";
      const parsed = new URL(href, window.location.origin);
      return parsed.searchParams.get("url") || "";
    } catch (error) {
      return "";
    }
  }

  function copyText(text) {
    if (!text) {
      return;
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).catch(() => {});
      return;
    }
    const input = document.createElement("textarea");
    input.value = text;
    input.setAttribute("readonly", "readonly");
    input.style.position = "absolute";
    input.style.left = "-9999px";
    document.body.appendChild(input);
    input.select();
    try {
      document.execCommand("copy");
    } catch (error) {
      console.warn("No se pudo copiar el enlace de compartir", error);
    }
    document.body.removeChild(input);
  }

  function createButton(className, title, iconClass, handler) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "btn btn-sm btn-outline-secondary " + className;
    button.title = title;
    button.innerHTML = `<i class="${iconClass}"></i>`;
    button.addEventListener("click", handler);
    return button;
  }

  function enhanceShareGroup(group) {
    if (!group || group.dataset.ctfcuShareEnhanced === "1") {
      return;
    }

    const twitter = group.querySelector('a[href*="twitter.com/intent/tweet"]');
    const facebook = group.querySelector('a[href*="facebook.com/sharer"]');
    const linkedin = group.querySelector('a[href*="linkedin.com/shareArticle"]');

    if (!twitter && !facebook && !linkedin) {
      return;
    }

    const shareUrl = decodeURIComponent(decodeShareUrl(twitter || facebook || linkedin));
    const limitedPreviewEnv = window.location.protocol !== "https:" || isIpv4Host(window.location.hostname);

    if (limitedPreviewEnv) {
      [facebook, linkedin].forEach((link) => {
        if (link) {
          link.style.display = "none";
          link.setAttribute("aria-hidden", "true");
          link.setAttribute("tabindex", "-1");
        }
      });

      if (twitter && shareUrl) {
        twitter.href = "https://twitter.com/intent/tweet?text=" +
          encodeURIComponent("Reto resuelto en el laboratorio CTF CUH") +
          "&url=" + encodeURIComponent(shareUrl);
        twitter.title = "Compartir en X";
      }

      if (!group.querySelector(".ctfcu-web-share")) {
        const shareButton = createButton(
          "ctfcu-web-share ctfcu-native-share",
          "Compartir enlace",
          "fa-solid fa-share-nodes",
          async () => {
            if (!shareUrl) {
              return;
            }
            if (navigator.share) {
              try {
                await navigator.share({
                  title: document.title || "CTF CUH",
                  text: "Reto resuelto en el laboratorio CTF CUH",
                  url: shareUrl,
                });
                return;
              } catch (error) {
                if (error && error.name === "AbortError") {
                  return;
                }
              }
            }
            copyText(shareUrl);
          }
        );
        group.appendChild(shareButton);
      }

      const parent = group.parentElement || group.closest("div");
      if (parent && !parent.querySelector(".ctfcu-share-note")) {
        const note = document.createElement("div");
        note.className = "ctfcu-share-note";
        note.textContent = "En esta instancia de laboratorio, Facebook y LinkedIn no generan una vista previa fiable con enlaces HTTP sobre IP pública. Usa copiar enlace, compartir desde el navegador o X.";
        parent.appendChild(note);
      }
    }

    group.dataset.ctfcuShareEnhanced = "1";
  }

  function scanShareGroups() {
    document.querySelectorAll(".challenge-window .btn-group, .alert .btn-group").forEach(enhanceShareGroup);
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

  document.addEventListener("DOMContentLoaded", scanShareGroups);
  observeBodyReady(scanShareGroups);
})();
</script>
"""

app = create_app()
with app.app_context():
    footer = Configs.query.filter_by(key="theme_footer").first()
    if footer is None:
        raise SystemExit("No existe theme_footer en Configs")

    value = str(footer.value)
    if "ctfcu-social-share-fix-script" in value:
        print("social share fix already present")
    else:
        footer.value = value + FIX_BLOCK
        db.session.commit()
        print("social share fix applied")
PY

docker cp "$WORKDIR/apply_social_fix.py" "$CTFD_CONTAINER:/tmp/apply_social_fix.py"
docker exec -e PYTHONPATH=/opt/CTFd "$CTFD_CONTAINER" python3 /tmp/apply_social_fix.py
