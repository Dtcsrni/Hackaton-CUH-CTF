#!/usr/bin/env bash
set -euo pipefail
tmpfile=$(mktemp)
trap 'rm -f "$tmpfile"' EXIT
curl -fsS -o "$tmpfile" http://127.0.0.1:8000/
grep -Fq "CUH{el_codigo_fuente_tambien_orienta}" "$tmpfile"
echo "Validacion de Fuente principal: OK"
