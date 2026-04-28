from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import role
from app.routes import dashboard
from app.routes import users
from app.core.seed import seed_admin
from app.db.database import Base, engine


# ROUTERS
from app.routes import auth, admin, task
from app.routes import audit
from app.routes import notification

app = FastAPI()

# ======================
# CORS CONFIG
# ======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://mainstream-magnetic-leader-jets.trycloudflare.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# DATABASE
# ======================
Base.metadata.create_all(bind=engine)

# ======================
# ROUTERS
# ======================
app.include_router(auth.router)
# app.include_router(admin.router)
app.include_router(task.router)  # added task router
app.include_router(role.router)
app.include_router(dashboard.router)
app.include_router(users.router)

@app.on_event("startup")
def startup():
    seed_admin()
app.include_router(audit.router)
app.include_router(notification.router)