# 1-12 검증 세 가지, 잡아낸 것 바로잡기

!!! abstract "이 절에서 할 일"
    그림을 믿기 전에 세 가지를 확인한다. ① 영수증이 한 번씩만 있나 ② 월별 합계가 전체와 같나 ③ 빈칸이 없나.

```python
# 검증 세 가지
c1 = m["receipt_id"].duplicated().sum()            # ① 두 번 찍힌 영수증 줄
c2 = pl["net"].sum() - m["net"].sum()               # ② 월별 합 − 전체 합 (0 이어야)
c3 = m[["net", "cost"]].isna().sum().sum()          # ③ 계산에 쓴 열의 빈칸
print("① duplicated receipts:", c1)
print("② monthly sum - total:", c2)
print("③ missing values:", c3)
```

```text title="실행 결과"
① duplicated receipts: 3
② monthly sum - total: 0
③ missing values: 0
```

①이 0 이 아니다. 어떤 줄인지 들여다본다.

```python
print(m.loc[m["receipt_id"].duplicated(keep=False), ["receipt_id", "date", "menu", "qty", "net"]])
```

```text title="실행 결과"
       receipt_id       date       menu  qty    net
4120    250419021 2025-04-19      Latte    2   9000
4121    250419021 2025-04-19      Latte    2   9000
9052    250819022 2025-08-19   Iced Tea    3  16500
9053    250819022 2025-08-19   Iced Tea    3  16500
13009   251129050 2025-11-29  Americano    2   9000
13010   251129050 2025-11-29  Americano    2   9000
```

똑같은 영수증이 두 번씩 찍혀 있다. 하나씩만 남기고 다시 모은다.

```python
m2 = m.drop_duplicates(subset="receipt_id")
pl2 = m2.groupby("month")[["net", "cogs"]].sum()
pl2["fixed"] = pl["fixed"]
pl2["profit"] = pl2["net"] - pl2["cogs"] - pl2["fixed"]
print("rows:", len(m), "->", len(m2))
print("profit change by month:")
print((pl2["profit"] - pl["profit"])[lambda s: s != 0])
print("duplicated now:", m2["receipt_id"].duplicated().sum())
```

```text title="실행 결과"
rows: 14237 -> 14234
profit change by month:
month
4     -5800
8    -13200
11    -6600
Name: profit, dtype: int64
duplicated now: 0
```

<div class="say" data-who="robo" data-state="wrong">삐빅! 같은 영수증이 3번 더 찍혔어.</div>
<div class="say" data-who="asst">고치니까 3줄이 빠지고, 이익이 4월, 8월, 11월에서 줄었어요.</div>
<div class="say" data-who="robo" data-state="success">삐빅! 이제 세 가지 다 통과!</div>

!!! info "읽는 법"
    ②와 ③은 0 으로 통과했지만 ①이 3 이다. ②는 "더하는 방법"이 맞는지를, ①은 "더할 재료"가 맞는지를 본다. 둘은 다른 검사라서 ②가 통과해도 ①이 틀릴 수 있다. 이후 계산은 `m2`, `pl2` 로 한다.

!!! warning "검증은 그림보다 먼저"
    1-11 의 그림은 중복 줄이 섞인 숫자로 그린 것이다. 차이는 작지만, 순서를 지키는 습관이 큰 실수를 막는다.

!!! tip "바꿔 보기"
    `subset="receipt_id"` 를 빼고 `m.drop_duplicates()` 로 해 본다. 줄 전체가 같은 경우만 지우므로 이번에는 결과가 같다.

<label class="done"><input type="checkbox" data-step="1-12"> 1-12 끝냈어요</label>
