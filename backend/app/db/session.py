"""
Database session and engine management.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# รองรับ CON-TECH-01 สลับระหว่าง PostgreSQL และ SQLite ในหน่วยความจำผ่าน DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# รองรับ SQLite สำหรับ testing และ PostgreSQL สำหรับ production
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# รองรับ CON-TECH-01 ให้บริการ database session สำหรับ Dependency Injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
