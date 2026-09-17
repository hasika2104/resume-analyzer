#!/usr/bin/env python3
import sys
sys.path.insert(0, ".")

from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.utils.auth import get_password_hash

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    demo = db.query(User).filter(User.email == "demo@career.ai").first()
    if not demo:
        demo = User(
            email="demo@career.ai",
            hashed_password=get_password_hash("demo123"),
            full_name="Demo User",
        )
        db.add(demo)
        print("Demo user: demo@career.ai / demo123")

    admin = db.query(User).filter(User.email == "admin@career.ai").first()
    if not admin:
        admin = User(
            email="admin@career.ai",
            hashed_password=get_password_hash("admin123"),
            full_name="Platform Admin",
            is_admin=True,
        )
        db.add(admin)
        print("Admin user: admin@career.ai / admin123")

    db.commit()
    print("Seed complete.")
finally:
    db.close()
