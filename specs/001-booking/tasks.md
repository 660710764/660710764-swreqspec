# Tasks: จองคิวตรวจสุขภาพ (Booking)
Feature: 001-booking | Spec ID: SPEC-BKG-001 | อ้างอิง: plan.md (plan v1) | วันที่: 2569-09-23

สรุป: มีทั้งหมด 13 tasks (พร้อมทำ 11 tasks, รอ Q-02 จำนวน 2 tasks)
ทุก task ชี้กลับไปหา FR, NFR, CON, IF, DOM หรือ AC ใน spec.md ห้ามเริ่มเขียนโค้ดจนกว่าทีมจะสั่ง /implement

---

### T-01 สร้างโมเดลฐานข้อมูลและ migration
- รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-02, T-03, T-07
- ไฟล์ที่แตะ: `backend/app/db/models.py`, `backend/app/db/session.py`, `backend/app/db/migrations/001_init.py`, `backend/tests/conftest.py`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: รัน migration สร้างตาราง slots, bookings, audit_logs บน SQLite ในหน่วยความจำสำเร็จ และยืนยันว่าตาราง bookings ไม่มีคอลัมน์เลขบัตรประชาชน (national_id)
- สถานะ: เสร็จ รอทีมตรวจ

### T-02 พัฒนา API ค้นหาช่วงเวลาว่าง (GET /slots)
- รองรับ: FR-BKG-01, FR-BKG-06, NFR-PERF-01
- ตรวจด้วย: AC-BKG-05
- ไฟล์ที่แตะ: `backend/app/slots/router.py`, `backend/app/slots/service.py`, `backend/tests/test_AC_BKG_05.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: `pytest backend/tests/test_AC_BKG_05.py` ผ่าน โดยค้นหาช่วงเวลาว่างล่วงหน้า 30 วัน คำนวณช่วงว่างใหม่ตามแพ็กเกจ และวัด p95 เวลาตอบสนองผ่านเกณฑ์
- สถานะ: พร้อมทำ

### T-03 พัฒนาระบบจองคิวพื้นฐานและตัดที่นั่ง (POST /bookings)
- รองรับ: FR-BKG-04
- ตรวจด้วย: AC-BKG-01
- ไฟล์ที่แตะ: `backend/app/booking/router.py`, `backend/app/booking/service.py`, `backend/tests/test_AC_BKG_01.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: `pytest backend/tests/test_AC_BKG_01.py` ผ่าน โดยส่งคำขอยืนยันช่วง 09.00 น. ที่เหลือ 1 ที่สำเร็จ บันทึกการจอง และ remaining ลดเหลือ 0
- สถานะ: พร้อมทำ

### T-04 พัฒนาระบบปฏิเสธการจองซ้ำวันเดียวกัน
- รองรับ: FR-BKG-02
- ตรวจด้วย: AC-BKG-02
- ไฟล์ที่แตะ: `backend/app/booking/service.py`, `backend/tests/test_AC_BKG_02.py`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: `pytest backend/tests/test_AC_BKG_02.py` ผ่าน โดยปฏิเสธคำขอจองคิวใหม่เมื่อผู้รับบริการมีคิวในวันเดียวกันอยู่แล้ว และส่งหมายเลขคิวเดิมกลับมา
- สถานะ: พร้อมทำ

### T-05 พัฒนาระบบเสนอ 3 ช่วงเวลาใกล้เคียงเมื่อที่นั่งเต็ม
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: `backend/app/booking/service.py`, `backend/app/slots/service.py`, `backend/tests/test_AC_BKG_03.py`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: `pytest backend/tests/test_AC_BKG_03.py` ผ่าน โดยเมื่อช่วงเวลาเต็ม API ส่ง 409 พร้อม 3 ช่วงเวลาว่างที่ใกล้ที่สุดในวันเดียวกันและวันถัดไป 1 วัน โดยไม่สร้างรายการจอง
- สถานะ: พร้อมทำ

