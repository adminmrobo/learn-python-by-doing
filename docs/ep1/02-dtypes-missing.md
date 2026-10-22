# 1-2 자료형과 빈칸부터

!!! abstract "이 절에서 할 일"
    계산하기 전에 열마다 자료형(dtype)과 빈칸 수, 메뉴별 줄 수를 확인한다.

```python
# 열마다 자료형, 빈칸(NaN) 수, 메뉴별 줄 수
print(sales.dtypes)
print(sales.isna().sum())
print(sales["menu"].value_counts())
```

```text title="실행 결과"
receipt_id             int64
date          datetime64[ns]
menu                  object
qty                    int64
price                  int64
discount               int64
customer              object
dtype: object
receipt_id      0
date            0
menu            0
qty             0
price           0
discount        0
customer      697
dtype: int64
menu
Americano     4640
Latte         3396
Croissant     3131
Cheesecake    1680
Iced Tea      1390
Name: count, dtype: int64
```

<div class="say" data-who="fly">손님 유형이 697칸 비었네. 그 줄은 버려?</div>
<div class="say" data-who="doc">아직요. 매출은 멀쩡하니 손님 유형만 '모름'인 거예요.</div>

!!! info "읽는 법"
    `date` 가 `datetime64[ns]` 면 날짜형으로 잘 읽힌 것이다. 금액 열이 `int64` 라 바로 더할 수 있다. `customer` 의 빈칸 697개는 포스기에서 손님 유형을 안 누른 줄이다.

!!! tip "바꿔 보기"
    `sales["customer"].value_counts(dropna=False)` 로 빈칸(NaN)까지 함께 세어 본다.

<label class="done"><input type="checkbox" data-step="1-2"> 1-2 끝냈어요</label>
