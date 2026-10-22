# 4-1 데이터 큐브: 월 × 요일 × 고객 유형

!!! abstract "이 절에서 할 일"
    1편 판매 기록을 다시 읽어 정리하고, 월 · 요일 · 고객 유형 세 방향으로 묶은 '데이터 큐브'를 만든다.

[ep1-cafe.zip](../data/ep1-cafe.zip) 을 다시 올린다(1편과 같은 파일). 1편에서 한 정리 두 가지(중복 영수증 지우기, 순매출 열)를 먼저 한다.

```python
# 1편 실습 파일 묶음(zip)을 다시 올리고 푼다
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

```python
import pandas as pd
enc = "utf-8-sig"
sales = pd.read_csv("koi_sales.csv", encoding=enc, parse_dates=["date"]).drop_duplicates(subset="receipt_id")
sales["net"] = sales["qty"] * sales["price"] - sales["discount"]
sales["month"] = sales["date"].dt.month
sales["weekday"] = sales["date"].dt.day_name().str[:3]
sales["customer"] = sales["customer"].fillna("Unknown")      # 빈칸은 '모름'으로
cube = sales.groupby(["month", "weekday", "customer"])["net"].sum()
print("cells:", len(cube), "= 12 months x 7 days x", sales["customer"].nunique(), "types")
print(cube.head(8))
```

```text title="실행 결과"
cells: 336 = 12 months x 7 days x 4 types
month  weekday  customer
1      Fri      Regular     551000
                Tourist     126000
                Unknown      72000
                Walk-in     809500
       Mon      Regular     315000
                Tourist      96000
                Unknown      54000
                Walk-in     439000
Name: net, dtype: int64
```

<div class="say" data-who="asst">표가 세로로 길게만 나와요. 이게 큐브예요?</div>
<div class="say" data-who="doc">세 방향 이름표(월 · 요일 · 유형)가 붙은 값 목록이에요. 상자를 펼쳐 놓은 모양이죠.</div>

!!! info "읽는 법"
    큐브는 "월 × 요일 × 고객 유형" 칸마다 순매출 합계가 하나씩 들어 있는 상자다. 칸은 336개다. 줄 이름이 세 겹(MultiIndex)이라서 원하는 방향으로 자르거나(4-2) 펼칠(unstack) 수 있다. 1편에서 빈칸이던 손님 유형은 `Unknown` 으로 채웠다.

!!! tip "바꿔 보기"
    `["month", "weekday", "customer"]` 에서 `"weekday"` 를 빼고 다시 실행해 칸 수가 어떻게 줄어드는지 본다.

<label class="done"><input type="checkbox" data-step="4-1"> 4-1 끝냈어요</label>
