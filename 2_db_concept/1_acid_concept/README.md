## Question
![](/assets/q_acid.png)
## Response Section 
### ความหมายของ ACID
- A - Atomicity คือ การทำ transaction ที่ทั้งหมดต้องทำสำเร็จ หากมี process ใดๆไม่สำเร็จก็จะยกเลิก (ฺBEGIN COMMIT ROLLBACK)
- C - Consistency คือ ข้อมูลก่อนและหลัง transaction จะต้องถูกต้องและมีไม่ขัดต่อกฏเกณฑ์ Constraints หรือ ความสัมพันธ์ท์ตั้งไว้ (Database Schema Constraints)
- I - Isolation คือ การทำ Transaction ที่เป็นแบบ Concurrent จะต้องแยกออกจากกันอย่างเด็ดขาด (FOR UPDATE , TRANSACTION ISOLATION LEVEL -> Pessimistic Locking)
- D - Durability คือ เมื่อ Transaction นั้นถูกบันทึกเรียบร้อย ข้อมูลนั้นๆจะต้องอยู่ ถาวร ไม่ว่าจะเกิดอะไรขึ้นกับ Database (WAL, T-Log, Redo Log และ หลัก Backup 3-2-1-1)
### ในความหมายของ ACID ฝั่งฐานข้อมูลรับผิดชอบเรื่องใด และฝั่งแอพลิเคชันรับผิดชอบเรื่องใด
- A - Atomicity
    - Database
        - BEGIN COMMIT ROLLBACK ให้ Transaction สำเร็จทั้งหมดหากไม่ก็ย้อนกลับทั้งหมด
    - Application
        - กำหนดว่าการทำงานไหนควรอยู่ใน Transaction เดียวกัน และจัดการ Error
- C - Consistency
    - Database
        - การทำ PK, FK, UNIQUE, CHECK และ Constraints ต่างๆ
    - Application
        - Business Rule Logic ที่ DB ไม่รู้ เช่น "ถอนเงินที่ต้องไม่เกินวงเงิน"
- I - Isolation
    - Database
        - จัดการ concurrent transactions และ Isolation Level
    - Application
        - เลือก/ใช้งาน transaction และ isolation level ให้เหมาะกับกรณี
- D - Durability
    - Database
        - ทำให้ข้อมูลที่ COMMIT แล้วไม่หาย เช่น transaction log/WAL
    - Application
        - ต้องรอ/ตรวจสอบว่า transaction COMMIT สำเร็จก่อนแจ้งผู้ใช้ว่าสำเร็จ