### T-06 พัฒนาระบบคิวส่งข้อความแจ้งเตือนและกลไกส่งซ้ำ (Async Notification Queue)
- รองรับ: FR-BKG-05, NFR-REL-02, IF-NOT-01
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: `backend/app/notify/queue.py`, `backend/app/booking/service.py`, `backend/tests/test_AC_BKG_04.py`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: `pytest backend/tests/test_AC_BKG_04.py` ผ่าน โดยเมื่อระบบแจ้งเตือนจำลองไม่ตอบสนอง การจองยังสำเร็จ และมีงานถูกนำเข้าคิวเพื่อส่งซ้ำภายใน 5 นาที
- สถานะ: พร้อมทำ

### T-07 พัฒนา Middleware บันทึก Audit Log ข้อมูลสุขภาพ
- รองรับ: DOM-PDPA-01
- ตรวจด้วย: AC-BKG-06
- ไฟล์ที่แตะ: `backend/app/audit/middleware.py`, `backend/tests/test_AC_BKG_06.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: `pytest backend/tests/test_AC_BKG_06.py` ผ่าน โดยตรวจสอบว่ามีบันทึกในตาราง audit_logs ระบุ actor_id, accessed_at และ hn ทุกครั้งที่มีการเปิดดูข้อมูลการจอง
- สถานะ: พร้อมทำ

### T-08 พัฒนาระบบตรวจรับรองตัวตน (IDP) และค้นหา HN จาก HIS
- รองรับ: IF-IDP-01, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-03
- ไฟล์ที่แตะ: `backend/app/auth/idp.py`, `backend/app/his/client.py`, `backend/tests/test_auth_his.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: `pytest backend/tests/test_auth_his.py` ผ่าน โดยสามารถตรวจผลยืนยันตัวตน และค้นหา HN จาก HIS ด้วยเลขบัตรประชาชนได้โดยไม่บันทึกเลขบัตรลงระบบ
- สถานะ: พร้อมทำ

### T-09 พัฒนาอัลกอริทึมการออกหมายเลขคิว
- รองรับ: FR-BKG-04
- ตรวจด้วย: ไม่มี AC ตรง ๆ รอ Q-02
- ไฟล์ที่แตะ: `backend/app/booking/service.py`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: มีฟังก์ชันสร้างหมายเลขคิวตามรูปแบบที่ถูกต้องและรีเซ็ตตามข้อกำหนดของโรงพยาบาล
- สถานะ: รอ Q-02

### T-10 พัฒนาหน้าจอเลือกแพ็กเกจและช่วงเวลา (SlotPicker)
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของหน้าจอ
- ไฟล์ที่แตะ: `frontend/src/pages/SlotPicker.jsx`, `frontend/src/__tests__/SlotPicker.test.jsx`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: `npm test -- frontend/src/__tests__/SlotPicker.test.jsx` ผ่าน โดยหน้าจอแสดงช่วงเวลาว่าง 30 วัน และอัปเดตช่วงเวลาเมื่อเปลี่ยนแพ็กเกจ (ผ่าน API จำลอง)
- สถานะ: พร้อมทำ

### T-11 พัฒนาหน้าจอยืนยันและการแจ้งเตือนช่วงเวลาเต็มพร้อม 3 ตัวเลือก (ConfirmBooking)
- รองรับ: FR-BKG-03, FR-BKG-04
- ตรวจด้วย: AC-BKG-03 (หน้าจอ)
- ไฟล์ที่แตะ: `frontend/src/pages/ConfirmBooking.jsx`, `frontend/src/__tests__/AC-BKG-03.test.jsx`
- ต้องทำหลัง: T-10
- เสร็จเมื่อ: `npm test -- frontend/src/__tests__/AC-BKG-03.test.jsx` ผ่าน โดยเมื่อ API จำลองตอบ 409 หน้าจอแสดงข้อความ "ช่วงเวลาเต็ม" และปุ่ม 3 ตัวเลือกช่วงเวลาว่างใกล้เคียง
- สถานะ: พร้อมทำ

