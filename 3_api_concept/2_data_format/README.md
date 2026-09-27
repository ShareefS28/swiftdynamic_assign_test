## Question
![](/assets/q_data_format.png)
## Response Section
ข้อมูลตัวอย่าง
```
{
  "id": 1001,
  "name": "John",
  "age": 30,
  "active": true
}
```
### JSON
JSON จะส่งข้อมูลเป็น TEXT
- ข้อดี
    - สามารถอ่านเข้าใจได้ง่าย
    - ใช้กับ REST API ได้ง่าย
    - รองรับ Programming หลายภาษา
    - มีความยืดหยุ่น
- ข้อเสีย
    - ข้อมูลมีขนาดใหญ่
    - type safety ต่ำ
    - performance อาจทำได้ไม่ดี

### Protocol Buffer
Protocol Buffer จะส่งข้อมูลเป็นแบบ Serialization Format กับ Binary
- ข้อดี
    - ข้อมูลมีขนาดเล็ก
    - performance เร็ว
    - type safety สูง ต้องมีการทำ Schema
- ข้อเสีย
    - อ่านเข้าใจได้ยาก
    - ต้องมี Schema ที่กำหนดแต่ละ Field
    - Front-end นำไปใช้ยาก
    - เหมาะกับงานที่ต้องเป็น service-to-service communication หรือ Microservice
