# 📌 Task Manager Backend

A **Role-Based Task Management Backend API** built using **FastAPI** and **PostgreSQL**, implementing **JWT Authentication** and a dynamic **Role-Based Access Control (RBAC)** system.

---

## 📸 API Preview

<img width="1865" height="829" alt="Swagger UI" src="https://github.com/user-attachments/assets/066c68c3-60a3-4536-87de-4cb3dccc8a9b" />

<img width="1855" height="589" alt="Users API" src="https://github.com/user-attachments/assets/7d9385ab-f089-46f7-bcd5-6d93da8f2b6d" />

<img width="1858" height="842" alt="Tasks API" src="https://github.com/user-attachments/assets/2e72b233-59ee-48ec-b35f-ac2f1d4de573" />

<img width="1851" height="784" alt="Database View" src="https://github.com/user-attachments/assets/eea28a4e-5c7b-4fe2-9b99-1144cef731d5" />

---

## 🚀 Features

### 🔐 Authentication
- JWT Login (Access + Refresh Tokens)
- Secure cookie-based refresh tokens
- `/auth/me` for current user

### 👥 Users (Multi-Role System)
- Create users with multiple roles
- UUID-based user IDs
- Prevent self-deletion
- Pagination & filtering support

### 🧩 Roles (RBAC Core)
- Dynamic permission system (JSON-based)
- Multiple roles per user
- Permission merging (OR logic)

#### 🔥 Smart Permission Rules
- If `create/update/delete = true` → `view = true`
- If `view = false` → all actions = false

### 📋 Tasks
- Create, update, delete tasks
- Assign tasks to users
- Default assignment = self
- Admin → full access
- User → only own tasks

### 🔍 Filtering & Pagination

**Users**
- Filter by email → `/users?email=gmail`
- Filter by roles → `/users?roles=admin,tester`
- Pagination → `/users?page=1&limit=10`

**Roles**
- Filter by name → `/roles?name=admin`
- Pagination → `/roles?page=1&limit=10`

---

## 🧱 Tech Stack

| Layer        | Tech            |
|-------------|----------------|
| Backend     | FastAPI        |
| Database    | PostgreSQL     |
| ORM         | SQLAlchemy     |
| Auth        | JWT (python-jose) |
| Hashing     | passlib + bcrypt |
| Server      | Uvicorn        |

---
## 🌐 Base URL
http://127.0.0.1:8000

---

## 🔌 API Endpoints

### 🔐 Authentication

| Method | Endpoint        | Description |
|--------|----------------|------------|
| POST   | /auth/login    | Login user |
| POST   | /auth/refresh  | Refresh access token |
| GET    | /auth/me       | Get current user |

---

### 👥 Users

| Method | Endpoint            | Description |
|--------|--------------------|------------|
| POST   | /users/            | Create user |
| GET    | /users/            | Get users (filter + pagination) |
| PUT    | /users/{user_id}   | Update user |
| DELETE | /users/{user_id}   | Delete user |

---

### 🧩 Roles

| Method | Endpoint            | Description |
|--------|--------------------|------------|
| POST   | /roles/            | Create role |
| GET    | /roles/            | Get roles (filter + pagination) |
| PUT    | /roles/{role_id}   | Update role |
| DELETE | /roles/{role_id}   | Delete role |

---

### 📋 Tasks

| Method | Endpoint                | Description |
|--------|------------------------|------------|
| POST   | /tasks/                | Create task |
| GET    | /tasks/                | Get tasks |
| GET    | /tasks/{task_id}       | Get single task |
| PUT    | /tasks/{task_id}       | Update task |
| DELETE | /tasks/{task_id}       | Delete task |

---

## 🔑 Authorization

All protected routes require:
Authorization: Bearer <access_token>

---

## 👥 RBAC (Role-Based Access Control)

### 🧠 Multi-Role Logic
- One user → multiple roles
- Permissions merged across roles
- OR logic → If any role allows → access granted

---

### 📊 Permission Structure

```json
{
  "user": {
    "view": true,
    "create": true,
    "update": false,
    "delete": false
  }
}
```

## 📋 Access Matrix

| Action           | Admin | User |
|------------------|-------|------|
| View all tasks   | ✅    | ❌   |
| View own tasks   | ✅    | ✅   |
| Create task      | ✅    | ✅   |
| Update any task  | ✅    | ❌   |
| Delete task      | ✅    | ❌   |
| Manage users     | ✅    | ❌   |

---

## 🆔 UUID System

- Users → UUID  
- Roles → UUID  
- APIs use UUID everywhere  

---

## 🗂️ Project Structure

```bash
Backend/
│── app/
│   ├── core/          # security, RBAC logic
│   ├── db/            # models, database setup
│   ├── routes/        # API endpoints
│   ├── schemas/       # validation (Pydantic)
│   ├── services/      # business logic
│   └── main.py
│
│── alembic/           # migrations
│── .env
│── requirements.txt
│── .gitignore
```

---

## ⚙️ Setup Instructions

```bash
Backend/
│── app/
│   ├── core/          # security, RBAC logic
│   ├── db/            # models, database setup
│   ├── routes/        # API endpoints
│   ├── schemas/       # validation (Pydantic)
│   ├── services/      # business logic
│   └── main.py
│
│── alembic/           # migrations
│── .env
│── requirements.txt
│── .gitignore
```

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd Backend
```

### 2. Create Virtual Environment

```bash
python -m venv env

# Windows
env\Scripts\activate

# Linux / Mac
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file.

---

### 5. Run Server

```bash
uvicorn app.main:app --reload
```

---

### 6. Open API Docs

- Swagger UI → http://127.0.0.1:8000/docs  
- ReDoc → http://127.0.0.1:8000/redoc  

---

## 🧠 Architecture

```
Routes → Services → Database Models
        ↓
     Schemas (Validation)
        ↓
     Core (Security & RBAC)
```

---

## 🔐 Security

- Passwords hashed using bcrypt  
- JWT tokens with expiration  
- Secure authentication & authorization  
- Role-based permission enforcement  
- Prevents critical misuse (e.g., self-deletion)  

---

## 👨‍💻 Author

- Abhijit Maity

---
