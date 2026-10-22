# 1-8 새 열: 음료/디저트 분류와 순매출

!!! abstract "이 절에서 할 일"
    메뉴를 음료/디저트로 나누는 열(map)과, 수량 × 단가 − 할인으로 순매출 열을 만든다.

```python
# 메뉴 → 분류 사전
kind = {"Americano": "Drink", "Latte": "Drink", "Iced Tea": "Drink",
        "Cheesecake": "Dessert", "Croissant": "Dessert"}
sales["category"] = sales["menu"].map(kind)
# 순매출 = 수량 × 단가 − 할인
sales["net"] = sales["qty"] * sales["price"] - sales["discount"]
print(sales[["menu", "category", "qty", "price", "discount", "net"]].head())
print("unmapped:", sales["category"].isna().sum())
print("total net:", sales["net"].sum())
```

```text title="실행 결과"
         menu category  qty  price  discount   net
0   Croissant  Dessert    1   3500         0  3500
1  Cheesecake  Dessert    1   6000       500  5500
2   Americano    Drink    2   4500         0  9000
3       Latte    Drink    1   5000       500  4500
4   Americano    Drink    1   4500         0  4500
unmapped: 0
total net: 108381000
```

<div class="say" data-who="robo" data-state="success">삐빅, 분류 빈칸 0개. 다 짝을 찾았어.</div>

!!! info "읽는 법"
    열끼리 계산하면 같은 줄끼리 계산된다. 3번 줄은 라테 1개 5,000원에서 단골 할인 500원을 뺀 4,500원이다. 한 해 순매출은 108,381,000원이다.

!!! tip "바꿔 보기"
    `kind` 사전에서 `"Croissant"` 를 지우고 다시 실행한다. `unmapped` 가 크루아상 줄 수만큼 늘어난다. 확인했으면 되돌린다.

<label class="done"><input type="checkbox" data-step="1-8"> 1-8 끝냈어요</label>
