# 0-4 이것만 알면 코드를 읽는다

!!! abstract "이 절에서 할 일"
    이 연습장 코드의 90% 는 아래 일곱 가지 모양으로 되어 있다. 모양과 뜻을 짝지어 둔다.

| 모양 | 뜻 | 예 |
|---|---|---|
| `이름 = 값` | 오른쪽 값을 왼쪽 이름에 담아 둔다 | `shop = "Cafe Koi"` |
| `print(...)` | 괄호 안을 화면에 보여 준다 | `print("store:", shop)` |
| `# 설명` | `#` 뒤는 사람에게 하는 말. 실행되지 않는다 | `# 메뉴판을 읽는다` |
| `{"키": 값}` | 사전(dict). 짝을 지어 둔 작은 표 | `{"Latte": 5000}` |
| `표["열 이름"]` | 표에서 열 하나를 꺼낸다 | `menu["price"]` |
| `표[조건]` | 조건에 맞는 줄만 남긴다 | `menu[menu["price"] >= 5000]` |
| `값.함수()` | 값에 기능을 적용한다 | `menu["price"].mean()` → 평균 |

0-3 에서 읽은 `menu` 로 일곱 가지를 한 셀에서 모두 써 본다.

```python
shop = "Cafe Koi"                      # 이름 = 값
print("store:", shop)                  # 괄호 안을 화면에 보여 준다
price = {"Americano": 4500, "Latte": 5000}   # 사전: 짝을 지어 둔 표
print("latte:", price["Latte"])
print(menu["price"])                   # 표에서 열 하나 꺼내기
print(menu[menu["price"] >= 5000])     # 조건에 맞는 줄만
print("mean price:", menu["price"].mean())   # 값.함수()
```

```text title="실행 결과"
store: Cafe Koi
latte: 5000
0    4500
1    5000
2    5500
3    6000
4    3500
Name: price, dtype: int64
         menu category  price  cost
1       Latte    Drink   5000  1600
2    Iced Tea    Drink   5500  1100
3  Cheesecake  Dessert   6000  2400
mean price: 4900.0
```

<div class="say" data-who="fly">5000원짜리 라테는 왜 남았어? 5000보다 큰 것만 아니야?</div>
<div class="say" data-who="doc">`>=` 는 "크거나 같다"예요. 같은 것도 남겨요.</div>

!!! info "읽는 법"
    `menu["price"] >= 5000` 은 줄마다 True / False 를 만든다. `menu[ ... ]` 로 감싸면 True 인 줄(1, 2, 3번)만 남는다. 평균 4900.0 은 (4500 + 5000 + 5500 + 6000 + 3500) ÷ 5 다.

!!! tip "바꿔 보기"
    `>= 5000` 을 `< 5000` 으로 바꿔 본다. 아메리카노와 크루아상 두 줄이 남는다.

<label class="done"><input type="checkbox" data-step="0-4"> 0-4 를 끝냈어요</label>
