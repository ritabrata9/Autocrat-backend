# Autocrat Backend

Backend service for **Autocrat**, a social platform API built using FastAPI.  
The project demonstrates two parallel approaches to database interaction: **ORM (SQLAlchemy)** and **non-ORM (raw SQL)**.

---

## Key Highlights

- Dual architecture: ORM vs raw SQL implementation
- JWT-based authentication (OAuth2 password flow)
- Post creation, like/unlike system, and user management
- Alembic-based migrations
- Dockerized development and production setup
- Modular FastAPI structure with routers

---

## Tech Stack

- **Framework:** FastAPI  
- **Language:** Python  
- **Database:** PostgreSQL  
- **ORM:** SQLAlchemy  
- **Migrations:** Alembic  
- **Auth:** JWT (OAuth2)  
- **Containerization:** Docker + Docker Compose  

---

## Project Structure


autocrat-backend/
│
├── orm/
│ ├── app/
│ │ ├── __init__.py
│ │ ├── main.py
│ │ ├── database.py
│ │ ├── models.py
│ │ ├── schemas.py
│ │ ├── oauth2.py
│ │ ├── utils.py
│ │ └── routers/
│ │ ├── auth.py
│ │ ├── user.py
│ │ ├── post.py
│ │ └── likes.py
│ │
│ ├── alembic/
│ ├── tests/
│ ├── Dockerfile
│ ├── docker-compose-dev.yaml
│ ├── docker-compose-prod.yaml
│ └── requirements.txt
│
├── non-orm/
│ └── app/
│ ├── main.py
│ ├── database.py
│ ├── models.py
│ └── schemas.py
│
├── requirements.txt
└── .gitignore


---

## Features

### Authentication
- User registration and login
- Password hashing
- JWT token generation and validation
- OAuth2 password flow

### Users
- Create and retrieve users
- Secure access to user-specific data

### Posts
- Create, read, delete posts
- Ownership-based authorization

### Likes System
- Like / unlike posts
- Prevent duplicate likes

### Infrastructure
- CORS configuration
- Database session management
- Environment-based configuration
- Debug endpoint for DB inspection

---

## Running the Project

### Local Setup

```bash
git clone https://github.com/ritabrata9/Autocrat-backend.git
cd Autocrat-backend/orm

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

Create .env file:

DATABASE_URL=postgresql://user:password@localhost:5432/autocrat
SECRET_KEY=your_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

Run server:

uvicorn app.main:app --reload
Docker Setup

Development:

docker-compose -f docker-compose-dev.yaml up --build

Production:

docker-compose -f docker-compose-prod.yaml up --build
Database Migrations (Alembic)
alembic revision -m "message"
alembic upgrade head
API Overview
Auth
POST /login
Users
POST /users
GET /users/{id}
Posts
GET /posts
POST /posts
DELETE /posts/{id}
Likes
POST /like
Authentication Flow
User logs in → receives JWT
Token is sent in headers:
Authorization: Bearer <token>
Protected routes validate token
Sample API Responses
Login

Request

{
  "username": "test@example.com",
  "password": "password123"
}

Response

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
Create User

Request

{
  "email": "user@example.com",
  "password": "password123"
}

Response

{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2026-04-06T12:00:00Z"
}
Create Post

Request

{
  "title": "My First Post",
  "content": "This is a post"
}

Response

{
  "id": 1,
  "title": "My First Post",
  "content": "This is a post",
  "owner_id": 1
}
Like / Unlike

Request

{
  "post_id": 1,
  "dir": 1
}

Response

{
  "message": "successfully added like"
}
Design Decisions
Separate ORM and non-ORM implementations to demonstrate depth
Modular routers for scalability
JWT-based stateless authentication
Dockerized environment for consistency
Alembic for schema versioning


Author

Ritabrata