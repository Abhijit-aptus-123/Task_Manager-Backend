# 📌 Task Manager Backend

A **Role-Based Task Management Backend** built using **FastAPI** and **PostgreSQL**, implementing **JWT Authentication** and **Role-Based Access Control (RBAC)**.


<img width="1865" height="829" alt="Screenshot 2026-04-21 174538" src="https://github.com/user-attachments/assets/066c68c3-60a3-4536-87de-4cb3dccc8a9b" />

<img width="1855" height="589" alt="Screenshot 2026-04-21 174605" src="https://github.com/user-attachments/assets/7d9385ab-f089-46f7-bcd5-6d93da8f2b6d" />

<img width="1858" height="842" alt="Screenshot 2026-04-21 174759" src="https://github.com/user-attachments/assets/2e72b233-59ee-48ec-b35f-ac2f1d4de573" />

<img width="1851" height="784" alt="Screenshot 2026-04-21 174908" src="https://github.com/user-attachments/assets/eea28a4e-5c7b-4fe2-9b99-1144cef731d5" />


---

## 🚀 Features

* 🔐 User Authentication (Register & Login)
* 🔑 JWT-based Authorization
* 👥 Role-Based Access (Admin & User)
* 📋 Task Management (CRUD)
* 🗄️ PostgreSQL Integration
* 📄 Swagger API Documentation

---

## 🧱 Tech Stack

* **Backend:** FastAPI (Python)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Authentication:** JWT (python-jose)
* **Password Hashing:** passlib + bcrypt
* **Server:** Uvicorn

---

## 🌐 Base URL

http://127.0.0.1:8000

---


---

# 🔌 API Endpoints

## 🔐 Authentication

| Method | Endpoint        | Description |
|--------|----------------|------------|
| POST   | /auth/login    | Login user |
| POST   | /auth/refresh  | Refresh access token |
| GET    | /auth/me       | Get current user |

---
## 👥 Admin

| Method | Endpoint                         | Description |
|--------|----------------------------------|------------|
| GET    | /admin/users                     | Get all users |
| POST   | /admin/users                     | Create user/admin |
| PUT    | /admin/users/{user_id}/role      | Update user role |

---

## 📋 Tasks

| Method | Endpoint              | Description |
|--------|----------------------|------------|
| GET    | /tasks               | Get tasks |
| POST   | /tasks               | Create task |
| PUT    | /tasks/{task_id}     | Update task (including status) |
| DELETE | /tasks/{task_id}     | Delete task |

---

## 🔑 Authorization

All protected routes require:


---

### 📋 Tasks

| Method | Endpoint         | Description |
| ------ | ---------------- | ----------- |
| GET    | /tasks           | Get tasks   |
| POST   | /tasks           | Create task |
| PUT    | /tasks/{task_id} | Update task |
| DELETE | /tasks/{task_id} | Delete task |

---

## 🔑 Authorization

All protected routes require:

Authorization: Bearer <access_token>

---

## 👥 Role-Based Access

| Action              | Admin | User |
|--------------------|------|------|
| View all tasks     | ✅   | ❌   |
| View own tasks     | ✅   | ✅   |
| Create task        | ✅   | ✅   |
| Update any task    | ✅   | ❌   |
| Update status      | ✅   | ✅ (own only) |
| Delete task        | ✅   | ❌   |
| Manage users       | ✅   | ❌   |

---

## 🗂️ Project Structure

Backend/
│── app/
│ ├── core/ # Security & dependencies
│ ├── db/ # Database & models
│ ├── routes/ # API routes
│ ├── schemas/ # Pydantic schemas
│ ├── services/ # Business logic
│ └── main.py # Entry point
│── assets/ # Images (Swagger screenshot)
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

DATABASE_URL=postgresql://postgres:password@localhost:5432/taskdb
SECRET_KEY=your_secret_key

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

* Routes → Handle requests
* Services → Business logic
* Schemas → Validation
* Models → Database structure
* Core → Security & dependencies

---

## 🔐 Security

* Passwords are hashed using bcrypt
* JWT tokens are securely signed
* Protected routes require authentication

---

## 🎯 Future Improvements

* 🔍 Search & Filtering
* 📄 Pagination
* 🔄 Refresh Tokens
* 🐳 Docker Deployment

---

## 👨‍💻 Author

**Abhijit Maity**
