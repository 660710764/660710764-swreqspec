"""
Database migration 001_init: create initial tables.
"""
from app.db.models import Base


# รองรับ CON-TECH-01, DOM-PDPA-01, IF-HIS-01 สร้างตาราง slots, bookings, audit_logs
def upgrade(engine):
    Base.metadata.create_all(bind=engine)


# รองรับ CON-TECH-01 ลบตารางทั้งหมดสำหรับการ rollback
def downgrade(engine):
    Base.metadata.drop_all(bind=engine)