### T-12 พัฒนาหน้าจอแสดงผลการจองสำเร็จและหมายเลขคิว (BookingResult)
- รองรับ: FR-BKG-04, FR-BKG-05
- ตรวจด้วย: ไม่มี AC ตรง ๆ รอ Q-02
- ไฟล์ที่แตะ: `frontend/src/pages/BookingResult.jsx`, `frontend/src/__tests__/BookingResult.test.jsx`
- ต้องทำหลัง: T-11
- เสร็จเมื่อ: หน้าจอแสดงผลสำเร็จของการจองและหมายเลขคิวได้ แม้การส่งข้อความยืนยันจะไม่สำเร็จ
- สถานะ: รอ Q-02

### T-13 เชื่อมต่อหน้าจอ Frontend เข้ากับ Backend API จริง
- รองรับ: FR-BKG-01, FR-BKG-02, FR-BKG-03, FR-BKG-04, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานบูรณาการระบบ
- ไฟล์ที่แตะ: `frontend/src/App.jsx`, `frontend/src/api/client.js`
- ต้องทำหลัง: T-02, T-05, T-11
- เสร็จเมื่อ: ผู้ใช้สามารถกดเลือกแพ็กเกจ วัน เวลา และกดยืนยันการจองผ่าน API จริงได้ครบทุก Flow
- สถานะ: พร้อมทำ

---

## ตารางตรวจความครบ

### 1. ความสอดคล้องกับ Acceptance Criteria
| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| `AC-BKG-01` | T-03 (จองสำเร็จ ตัดที่นั่ง remaining เป็น 0) |
| `AC-BKG-02` | T-04 (ปฏิเสธการจองซ้ำวันเดียวกัน และคืนคิวเดิม) |
| `AC-BKG-03` | T-05 (Backend ตอบ 409 พร้อม 3 ช่วงใกล้เคียง), T-11 (หน้าจอแสดงข้อความและ 3 ตัวเลือก) |
| `AC-BKG-04` | T-06 (บันทึกการจองสำเร็จ และนำเข้าคิวส่งซ้ำภายใน 5 นาที) |
| `AC-BKG-05` | T-02 (ค้นหาช่วงเวลาว่าง และวัด p95 เวลาตอบสนอง) |
| `AC-BKG-06` | T-07 (ตรวจพบ audit log เมื่อมีการเปิดดูข้อมูลการจอง) |

### 2. ความสอดคล้องกับ Constraints
| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| `CON-TECH-01` | T-01 (กำหนดโมเดลฐานข้อมูลรองรับ PostgreSQL และ SQLite สำหรับเทสต์) |
| `DOM-PDPA-01` | T-01 (โมเดล audit_logs), T-07 (Middleware ดักจับการเข้าถึงข้อมูลสุขภาพ) |
| `IF-IDP-01` | T-08 (ตรวจผลยืนยันตัวตนก่อนเข้าถึง endpoint) |
| `IF-HIS-01` | T-01 (ตาราง bookings ไม่เก็บเลขบัตรประชาชน), T-08 (ดึง HN ผ่าน HIS API) |
| `IF-NOT-01` | T-06 (แยกคิวส่งข้อความแจ้งเตือนแบบ asynchronous ไม่บล็อกการจอง) |

---

## สิ่งที่ยังไม่ทำ (คัดลอกจาก Open Questions ใน spec.md)

- **Q-02**: หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง และมีรูปแบบอย่างไร (เช่น A001)? -> ถามเจ้าหน้าที่เวชระเบียน (ยังไม่ได้คำตอบ)  
  *งานที่รออยู่*: **T-09** (ออกหมายเลขคิว) และ **T-12** (แสดงหมายเลขคิวบนหน้าจอผลลัพธ์) จะยังไม่เริ่มทำจนกว่าจะได้คำตอบ
