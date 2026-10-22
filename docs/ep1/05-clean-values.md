# 1-5 청소 ② "₩4,500", 날짜, "-"

!!! abstract "이 절에서 할 일"
    `₩4,500` 같은 글자를 숫자로, 날짜 글자를 날짜형으로, `-` 를 빈칸(NaT)으로 바꾼다.

```python
# ₩ 와 콤마를 지우고 숫자로 바꾼다
for col in ["price", "cost"]:
    cost[col] = pd.to_numeric(cost[col].str.replace("₩", "").str.replace(",", ""), errors="coerce")
# 날짜 글자를 날짜형으로. '-' 처럼 날짜가 아닌 것은 NaT(빈 날짜)가 된다
cost["updated"] = pd.to_datetime(cost["updated"], errors="coerce")
print(cost)
print(cost.dtypes)
```

```text title="실행 결과"
         menu  price  cost    updated
0   Americano   4500  1200 2025-01-02
1      Latte    5000  1600 2025-01-02
3    Iced Tea   5500  1100 2025-05-20
4  Cheesecake   6000  2400 2025-03-11
5  Croissant    3500  1300        NaT
menu               object
price               int64
cost                int64
updated    datetime64[ns]
dtype: object
```

<div class="say" data-who="robo" data-state="success">삐빅, 숫자가 됐어. 이제 더할 수 있어!</div>

!!! info "읽는 법"
    `errors="coerce"` 는 "바꿀 수 없는 값은 멈추지 말고 빈칸으로" 라는 뜻이다. Croissant 의 `-` 가 `NaT` 가 됐다. `price` 와 `cost` 가 `int64` 가 되어 이제 계산할 수 있다.

!!! tip "바꿔 보기"
    `errors="coerce"` 를 빼고 `pd.to_datetime(cost["updated"])` 만 실행해 본다. `-` 때문에 오류가 나는 것을 확인한다.

<label class="done"><input type="checkbox" data-step="1-5"> 1-5 끝냈어요</label>
