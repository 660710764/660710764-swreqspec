"""
Pytest fixtures and in-memory test database setup.
"""
import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.db.models import Base
from app.db.migrations.001_init import upgrade


# รองรับ CON-TECH-01 เตรียมฐานข้อมูล SQLite ในหน่วยความจำสำหรับทุก test
@pytest.fixture(scope="function")
def db_engine():
    engine = create_engine("sqlite:///:memory:")
    upgrade(engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


# รองรับ CON-TECH-01 เตรียม session สำหรับการทดสอบ
@pytest.fixture(scope="function")
def db_session(db_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    yield session
    session.close()


# รองรับ T-01 ยืนยันว่าตารางถูกสร้างครบ และตาราง bookings ไม่มี national_id (IF-HIS-01)
def test_t01_migration_and_models(db_engine):
    inspector = inspect(db_engine)
    table_names = inspector.get_table_names()

    # ตรวจสอบว่ามีครบทั้ง 3 ตาราง
    assert "slots" in table_names
    assert "bookings" in table_names
    assert "audit_logs" in table_names

    # ตรวจสอบว่าตาราง bookings เก็บเฉพาะ hn และไม่มีคอลัมน์ national_id ตาม IF-HIS-01
    booking_columns = [col["name"] for col in inspector.get_columns("bookings")]
    assert "hn" in booking_columns
    assert "national_id" not in booking_columns
    assert "id_card" not in booking_columns
    assert "citizen_id" not in booking_columns
