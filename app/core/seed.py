from app.db.models import User, Role
from app.db.database import SessionLocal
from app.core.security import hash_password


def seed_admin():
    db = SessionLocal()

    try:
        # ======================
        # CHECK EXISTING ADMIN
        # ======================
        existing = db.query(User).filter(User.email == "ab@gmail.com").first()
        if existing:
            print("⚠️ Admin already exists")
            return

        # ======================
        # ENSURE ADMIN ROLE EXISTS
        # ======================
        admin_role = db.query(Role).filter(Role.name == "admin").first()

        if not admin_role:
            print("⚠️ Admin role not found, creating...")

            admin_role = Role(
                name="admin",
                description="Super admin",
                permissions={
                    "dashboard": {"view": True, "create": True, "update": True, "delete": True},
                    "user": {"view": True, "create": True, "update": True, "delete": True},
                    "role": {"view": True, "create": True, "update": True, "delete": True},
                    "task": {"view": True, "create": True, "update": True, "delete": True},
                }
            )

            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)

        # ======================
        # CREATE ADMIN USER
        # ======================
        admin = User(
            email="ab@gmail.com",
            password=hash_password("123456"),
            roles=[admin_role]   # ✅ MULTI-ROLE
        )

        db.add(admin)
        db.commit()

        print("✅ Admin seeded successfully")

    finally:
        db.close()