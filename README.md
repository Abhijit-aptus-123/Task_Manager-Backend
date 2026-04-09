📌 Task Manager Backend

A Role-Based Task Management Backend built using FastAPI + PostgreSQL with JWT Authentication and RBAC (Role-Based Access Control).

🚀 Features
🔐 User Authentication (Register & Login)
🔑 JWT-based Authorization
👥 Role-Based Access (Admin & User)
📋 Task Management (CRUD)
🗄️ PostgreSQL Database Integration
📄 Interactive API Docs (Swagger)
🧱 Tech Stack
Backend: FastAPI (Python)
Database: PostgreSQL
ORM: SQLAlchemy
Authentication: JWT (python-jose)
Password Hashing: passlib + bcrypt
Server: Uvicorn
API Testing: Swagger UI
🌐 Base URL
http://127.0.0.1:8000
🔌 API Endpoints
🔐 Authentication
1. Register
POST /auth/register
2. Login
POST /auth/login
📋 Task APIs
3. Get Tasks
GET /tasks
4. Create Task
POST /tasks
5. Update Task
PUT /tasks/{task_id}
6. Delete Task
DELETE /tasks/{task_id}
🔑 Authorization

All protected routes require:

Authorization: Bearer <access_token>
👥 Role-Based Access Control
Action	Admin	User
View all tasks	✅	❌
View own tasks	✅	✅
Create task	✅	✅
Update any task	✅	❌
Delete task	✅	❌
🗂️ Project Structure
Backend/
 ├── app/
 │   ├── core/          # Security & dependencies
 │   ├── db/            # Database & models
 │   ├── routes/        # API routes
 │   ├── schemas/       # Pydantic schemas
 │   ├── services/      # Business logic
 │   └── main.py        # Entry point
 ├── .env
 ├── requirements.txt
 └── .gitignore
⚙️ Setup Instructions
1️⃣ Clone Repo
git clone <your-repo-url>
cd Backend
2️⃣ Create Virtual Environment
python -m venv env
env\Scripts\activate   # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Setup Environment Variables

Create .env file:

DATABASE_URL=postgresql://postgres:password@localhost:5432/taskdb
SECRET_KEY=your_secret_key
5️⃣ Run Server
uvicorn app.main:app --reload
6️⃣ Open Swagger Docs
http://127.0.0.1:8000/docs
