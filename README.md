# 📌 Task Manager Backend

A **Role-Based Task Management Backend** built using **FastAPI** and **PostgreSQL**, implementing **JWT Authentication** and **Role-Based Access Control (RBAC)**.


<img width="1865" height="829" alt="Screenshot 2026-04-21 174538" src="https://github.com/user-attachments/assets/066c68c3-60a3-4536-87de-4cb3dccc8a9b" />

<img width="1855" height="589" alt="Screenshot 2026-04-21 174605" src="https://github.com/user-attachments/assets/7d9385ab-f089-46f7-bcd5-6d93da8f2b6d" />

<img width="1858" height="842" alt="Screenshot 2026-04-21 174759" src="https://github.com/user-attachments/assets/2e72b233-59ee-48ec-b35f-ac2f1d4de573" />

<img width="1851" height="784" alt="Screenshot 2026-04-21 174908" src="https://github.com/user-attachments/assets/eea28a4e-5c7b-4fe2-9b99-1144cef731d5" />


---

## 🚀 Features
🔐 Authentication
JWT Login (Access + Refresh tokens)
Secure cookies for refresh token
/auth/me for current user
👥 Users (Multi-Role System)
Create users with multiple roles
UUID-based user IDs
Prevent self-deletion
Pagination + filtering
🧩 Roles (RBAC Core)
Dynamic permission system (JSON-based)
Multiple roles per user
Permission merging logic
Auto rules:
If create/update/delete = true → view = true
If view = false → all actions = false
📋 Tasks
Create / update / delete tasks
Assign tasks to users
Default assignment = self
Admin → full access
User → own tasks only
🔍 Filtering & Pagination
Users:
Filter by email
Filter by multiple roles
Roles:
Filter by name
Offset-based pagination

---

🧱 Tech Stack
Layer	Tech
Backend	FastAPI
Database	PostgreSQL
ORM	SQLAlchemy
Auth	JWT (python-jose)
Hashing	passlib + bcrypt
Server	Uvicorn

---

## 🌐 Base URL

http://127.0.0.1:8000

---


---

🔌 API Endpoints
🔐 Authentication
Method	Endpoint	Description
POST	/auth/login	Login user
POST	/auth/refresh	Refresh access token
GET	/auth/me	Get current user
👥 Users
Method	Endpoint	Description
POST	/users/	Create user
GET	/users/	Get users (filter + pagination)
PUT	/users/{user_id}	Update user
DELETE	/users/{user_id}	Delete user
🔍 User Filters
GET /users?email=gmail
GET /users?roles=admin,tester
GET /users?page=1&limit=10
🧩 Roles
Method	Endpoint	Description
POST	/roles/	Create role
GET	/roles/	Get roles (filter + pagination)
PUT	/roles/{role_id}	Update role
DELETE	/roles/{role_id}	Delete role
🔍 Role Filters
GET /roles?name=admin
GET /roles?page=1&limit=10
📋 Tasks
Method	Endpoint	Description
POST	/tasks/	Create task
GET	/tasks/	Get tasks
GET	/tasks/{task_id}	Get single task
PUT	/tasks/{task_id}	Update task
DELETE	/tasks/{task_id}	Delete task
🔑 Authorization

All protected routes require:

Authorization: Bearer <access_token>
👥 RBAC (Role-Based Access Control)
🧠 Multi-Role Logic
One user → multiple roles
Permissions merged across roles
OR logic:
If any role allows → access granted
📊 Permission Structure
{
  "user": {
    "view": true,
    "create": true,
    "update": false,
    "delete": false
  }
}
🔥 Smart Rules
Rule	Behavior
create/update/delete = true	view = true
view = false	all = false
📋 Access Matrix
Action	Admin	User
View all tasks	✅	❌
View own tasks	✅	✅
Create task	✅	✅
Update any task	✅	❌
Delete task	✅	❌
Manage users	✅	❌
🆔 UUID SYSTEM
Users → UUID
Roles → UUID
API uses UUID everywhere


---

## 🗂️ Project Structure

Backend/
│── app/
│   ├── core/          # security, permissions
│   ├── db/            # models, database
│   ├── routes/        # API endpoints
│   ├── schemas/       # request/response validation
│   ├── services/      # business logic
│   └── main.py
│
│── alembic/           # migrations
│── .env
│── requirements.txt
│── .gitignore
---

## ⚙️ Setup Instructions

### 1. Clone Repository

git clone <repo-url>
cd Backend

### 2. Create Virtual Environment

python -m venv env
env\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Setup Environment Variables

Create a `.env` file:

### 5. Run Server

uvicorn app.main:app --reload

### 6. Open API Docs

http://127.0.0.1:8000/docs

---

## 📸 API Preview

* Swagger UI for testing endpoints
* PostgreSQL (pgAdmin) for database visualization

---

## 🧠 Architecture

Routes → Services → DB Models
        ↓
     Schemas (Validation)
        ↓
     Core (Security & RBAC)

---

## 🔐 Security

* Passwords are hashed using bcrypt
* JWT tokens are securely signed
* Protected routes require authentication

---


## 👨‍💻 Author

**Abhijit Maity**
