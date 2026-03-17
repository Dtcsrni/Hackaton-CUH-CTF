#!/usr/bin/env bash
set -euo pipefail

TS=$(date +%Y%m%d%H%M%S)
BACKUP_DIR=/opt/cuh-ctf/artifacts/backups/https_ip_$TS
mkdir -p "$BACKUP_DIR"

cp /opt/ctfd/docker-compose.yml "$BACKUP_DIR/docker-compose.yml.bak"
[ -f /etc/nginx/sites-available/ctfd-ip.conf ] && cp /etc/nginx/sites-available/ctfd-ip.conf "$BACKUP_DIR/ctfd-ip.conf.bak" || true
[ -f /etc/systemd/system/cuh-certbot-ip-renew.service ] && cp /etc/systemd/system/cuh-certbot-ip-renew.service "$BACKUP_DIR/cuh-certbot-ip-renew.service.bak" || true
[ -f /etc/systemd/system/cuh-certbot-ip-renew.timer ] && cp /etc/systemd/system/cuh-certbot-ip-renew.timer "$BACKUP_DIR/cuh-certbot-ip-renew.timer.bak" || true

python3 - <<'PY'
from pathlib import Path
p = Path('/opt/ctfd/docker-compose.yml')
text = p.read_text(encoding='utf-8')
text = text.replace('REVERSE_PROXY: "false"', 'REVERSE_PROXY: "true"')
p.write_text(text, encoding='utf-8')
print('docker-compose updated')
PY

cd /opt/ctfd
docker compose up -d ctfd

systemctl stop nginx || true
certbot certonly \
  --standalone \
  --non-interactive \
  --agree-tos \
  --register-unsafely-without-email \
  --preferred-challenges http \
  --preferred-profile shortlived \
  --ip-address 45.55.49.111 \
  --cert-name ctfd-ip

cat > /etc/nginx/conf.d/cuh-upgrade-map.conf <<'EOF'
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}
EOF

cat > /etc/nginx/sites-available/ctfd-ip.conf <<'EOF'
server {
    listen 80;
    listen [::]:80;
    server_name 45.55.49.111;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name 45.55.49.111;

    ssl_certificate /etc/letsencrypt/live/ctfd-ip/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ctfd-ip/privkey.pem;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:10m;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    client_max_body_size 64m;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port 443;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_buffering off;
    }
}
EOF

rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/ctfd-ip.conf /etc/nginx/sites-enabled/ctfd-ip.conf
nginx -t
systemctl enable --now nginx

cat > /opt/cuh-ctf/scripts/renovar_https_ip.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
trap 'systemctl start nginx >/dev/null 2>&1 || true' EXIT
systemctl stop nginx
certbot renew --cert-name ctfd-ip --preferred-profile shortlived -q
systemctl start nginx
EOF
chmod +x /opt/cuh-ctf/scripts/renovar_https_ip.sh

cat > /etc/systemd/system/cuh-certbot-ip-renew.service <<'EOF'
[Unit]
Description=Renovacion HTTPS IP para CTFd
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/opt/cuh-ctf/scripts/renovar_https_ip.sh
EOF

cat > /etc/systemd/system/cuh-certbot-ip-renew.timer <<'EOF'
[Unit]
Description=Ejecucion periodica de renovacion HTTPS IP para CTFd

[Timer]
OnBootSec=15m
OnUnitActiveSec=12h
Persistent=true

[Install]
WantedBy=timers.target
EOF

systemctl daemon-reload
systemctl enable --now cuh-certbot-ip-renew.timer

curl -k -I https://45.55.49.111 | sed -n '1,20p'
openssl s_client -connect 45.55.49.111:443 -servername 45.55.49.111 </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates -ext subjectAltName
