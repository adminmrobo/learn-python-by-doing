# 3-1 글자 가격을 숫자로

!!! abstract "이 절에서 할 일"
    "₩39,000" 처럼 글자로 된 원화 가격을 숫자로 바꾸고, 값이 없는 상품을 따로 빼 둔다.

[ep3-shop.zip](../data/ep3-shop.zip) 을 올린다.

```python
# 3편 실습 파일 묶음(zip)을 올리고 푼다
from google.colab import files
import zipfile, os
up = files.upload()
zipfile.ZipFile(list(up)[0]).extractall()
print(sorted(f for f in os.listdir() if f.startswith(("shop_", "fx_", "ai_"))))
```

```text title="실행 결과"
Saving ep3-shop.zip to ep3-shop.zip
['ai_pricetag.json', 'fx_2025_backup.csv', 'shop_items.csv', 'shop_orders_global.csv']
```

```python
import pandas as pd
enc = "utf-8-sig"
items = pd.read_csv("shop_items.csv", encoding=enc)
items["krw"] = pd.to_numeric(items["price"].str.replace("₩", "").str.replace(",", ""), errors="coerce")
print(items)
print("no price:", items.loc[items["krw"].isna(), "item"].tolist())
items = items.dropna(subset=["krw"])      # 가격이 없는 상품은 가격표에서 뺀다
```

```text title="실행 결과"
       item name_ko     price       krw
0       Tee     티셔츠   ₩19,000   19000.0
1     Shirt      셔츠   ₩39,000   39000.0
2      Knit      니트   ₩59,000   59000.0
3     Denim     청바지   ₩89,000   89000.0
4      Coat      코트  ₩189,000  189000.0
5       Cap      모자   ₩25,000   25000.0
6     Socks      양말    ₩6,000    6000.0
7  Tote bag     토트백         -       NaN
no price: ['Tote bag']
```

<div class="say" data-who="asst">토트백은 왜 가격이 '-' 예요?</div>
<div class="say" data-who="doc">아직 값을 안 정한 상품이에요. 빼 두고 사장님께 물어봐요.</div>

!!! info "읽는 법"
    1-5 와 같은 청소다. `₩` 와 `,` 를 지우면 `"39000"` 이라는 글자가 되고, `to_numeric` 이 숫자로 바꾼다. `-` 는 숫자가 될 수 없어 `NaN` 이 됐다. 가격표에 남은 상품은 7개다.

!!! tip "바꿔 보기"
    `dropna(subset=["krw"])` 줄을 지우고 실행해 `items` 에 토트백이 남는 것을 확인한다. 확인했으면 되돌린다.

<label class="done"><input type="checkbox" data-step="3-1"> 3-1 끝냈어요</label>
