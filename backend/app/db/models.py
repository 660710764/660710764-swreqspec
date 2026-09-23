"""
Database models for Health Check Booking System.
"""
from datetime import datetime, date, time
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    DateTime,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# รองรับ FR-BKG-01, FR-BKG-06, ASM-01, CON-TECH-01
class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slot_date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    package_code = Column(String(50), nullable=False, index=True)
    capacity = Column(Integer, nullable=False)
    remaining = Column(Integer, nullable=False)

    bookings = relationship("Booking", back_populates="slot")

    __table_args__ = (
        CheckConstraint("remaining >= 0", name="check_remaining_non_negative"),
        CheckConstraint("capacity >= 0", name="check_capacity_non_negative"),
    )


# รองรับ FR-BKG-02, FR-BKG-04, IF-HIS-01 (ไม่มีคอลัมน์เลขบัตรประชาชน / national_id)
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String(36), primary_key=True)  # UUID string
    hn = Column(String(20), nullable=False, index=True)  # เก็บเฉพาะ HN ตาม IF-HIS-01
    slot_id = Column(Integer, ForeignKey("slots.id"), nullable=False)
    booking_date = Column(Date, nullable=False, index=True)
    queue_no = Column(String(50), nullable=True)  # ว่างได้ รอคำตอบ Q-02
    status = Column(String(20), nullable=False, default="CONFIRMED")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    slot = relationship("Slot", back_populates="bookings")


# รองรับ DOM-PDPA-01 บันทึก audit log ทุกครั้งที่เข้าถึงข้อมูลสุขภาพ
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    actor_id = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False)
    hn = Column(String(20), nullable=False, index=True)
    accessed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
