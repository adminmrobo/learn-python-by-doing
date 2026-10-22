# 1-6 배달앱 주문 JSON 읽기

!!! abstract "이 절에서 할 일"
    배달앱이 보내 준 주문 응답(JSON)을 열어 `status` 를 확인하고, 주문 목록을 표로 바꾼다.

```python
# JSON 은 사전(dict) 모양으로 읽힌다. 표는 "orders" 안에 있다
import json
with open("koi_delivery.json", encoding="utf-8") as f:
    reply = json.load(f)
print(reply["status"], reply["month"], reply["count"])
delivery = pd.DataFrame(reply["orders"])
delivery["amount"] = delivery["qty"] * delivery["price"]
print(delivery.head())
print("orders:", len(delivery), "/ total:", delivery["amount"].sum())
```

```text title="실행 결과"
ok 2025-07 24
  order_id        date        menu  qty  price  amount
0   D-2512  2025-07-01   Americano    2   4500    9000
1   D-2511  2025-07-03    Iced Tea    3   5500   16500
2   D-2516  2025-07-03    Iced Tea    2   5500   11000
3   D-2508  2025-07-04  Cheesecake    1   6000    6000
4   D-2509  2025-07-04    Iced Tea    2   5500   11000
orders: 24 / total: 235000
```

<div class="say" data-who="asst">status 가 ok 가 아니면요?</div>
<div class="say" data-who="doc">그땐 표로 바꾸기 전에 멈춰야 해요. 비어 있는 응답일 수 있거든요.</div>

!!! info "읽는 법"
    `reply` 는 사전이다. `reply["orders"]` 는 주문 24건짜리 목록이고, `pd.DataFrame` 이 목록의 항목 하나를 한 줄로 만든다. 7월 배달 매출은 235,000원이다.

!!! tip "바꿔 보기"
    `print(reply.keys())` 를 실행해 이 응답에 어떤 칸들이 있는지 본다.

<label class="done"><input type="checkbox" data-step="1-6"> 1-6 끝냈어요</label>
