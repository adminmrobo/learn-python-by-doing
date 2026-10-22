# 1-10 공백 지우고 merge, 합계까지 맞추기

!!! abstract "이 절에서 할 일"
    원가표 이름의 공백을 지우고 `merge` 로 붙인 뒤, 줄 수와 빈칸 수로 제대로 붙었는지 확인한다.

```python
# 이름 끝 공백을 지우고, 판매 기록 왼쪽에 원가를 붙인다
cost["menu"] = cost["menu"].str.strip()
m = sales.drop(columns="unit_cost").merge(cost[["menu", "cost"]], on="menu", how="left")
print("rows:", len(sales), "->", len(m))
print("missing cost:", m["cost"].isna().sum())
m["cogs"] = m["qty"] * m["cost"]        # 재료비 = 수량 × 한 개 원가
print(m[["menu", "qty", "net", "cost", "cogs"]].head())
```

```text title="실행 결과"
rows: 14237 -> 14237
missing cost: 0
         menu  qty   net  cost  cogs
0   Croissant    1  3500  1300  1300
1  Cheesecake    1  5500  2400  2400
2   Americano    2  9000  1200  2400
3       Latte    1  4500  1600  1600
4   Americano    1  4500  1200  1200
```

<div class="say" data-who="robo" data-state="success">삐빅! 줄 수 그대로, 빈칸 0개. 다 붙었어!</div>

!!! info "읽는 법"
    `how="left"` 는 왼쪽 표(판매 기록)의 줄을 하나도 버리지 않는다. 붙인 뒤 줄 수가 14,237 → 14,237 로 같고 빈칸이 0 이면 제대로 붙은 것이다. 줄 수가 늘었다면 원가표에 같은 메뉴가 두 번 있다는 뜻이다.

!!! tip "바꿔 보기"
    `str.strip()` 줄을 지우고(앞 절 상태로) 다시 실행하면 `missing cost` 가 몇이 되는지 본다. 그다음 되돌린다.

<label class="done"><input type="checkbox" data-step="1-10"> 1-10 끝냈어요</label>
