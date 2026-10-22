# 1-7 열 고르고 조건 거르기

!!! abstract "이 절에서 할 일"
    열 하나 · 여러 열 · 조건 거르기 · `query` 네 가지를 차례로 해 본다.

```python
# 열 하나, 여러 열
print(sales["menu"].head(3))
print(sales[["date", "menu", "qty"]].head(3))
# 조건: 7월 줄만
july = sales[sales["date"].dt.month == 7]
print("July rows:", len(july))
# 조건 두 개: 아이스티를 3개 이상 산 줄
big_tea = sales[(sales["menu"] == "Iced Tea") & (sales["qty"] >= 3)]
print("Iced Tea x3+:", len(big_tea))
# 같은 조건을 글자로
print(len(sales.query("menu == 'Iced Tea' and qty >= 3")))
```

```text title="실행 결과"
0     Croissant
1    Cheesecake
2     Americano
Name: menu, dtype: object
        date        menu  qty
0 2025-01-01   Croissant    1
1 2025-01-01  Cheesecake    1
2 2025-01-01   Americano    2
July rows: 1382
Iced Tea x3+: 233
233
```

<div class="say" data-who="fly">& 대신 and 쓰면 안 돼?</div>
<div class="say" data-who="doc">표의 조건끼리는 & 예요. 괄호도 꼭 씌우고요. query 안에서는 and 를 써요.</div>

!!! info "읽는 법"
    `sales["date"].dt.month == 7` 은 줄마다 True/False 를 만들고, `sales[...]` 가 True 인 줄만 남긴다. 7월은 1,382줄, 아이스티 3개 이상은 233줄이다.

!!! tip "바꿔 보기"
    `== 7` 을 `== 1` 로 바꿔 1월 줄 수와 비교해 본다. 아이스티 줄은 여름에 몰려 있다.

<label class="done"><input type="checkbox" data-step="1-7"> 1-7 끝냈어요</label>
