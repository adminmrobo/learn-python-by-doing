# 4-4 가정은 사전에, 계산은 격자로

!!! abstract "이 절에서 할 일"
    이익 계산에 쓰는 가정을 사전 하나에 모으고, 판매가 × 원두 값의 모든 조합을 격자로 계산한다.

이제부터는 "만약에"를 계산한다. 숫자를 코드 곳곳에 흩어 두면 하나 바꿀 때 다른 곳을 빠뜨린다. **가정은 한곳(사전)에** 모은다.

```python
# 커피(아메리카노 · 라테) 한 달 잔 수: 2025년 실제 평균
coffee = sales[sales["menu"].isin(["Americano", "Latte"])]
base_cups = round(coffee.groupby("month")["qty"].sum().mean())
assume = {
    "base_cups": base_cups,   # 지금 가격일 때 한 달 잔 수
    "base_price": 4500,       # 지금 판매가 (원)
    "elasticity": -1.0,       # 값이 1% 오르면 잔 수가 1% 준다고 가정
    "grams": 18,              # 한 잔에 드는 원두 (g)
    "usdkrw": 1470,           # 환율 (3편, 12월 수준)
    "other": 600,             # 컵 · 우유 · 시럽 등 한 잔 기타 비용 (원)
    "fixed": 3_600_000,       # 커피에 나눠 준 한 달 고정비 (원)
}
def profit(price, bean_usd, a):
    """한 달 커피 이익(원). bean_usd = 원두 1kg 달러 가격"""
    cups = a["base_cups"] * (price / a["base_price"]) ** a["elasticity"]
    bean = bean_usd * a["usdkrw"] * a["grams"] / 1000     # 한 잔 원두값(원)
    return cups * (price - bean - a["other"]) - a["fixed"]
print(assume)
print("now ($14/kg, 4,500원):", round(profit(4500, 14, assume)))
```

```text title="실행 결과"
{'base_cups': 1105, 'base_price': 4500, 'elasticity': -1.0, 'grams': 18, 'usdkrw': 1470, 'other': 600, 'fixed': 3600000}
now ($14/kg, 4,500원): 300164
```

판매가 3,000~6,000원, 원두 1kg 8~30달러의 모든 조합을 한 번에 계산한다.

```python
prices = np.linspace(3000, 6000, 61)      # 50원 간격
beans  = np.linspace(8, 30, 45)           # 0.5달러 간격
P, B = np.meshgrid(prices, beans)
Z = profit(P, B, assume) / 1e4           # 만원
print("grid:", Z.shape, "/ max", round(Z.max()), "/ min", round(Z.min()))
```

```text title="실행 결과"
grid: (45, 61) / max 70 / min -94
```

<div class="say" data-who="asst">탄력성 -1.0 은 어디서 나온 숫자예요?</div>
<div class="say" data-who="doc">가정이에요. 그래서 사전에 이름을 붙여 둬요. 나중에 -1.5 로 바꿔 보기 쉽게요.</div>

!!! info "읽는 법"
    `meshgrid` 는 가격 61개 × 원두값 45개의 모든 짝을 만들어 준다. 함수에 격자를 통째로 넣으면 2,745칸이 한 번에 계산된다. 지금 상태(원두 $14, 4,500원)의 한 달 커피 이익은 300,164원이다.

!!! warning "이건 예측이 아니라 가정 계산이다"
    잔 수가 가격에 어떻게 반응할지(탄력성), 고정비를 얼마나 커피에 나눌지는 모두 가정이다. 결과는 "이 가정이라면" 으로 읽는다.

!!! tip "바꿔 보기"
    `"elasticity": -1.0` 을 `-1.5` 로 바꾸고 `now` 이익이 어떻게 변하는지 본다. 바꾼 뒤엔 되돌린다.

<label class="done"><input type="checkbox" data-step="4-4"> 4-4 끝냈어요</label>
