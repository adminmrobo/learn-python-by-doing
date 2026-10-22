# 1-1 판매 기록 읽고 모양 보기

!!! abstract "이 절에서 할 일"
    판매 기록 CSV 를 표로 읽고, 줄 수 · 열 수와 첫 세 줄을 본다.

먼저 [ep1-cafe.zip](../data/ep1-cafe.zip) 을 올린다. 0-3 과 같은 셀이다.

```python
# 1편 실습 파일 묶음(zip)을 올리고 푼다
from google.colab import files
import zipfile, os
up = files.upload()
zipfile.ZipFile(list(up)[0]).extractall()
print(sorted(f for f in os.listdir() if f.startswith("koi_")))
```

```text title="실행 결과"
Saving ep1-cafe.zip to ep1-cafe.zip
['koi_cost.xlsx', 'koi_delivery.json', 'koi_fixed.csv', 'koi_sales.csv', 'koi_stock.csv']
```

판매 기록을 표로 읽는다. `parse_dates` 를 주면 날짜 글자가 처음부터 날짜형으로 읽힌다.

```python
# 판매 기록(CSV)을 표로 읽는다
import pandas as pd
enc = "utf-8-sig"
sales = pd.read_csv("koi_sales.csv", encoding=enc, parse_dates=["date"])
sales_raw = sales.copy()          # 나중에 비교할 원본을 따로 둔다
print("rows x cols:", sales.shape)
print(sales.head(3))
```

```text title="실행 결과"
rows x cols: (14237, 7)
   receipt_id       date        menu  qty  price  discount customer
0   250101001 2025-01-01   Croissant    1   3500         0  Regular
1   250101002 2025-01-01  Cheesecake    1   6000       500  Regular
2   250101003 2025-01-01   Americano    2   4500         0  Regular
```

<div class="say" data-who="asst">14,237줄이면 엑셀로도 열 수 있지 않아요?</div>
<div class="say" data-who="doc">열 수는 있어요. 그런데 월별로 묶고 검증하는 건 여기가 훨씬 빨라요.</div>

!!! info "읽는 법"
    `(14237, 7)` 은 영수증 줄 14,237개, 열 7개라는 뜻이다. 한 줄이 영수증의 메뉴 한 줄이다. `price` 는 한 개 값, `qty` 는 개수, `discount` 는 그 줄에서 깎아 준 금액이다(단골 할인). 금액 단위는 원.

!!! tip "바꿔 보기"
    `sales.head(3)` 을 `sales.tail(3)` 으로 바꿔 12월 31일 마지막 영수증을 본다.

<label class="done"><input type="checkbox" data-step="1-1"> 1-1 끝냈어요</label>
