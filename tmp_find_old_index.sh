#!/usr/bin/env sh
set -eu
grep -R -n "color: #d2b889" /opt /tmp 2>/dev/null | head -n 20 || true
grep -R -n "rgba(222, 210, 193, 0.82)" /opt /tmp 2>/dev/null | head -n 20 || true
