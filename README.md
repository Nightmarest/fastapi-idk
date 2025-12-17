# FastAPI Backend with SQLite

A simple FastAPI backend with user registration, authentication (JWT), and review system.

## Features

- User registration with email, password, and name (returns JWT token immediately)
- JWT Bearer authentication for login
- User profile endpoints (GET and PATCH)
- Casino management system (create and list casinos)
- Review system with stars (1-5) and comments for casinos
- Each user can only submit one review per casino
- SQLite database with persistent volume
- Docker containerization
- Nginx reverse proxy with SSL/TLS support
- Automatic SSL certificate generation via Let's Encrypt

## Requirements

- Docker
- Docker Compose
- Domain name pointing to your server (for SSL certificate)

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application and endpoints
│   ├── database.py       # Database configuration
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── security.py       # JWT and password handling
│   ├── deps.py           # Dependency injection
│   └── crud.py           # Database operations
├── nginx/
│   ├── nginx.conf        # Nginx configuration with SSL
│   └── nginx-init.conf   # Initial Nginx configuration (HTTP only)
├── scripts/
│   └── certbot-renew.sh  # Certbot auto-renewal script
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── init-letsencrypt.sh   # SSL certificate initialization script
├── DEPLOYMENT.md         # Detailed production deployment guide
└── README.md
```

## Running the Application

### Local Development (without SSL)

1. Clone the repository:
```bash
git clone https://github.com/Nightmarest/fastapi-idk.git
cd fastapi-idk
```

2. Start the application with Docker Compose:
```bash
docker compose up --build
```

3. The API will be available at `http://localhost:8000`

4. Access the interactive API documentation (Swagger UI) at `http://localhost:8000/docs`

### Production Deployment (with SSL)

1. Clone the repository on your server:
```bash
git clone https://github.com/Nightmarest/fastapi-idk.git
cd fastapi-idk
```

2. Make sure your domain `api.albert-bet.ru` points to your server's IP address.

3. (Optional) Set your email for Let's Encrypt notifications:
```bash
export CERTBOT_EMAIL=your-email@example.com
```

4. Build and start the application:
```bash
docker compose up --build -d
```

5. Initialize SSL certificate:
```bash
./init-letsencrypt.sh
```

This script will:
- Request an SSL certificate from Let's Encrypt for `api.albert-bet.ru`
- Configure nginx to use the certificate
- Set up automatic certificate renewal every 12 hours

6. Your API will be available at `https://api.albert-bet.ru`

7. Access the interactive API documentation at `https://api.albert-bet.ru/docs`

**Note:** For testing purposes, you can use Let's Encrypt staging server to avoid rate limits:
```bash
STAGING=1 ./init-letsencrypt.sh
```

## API Endpoints

### Root
- `GET /` - Welcome message

### Authentication
- `POST /register` - Register a new user
- `POST /login` - Login and get JWT token

### User Profile
- `GET /users/me` - Get current user profile (requires authentication)
- `PATCH /users/me` - Update user name (requires authentication)

### Casinos
- `POST /casinos` - Create a new casino
- `GET /casinos` - Get all casinos (supports pagination)

### Reviews
- `POST /reviews` - Create a review for a casino (requires authentication)
- `GET /reviews` - Get all reviews (supports filtering by casino_id and pagination)

## Usage Examples

**Note:** Replace `https://api.albert-bet.ru` with `http://localhost:8000` if running locally without SSL.

### 1. Register a new user

```bash
curl -X POST "https://api.albert-bet.ru/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "name": "John Doe"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe"
}
```

**Note:** Registration now returns a JWT token immediately, so you can use the account right away without a separate login.

### 2. Login

```bash
curl -X POST "https://api.albert-bet.ru/login?email=user@example.com&password=securepassword123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Save the `access_token` for authenticated requests.

### 3. Get current user profile

```bash
curl -X GET "https://api.albert-bet.ru/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe"
}
```

### 4. Update user name

```bash
curl -X PATCH "https://api.albert-bet.ru/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe"
  }'
