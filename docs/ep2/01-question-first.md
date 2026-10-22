# 2-1 질문을 먼저 적고 답을 한 줄로

!!! abstract "이 절에서 할 일"
    데이터를 열기 전에 질문을 한 줄로 적고, 코드를 돌린 뒤 답을 한 줄로 적는 틀을 익힌다.

먼저 [ep2-cvs.zip](../data/ep2-cvs.zip) 을 올리고 결제 기록을 읽는다.

```python
# 2편 실습 파일 묶음(zip)을 올리고 푼다
from google.colab import files
import zipfile, os
up = files.upload()
zipfile.ZipFile(list(up)[0]).extractall()
print(sorted(f for f in os.listdir() if f.startswith("cvs_")))
```

```text title="실행 결과"
Saving ep2-cvs.zip to ep2-cvs.zip
['cvs_cash.csv', 'cvs_sales.csv', 'cvs_stock.csv']
```

```python
import pandas as pd
enc = "utf-8-sig"
cvs = pd.read_csv("cvs_sales.csv", encoding=enc, parse_dates=["time"])
print(cvs.shape)
print(cvs.head(3))
```

```text title="실행 결과"
(7810, 5)
   receipt                time category  amount   pay
0    30001 2025-03-01 00:22:00       과자    1300  Card
1    30002 2025-03-01 00:26:00      도시락    1500  Card
2    30003 2025-03-01 00:34:00       음료    9200  Card
```

질문을 코드 위에 주석으로 먼저 쓴다. 그리고 답을 `print` 한 줄로 낸다.

```python
# 질문: 3월에 결제가 가장 많은 요일은? 가장 적은 요일과 몇 배 차이인가?
cvs["weekday"] = cvs["time"].dt.day_name().str[:3]
cnt = cvs["weekday"].value_counts()
print(cnt)
print(f"답: {cnt.idxmax()} 이 {cnt.max()}건으로 가장 많고, {cnt.idxmin()} 의 {cnt.max() / cnt.min():.2f}배다.")
```

```text title="실행 결과"
weekday
Sun    1404
Sat    1365
Mon    1144
Wed     987
Fri     987
Thu     979
Tue     944
Name: count, dtype: int64
답: Sun 이 1404건으로 가장 많고, Tue 의 1.49배다.
```

<div class="say" data-who="fly">3월엔 토요일이 다섯 번이잖아. 요일마다 날 수가 다른데 그대로 비교해도 돼?</div>
<div class="say" data-who="doc">좋은 의심이에요. 3월은 토 · 일 · 월이 5번씩이라, 2-9 에서 하루 평균으로 다시 봐요.</div>

!!! info "읽는 법"
    질문이 "가장 많은 요일"이니 답은 요일 이름과 숫자 하나면 된다. 차트가 필요한지는 답을 적어 본 뒤에 정한다. 이 답에는 날 수 차이가 섞여 있다는 점도 함께 적어 둔다.

!!! tip "바꿔 보기"
    질문을 "결제가 가장 많은 시각(0~23시)은?" 으로 바꾸고 `cvs["time"].dt.hour.value_counts()` 로 답을 한 줄로 적어 본다.

<label class="done"><input type="checkbox" data-step="2-1"> 2-1 끝냈어요</label>
