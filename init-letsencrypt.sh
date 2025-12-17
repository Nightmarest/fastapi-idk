#!/usr/bin/env bash
set -euo pipefail

DOMAIN="api.albert-bet.ru"
EMAIL="admin@albert-bet.ru"
COMPOSE="docker compose"   # замените на 'docker-compose' если у вас старая версия
NGINX_SERVICE="nginx"
CERTBOT_SERVICE="certbot"

echo "================================================"
echo "SSL Certificate Initialization for ${DOMAIN}"
echo "================================================"
echo "Using Let's Encrypt production server"
echo
echo "Domain: ${DOMAIN}"
echo "Email: ${EMAIL}"
echo

read -r -p "Proceed with certificate request? (y/N) " decision
if [[ "${decision:-N}" != "y" && "${decision:-N}" != "Y" ]]; then
  echo "Aborted."
  exit 1
fi

# Подготовка директорий для webroot и конфигурации (согласовано с docker-compose.yml)
mkdir -p ./certbot/www
mkdir -p ./certbot/conf

echo
echo "Starting services..."
${COMPOSE} up -d ${NGINX_SERVICE}

echo
echo "Waiting for nginx to be ready..."
# ждём пока nginx поднимется и слушает 80 порт
for i in {1..30}; do
  if ${COMPOSE} exec -T ${NGINX_SERVICE} sh -c "nc -z -w1 127.0.0.1 80" >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

echo "Requesting Let's Encrypt certificate for ${DOMAIN}..."

# ПЕРВИЧНАЯ ВЫДАЧА: переопределяем entrypoint, явно запускаем 'certbot certonly'
${COMPOSE} run --rm --entrypoint "" ${CERTBOT_SERVICE} \
  certbot certonly \
  --webroot -w /var/www/certbot \
  -d "${DOMAIN}" \
  --email "${EMAIL}" \
  --agree-tos \
  --no-eff-email \
  --non-interactive \
  --rsa-key-size 4096 \
  --server https://acme-v02.api.letsencrypt.org/directory

echo
echo "Reloading nginx..."
${COMPOSE} exec -T ${NGINX_SERVICE} nginx -s reload

echo
echo "Done. Certificates should be in ./certbot/conf/live/${DOMAIN}/"