```

Response:
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "Jane Doe"
}
```

### 5. Create a casino

```bash
curl -X POST "https://api.albert-bet.ru/casinos" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Lucky Casino"
  }'
```

Response:
```json
{
  "id": 1,
  "name": "Lucky Casino"
}
```

### 6. Get all casinos

```bash
curl -X GET "https://api.albert-bet.ru/casinos"
```

Response:
```json
[
  {
    "id": 1,
    "name": "Lucky Casino"
  },
  {
    "id": 2,
    "name": "Royal Casino"
  }
]
```

### 7. Create a review for a casino

```bash
curl -X POST "https://api.albert-bet.ru/reviews" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "stars": 5,
    "comment": "Great service!",
    "casino_id": 1
  }'
```

Response:
```json
{
  "id": 1,
  "stars": 5,
  "comment": "Great service!",
  "user_id": 1,
  "casino_id": 1
}
```

**Note:** Each user can only submit one review per casino. Attempting to submit a second review for the same casino will result in an error.

### 8. Get all reviews

```bash
curl -X GET "https://api.albert-bet.ru/reviews"
```

Response:
```json
[
  {
    "id": 1,
    "stars": 5,
    "comment": "Great service!",
    "user_id": 1,
    "casino_id": 1
  }
]
```

### 9. Get reviews for a specific casino

```bash
curl -X GET "https://api.albert-bet.ru/reviews?casino_id=1"
```

Response:
```json
[
  {
    "id": 1,
    "stars": 5,
    "comment": "Great service!",
    "user_id": 1,
    "casino_id": 1
  },
  {
    "id": 2,
    "stars": 4,
    "comment": "Good experience",
    "user_id": 2,
    "casino_id": 1
  }
]
```

## Database

- The SQLite database is stored at `/data/app.db` inside the container
- Data persists across container restarts using Docker volumes
- Tables are automatically created on application startup

## Security Notes

⚠️ **Important for Production:**

- The `JWT_SECRET` is currently hardcoded in `app/security.py`
- In production, move `JWT_SECRET` to environment variables:
  ```python
  SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
  ```
- Add to `docker-compose.yml`:
  ```yaml
  environment:
    - JWT_SECRET=your-very-secure-secret-key
  ```
- Use strong, randomly generated secrets in production
- SSL/TLS is configured via nginx with Let's Encrypt certificates
- Rate limiting is configured in nginx (10 requests/second with burst of 20)
- Security headers (HSTS, X-Frame-Options, etc.) are set by nginx

## Development

To run without Docker:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create the data directory:
```bash
mkdir -p /data
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## Stopping the Application

```bash
docker compose down
```

To remove the database volume as well:
```bash
docker compose down -v
```

## SSL Certificate Management

### Certificate Renewal

The certbot service automatically renews certificates every 12 hours. No manual intervention is required.

### Manual Certificate Renewal

If you need to manually renew the certificate:

```bash
docker compose run --rm certbot renew
docker compose exec nginx nginx -s reload
```

### Testing with Staging Certificate

For testing purposes, use the staging environment to avoid Let's Encrypt rate limits:

```bash
STAGING=1 ./init-letsencrypt.sh
```

### Switching from Staging to Production

1. Remove the staging certificates:
```bash
sudo rm -rf ./certbot/conf/*
```

2. Run the initialization script without staging:
```bash
./init-letsencrypt.sh
```

## Troubleshooting

### nginx fails to start

- Check if ports 80 and 443 are available
- Verify nginx configuration syntax: `docker compose exec nginx nginx -t`

### Certificate request fails

- Ensure DNS is properly configured for api.albert-bet.ru
- Verify port 80 is accessible from the internet
- Check certbot logs: `docker compose logs certbot`

### API not accessible

- Check all services are running: `docker compose ps`
- View nginx logs: `docker compose logs nginx`
- View API logs: `docker compose logs web`

## License

MIT