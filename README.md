# Autocrat Backend

Backend service for **Autocrat**, a social platform API built using FastAPI.  
The project demonstrates two parallel approaches to database interaction: **ORM (SQLAlchemy)** and **non-ORM (raw SQL)**.

---

## Key Highlights

- Dual architecture: ORM vs raw SQL implementation
- JWT-based authentication (OAuth2 password flow)
- Post creation, like/unlike, comments and user management
- Alembic-based migrations
- Dockerized development and production setup
- Modular FastAPI structure with routers
- Role-based access control (ADMIN has control over all posts and users)


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

```

autocrat-backend/
│
├── orm
├── 📁 alembic
├── 📁 app
│   ├── 📁 routers
│   │   ├── 🐍 auth.py
│   │   ├── 🐍 comments.py
│   │   ├── 🐍 likes.py
│   │   ├── 🐍 post.py
│   │   └── 🐍 user.py
│   ├── 🐍 __init__.py
│   ├── 🐍 database.py
│   ├── 🐍 main.py
│   ├── 🐍 models.py
│   ├── 🐍 oauth2.py
│   ├── 🐍 schemas.py
│   └── 🐍 utils.py
├── 📁 tests
│   └── 🐍 mytest.py
├── 🐳 Dockerfile
├── ⚙️ alembic.ini
├── ⚙️ docker-compose-dev.yaml
├── ⚙️ docker-compose-prod.yaml
└── 📄 requirements.txt

````

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

### Comments System
- Create/ Delete comments on posts

### Infrastructure
- CORS configuration
- Database session management
- Environment-based configuration

---

## Running the Project

### Local Setup

```bash
git clone https://github.com/ritabrata9/Autocrat-backend.git
cd Autocrat-backend/orm

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
````

### Create `.env` file

```
DATABASE_URL=postgresql://user:password@localhost:5432/autocrat
SECRET_KEY=your_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Run server

```bash
uvicorn app.main:app --reload
```

---

## Docker Setup

### Development

```bash
docker-compose -f docker-compose-dev.yaml up --build
```

### Production

```bash
docker-compose -f docker-compose-prod.yaml up --build
```

---

## Database Migrations (Alembic)

```bash
alembic revision -m "message"
alembic upgrade head
```

---

## API Overview

### Auth

* `POST /login`

### Users

* `POST /users`
* `GET /users/{id}`

### Posts

* `GET /posts`
* `POST /posts`
* `DELETE /posts/{id}`

### Likes

* `POST /like`

### Comments

* `POST /comments/{post_id}`
* `DELETE /comments/{comment_id}`


---

## Authentication Flow

1. User logs in → receives JWT
2. Token is sent in headers:

```
Authorization: Bearer <token>
```

3. Protected routes validate token

---

## Sample API Responses

### Login

**Request**

```json
{
  "username": "test@example.com",
  "password": "password123"
}
```

**Response**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### Create User

**Request**

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response**

```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2026-04-06T12:00:00Z"
}
```

---

### Create Post

**Request**

```json
{
  "title": "My First Post",
  "content": "This is a post"
}
```

**Response**

```json
{
  "id": 1,
  "title": "My First Post",
  "content": "This is a post",
  "owner_id": 1
}
```

---

### Like / Unlike

**Request**

```json
{
  "post_id": 1,
  "dir": 1
}
```

**Response**

```json
{
  "message": "successfully added like"
}
```

---

## Author

Ritabrata
