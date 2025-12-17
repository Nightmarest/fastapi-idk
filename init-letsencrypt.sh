#!/bin/bash

# This script initializes Let's Encrypt SSL certificates using certbot

set -e

DOMAIN="api.albert-bet.ru"
EMAIL="${CERTBOT_EMAIL:-admin@albert-bet.ru}"  # Set your email or use environment variable
STAGING="${STAGING:-0}"  # Set to 1 to use Let's Encrypt staging server for testing
DATA_PATH="./certbot"

echo "================================================"
echo "SSL Certificate Initialization for $DOMAIN"
echo "================================================"

# Create directories
mkdir -p "$DATA_PATH/conf/live/$DOMAIN"
mkdir -p "$DATA_PATH/www"

# Check if certificate already exists
if [ -f "$DATA_PATH/conf/live/$DOMAIN/fullchain.pem" ]; then
    echo "✓ Certificate already exists for $DOMAIN"
    echo "To renew, remove the certificate directory and run this script again."
    read -p "Do you want to continue and request a new certificate? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Exiting..."
        exit 0
    fi
fi

# Determine if we should use staging server
STAGING_ARG=""
if [ "$STAGING" = "1" ]; then
    STAGING_ARG="--staging"
    echo "⚠ Using Let's Encrypt staging server (for testing)"
else
    echo "Using Let's Encrypt production server"
fi

echo ""
echo "Domain: $DOMAIN"
echo "Email: $EMAIL"
echo ""
read -p "Proceed with certificate request? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "Starting services..."
docker compose up -d nginx

echo "Waiting for nginx to be ready..."
sleep 5

echo "Requesting Let's Encrypt certificate for $DOMAIN..."
docker compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email "$EMAIL" \
    --agree-tos \
    --no-eff-email \
    $STAGING_ARG \
    -d "$DOMAIN"

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Certificate obtained successfully!"
    echo ""
    echo "Now updating nginx to use SSL configuration..."
    
    # Update docker-compose to use SSL nginx config
    docker compose exec nginx cp /etc/nginx/nginx.conf.full /etc/nginx/nginx.conf || echo "Manual configuration switch needed"
    
    echo "Reloading nginx..."
    docker compose exec nginx nginx -s reload
    
    echo ""
    echo "================================================"
    echo "✓ SSL Certificate Setup Complete!"
    echo "================================================"
    echo ""
    echo "Your API is now accessible at: https://$DOMAIN"
    echo ""
    echo "Certificate auto-renewal is configured and will run every 12 hours."
    echo ""
else
    echo ""
    echo "✗ Failed to obtain certificate."
    echo "Please check:"
    echo "  1. DNS is properly configured for $DOMAIN"
    echo "  2. Port 80 is accessible from the internet"
    echo "  3. The domain points to this server's IP address"
    exit 1
fi
