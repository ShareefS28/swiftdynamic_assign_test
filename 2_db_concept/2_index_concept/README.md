## Question
![](/assets/q_indexing.png)
## Response Section
### ข้อดี
- ทำให้ Query อ่านข้อมูลได้เร็วขึ้น
- ช่วยเรื่อง ORDER BY, JOIN
- ช่วยเรื่อง ENFORCE ข้อมูลให้ถูกต้องในบางกรณี เช่น user มีได้แค่คนๆเดียว
### ข้อเสีย
- ใช้พื่นที่ DISK เพิ่ม
- INSERT / UPDATE / DELETE อาจช้าลง เพราะต้อง Update Index ที่เกี่ยวข้องด้วย
- Index ไม่ได้ทำให้ทุก Query เร็วขึ้น หาก DB ต้องอ่านข้อมูลจำนวนมากอยู่ดี
- Index เหมาะกับ Query Pattern ที่ต้องมีการพิจารณาร่วมด้วยว่าตอบโจทย์ไหม