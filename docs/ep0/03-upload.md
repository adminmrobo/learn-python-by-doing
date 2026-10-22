# 0-3 실습 파일 올리기

!!! abstract "이 절에서 할 일"
    실습 파일 묶음(zip)을 Colab 에 올려 풀고, 그 안의 CSV 를 표로 읽어 본다.

편마다 실습 파일이 zip 하나로 묶여 있다. 0편은 카페 Koi 메뉴판 하나만 든 작은 묶음으로 연습한다.

1. [ep0-start.zip](../data/ep0-start.zip) 을 내 컴퓨터에 내려받는다. **압축은 풀지 않는다.**
2. 아래 코드를 새 셀에 붙여 넣고 실행한다. 셀 아래에 **[파일 선택]** 버튼이 나온다.
3. 버튼을 눌러 zip 파일 **하나만** 고른다. 압축은 셀이 알아서 푼다.

```python
# 실습 파일 묶음(zip)을 올리고 푼다. 실행하면 아래에 [파일 선택] 버튼이 나온다
from google.colab import files
import zipfile, os
up = files.upload()
zipfile.ZipFile(list(up)[0]).extractall()
print(sorted(f for f in os.listdir() if f.endswith((".csv", ".xlsx", ".json", ".txt"))))
```

```text title="실행 결과"
Saving ep0-start.zip to ep0-start.zip
['koi_menu.csv']
```

이제 풀린 파일을 표로 읽는다.

```python
# 메뉴판(CSV)을 표로 읽는다. 한글이 섞일 수 있는 CSV 는 utf-8-sig 로 연다
import pandas as pd
menu = pd.read_csv("koi_menu.csv", encoding="utf-8-sig")
print(menu)
```

```text title="실행 결과"
         menu category  price  cost
0   Americano    Drink   4500  1200
1       Latte    Drink   5000  1600
2    Iced Tea    Drink   5500  1100
3  Cheesecake  Dessert   6000  2400
4   Croissant  Dessert   3500  1300
```

<div class="say" data-who="asst">왼쪽 0, 1, 2… 는 제가 넣은 적 없는데요?</div>
<div class="say" data-who="doc">pandas 가 붙여 주는 줄 번호예요. 엑셀의 행 번호와 같아요.</div>

!!! info "읽는 법"
    `menu` 는 5줄 4열짜리 표(DataFrame)다. 한 줄이 메뉴 하나, `price` 는 판매가, `cost` 는 한 잔(한 개)의 재료비다. 단위는 원.

!!! warning "파일이 사라졌을 때"
    Colab 은 창을 닫거나 오래 두면 올린 파일이 지워진다. `FileNotFoundError` 가 나오면 이 업로드 셀을 다시 실행하고 그다음 셀부터 이어서 실행한다. 같은 zip 을 두 번 올리면 이름 뒤에 `(1)` 이 붙지만, 이 셀은 올라온 이름을 그대로 쓰므로 괜찮다.

!!! tip "바꿔 보기"
    `print(menu)` 를 `print(menu.shape)` 로 바꿔 본다. `(5, 4)` 가 나오면 5줄 4열이라는 뜻이다.

<label class="done"><input type="checkbox" data-step="0-3"> 0-3 을 끝냈어요</label>
