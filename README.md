# FastAPI Backend with SQLite

A simple FastAPI backend with user registration, authentication (JWT), and review system.

## Features

- User registration with email, password, and name
- JWT Bearer authentication for login
- User profile endpoints (GET and PATCH)
- Review system with stars (1-5) and comments
- SQLite database with persistent volume
- Docker containerization

## Requirements

- Docker
- Docker Compose

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
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Running the Application

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

## API Endpoints

### Root
- `GET /` - Welcome message

### Authentication
- `POST /register` - Register a new user
- `POST /login` - Login and get JWT token

### User Profile
- `GET /users/me` - Get current user profile (requires authentication)
- `PATCH /users/me` - Update user name (requires authentication)

### Reviews
- `POST /reviews` - Create a review (requires authentication)
- `GET /reviews` - Get all reviews

## Usage Examples

### 1. Register a new user

```bash
curl -X POST "http://localhost:8000/register" \
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
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe"
}
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/login?email=user@example.com&password=securepassword123"
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
curl -X GET "http://localhost:8000/users/me" \
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
curl -X PATCH "http://localhost:8000/users/me" \
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

### 5. Create a review

```bash
curl -X POST "http://localhost:8000/reviews" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "stars": 5,
    "comment": "Great service!"
  }'
```

Response:
```json
{
  "id": 1,
  "stars": 5,
  "comment": "Great service!",
  "user_id": 1
}
```

### 6. Get all reviews

```bash
curl -X GET "http://localhost:8000/reviews"
```

Response:
```json
[
  {
    "id": 1,
    "stars": 5,
    "comment": "Great service!",
    "user_id": 1
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
- Consider using HTTPS/TLS for API communication
- Implement rate limiting for authentication endpoints

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

## License

MIT