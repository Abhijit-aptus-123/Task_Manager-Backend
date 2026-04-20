from app.db.models import User, Role
from app.db.database import SessionLocal
from app.core.security import hash_password


def seed_admin():
    db = SessionLocal()

    # check if admin exists
    existing = db.query(User).filter(User.email == "ab@gmail.com").first()
    if existing:
        return

    # get admin role
    admin_role = db.query(Role).filter(Role.name == "admin").first()

    if not admin_role:
        print("❌ Admin role not found")
        return

    admin = User(
        email="ab@gmail.com",
        password=hash_password("123456"),
        roles=[admin_role]   # ✅ CORRECT
    )

    db.add(admin)
    db.commit()
    db.close()

    print("✅ Admin seeded")