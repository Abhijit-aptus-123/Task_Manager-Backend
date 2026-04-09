# 📌 Task Manager Backend

A **Role-Based Task Management Backend** built using **FastAPI** and **PostgreSQL**, implementing **JWT Authentication** and **Role-Based Access Control (RBAC)**.

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

## 🔌 API Endpoints

### 🔐 Authentication

| Method | Endpoint       | Description   |
| ------ | -------------- | ------------- |
| POST   | /auth/register | Register user |
| POST   | /auth/login    | Login user    |

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

| Action          | Admin | User |
| --------------- | ----- | ---- |
| View all tasks  | ✅     | ❌    |
| View own tasks  | ✅     | ✅    |
| Create task     | ✅     | ✅    |
| Update any task | ✅     | ❌    |
| Delete task     | ✅     | ❌    |

---

## 🗂️ Project Structure

Backend/
│── app/
│   ├── core/        # Security & dependencies
│   ├── db/          # Database & models
│   ├── routes/      # API routes
│   ├── schemas/     # Pydantic schemas
│   ├── services/    # Business logic
│   └── main.py      # Entry point
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
