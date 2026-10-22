# 1-9 map 으로 원가 붙이기, 그런데 두 메뉴가 빈다

!!! abstract "이 절에서 할 일"
    원가표에서 메뉴 → 원가 사전을 만들어 붙여 보고, 못 찾은 줄이 왜 생기는지 본다.

```python
# 원가표의 두 열로 사전을 만든다 (엑셀의 VLOOKUP 자리)
unit = dict(zip(cost["menu"], cost["cost"]))
sales["unit_cost"] = sales["menu"].map(unit)
print("missing:", sales["unit_cost"].isna().sum())
print(sales.loc[sales["unit_cost"].isna(), "menu"].value_counts())
```

```text title="실행 결과"
missing: 6527
menu
Latte        3396
Croissant    3131
Name: count, dtype: int64
```

눈으로는 같은 이름인데 왜 못 찾았을까. `repr` 로 감춰진 글자까지 찍어 본다.

```python
print([repr(m) for m in cost["menu"]])
```

```text title="실행 결과"
["'Americano'", "'Latte '", "'Iced Tea'", "'Cheesecake'", "'Croissant '"]
```

<div class="say" data-who="asst">Latte 랑 Croissant 만 비었어요. 왜요?</div>
<div class="say" data-who="fly">'Latte ' 끝에 공백 하나. 그거 하나로 6,527줄이 날아갔어.</div>

!!! info "읽는 법"
    원가표 쪽 이름이 `'Latte '`, `'Croissant '` 로 끝에 공백이 있다. 사전은 글자가 **완전히 같아야** 짝을 찾으므로, 판매 기록의 `'Latte'` 와 짝이 되지 않는다. 메뉴 두 종류, 줄로는 6,527줄이 비었다.

!!! tip "바꿔 보기"
    `print(len("Latte"), len("Latte "))` 를 실행해 두 글자의 길이가 5 와 6 으로 다른 것을 확인한다.

<label class="done"><input type="checkbox" data-step="1-9"> 1-9 끝냈어요</label>
