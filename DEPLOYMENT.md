# Quick Setup Guide for Production Deployment

This guide will help you deploy the FastAPI application with SSL on api.albert-bet.ru

## Prerequisites

- A server with Docker and Docker Compose installed
- Domain `api.albert-bet.ru` pointing to your server's IP address
- Ports 80 and 443 open and accessible from the internet

## Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nightmarest/fastapi-idk.git
   cd fastapi-idk
   ```

2. **Configure email for Let's Encrypt (optional)**
   ```bash
   export CERTBOT_EMAIL=your-email@example.com
   ```
   
   If not set, it defaults to `admin@albert-bet.ru`

3. **Start the services**
   ```bash
   docker compose up --build -d
   ```

4. **Initialize SSL certificate**
   ```bash
   chmod +x init-letsencrypt.sh
   ./init-letsencrypt.sh
   ```
   
   Follow the prompts. The script will:
   - Request an SSL certificate from Let's Encrypt
   - Configure nginx to use HTTPS
   - Set up automatic certificate renewal

5. **Verify the deployment**
   ```bash
   curl https://api.albert-bet.ru
   ```
   
   You should receive a welcome message.

6. **Access the API documentation**
   
   Open in your browser: https://api.albert-bet.ru/docs

## Testing Before Production

To test the setup without affecting Let's Encrypt rate limits:

```bash
STAGING=1 ./init-letsencrypt.sh
```

This uses Let's Encrypt's staging server, which issues certificates that browsers won't trust but are useful for testing.

## Monitoring

Check service status:
```bash
docker compose ps
```

View logs:
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f nginx
docker compose logs -f web
docker compose logs -f certbot
```

## Updating the Application

1. Pull the latest changes:
   ```bash
   git pull
   ```

2. Rebuild and restart:
   ```bash
   docker compose up --build -d
   ```

SSL certificates will be preserved across updates.

## Security Reminders

- [ ] Change the JWT_SECRET in production (set as environment variable)
- [ ] Review and adjust rate limiting in nginx.conf if needed
- [ ] Set up firewall rules to allow only ports 22, 80, and 443
- [ ] Regularly update Docker images for security patches
- [ ] Monitor certificate renewal in logs

## Support

For issues, check the main README.md file or open an issue on GitHub.
