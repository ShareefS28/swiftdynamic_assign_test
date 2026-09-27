## Question
![](/assets/q_idempotency.png)
## Response Section
- Idempotency คือ การส่ง Request เดิมซ้ำกี่ครั้ง ผลลัพธ์ที่เกิดขึ้นกับระบบควรเทียบเท่ากับการส่งเพียงครั้งเดียว
```
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI()

# จำลอง database
idempotency_store = {}
orders = []


class CreateOrderRequest(BaseModel):
    product_id: int
    quantity: int


@app.post("/orders")
def create_order(
    data: CreateOrderRequest,
    idempotency_key: str = Header(...)
):
    # 1. ตรวจว่าเคยใช้ key นี้หรือยัง ซึ่ง Key นี้จะถูกเก็บใน table
    if idempotency_key in idempotency_store:
        return idempotency_store[idempotency_key]

    # 2. สร้าง order
    order = {
        "id": str(uuid4()),
        "product_id": data.product_id,
        "quantity": data.quantity
    }

    orders.append(order)

    response = {
        "message": "Order created",
        "order": order
    }

    # 3. จำ response เอาไว้
    idempotency_store[idempotency_key] = response

    return response
```