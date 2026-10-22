# 3-4 곱할까 나눌까, 그리고 100엔

!!! abstract "이 절에서 할 일"
    원화 가격을 외화로 바꿀 때 곱하는지 나누는지 정하고, 은행 고시의 '100엔 기준'과 yfinance 의 '1엔 기준'을 섞지 않는다.

```python
rate = fx.iloc[-1]                     # 마지막 영업일 환율
print(rate)
# 1달러 = 1,4xx원 이므로, 원 → 달러는 '나누기'
tag = items[["item", "krw"]].copy()
tag["usd"] = (tag["krw"] / rate["USDKRW=X"]).round(2)
tag["jpy"] = (tag["krw"] / rate["JPYKRW=X"]).round(0)      # yfinance 는 1엔 기준
tag["cny"] = (tag["krw"] / rate["CNYKRW=X"]).round(1)
print(tag)
print("bank notice style: 100 JPY =", round(rate["JPYKRW=X"] * 100, 1), "KRW")
```

```text title="실행 결과"
CNYKRW=X     206.750
JPYKRW=X       9.433
USDKRW=X    1467.300
Name: 2025-12-31 00:00:00, dtype: float64
    item       krw     usd      jpy    cny
0    Tee   19000.0   12.95   2014.0   91.9
1  Shirt   39000.0   26.58   4134.0  188.6
2   Knit   59000.0   40.21   6255.0  285.4
3  Denim   89000.0   60.66   9435.0  430.5
4   Coat  189000.0  128.81  20036.0  914.1
5    Cap   25000.0   17.04   2650.0  120.9
6  Socks    6000.0    4.09    636.0   29.0
bank notice style: 100 JPY = 943.3 KRW
```

<div class="say" data-who="asst">1,467.3으로 곱해요, 나눠요?</div>
<div class="say" data-who="doc">1달러가 1,467.3원이니까, 원을 달러로 바꿀 땐 나눠요.</div>

!!! info "읽는 법"
    단위를 말로 적으면 헷갈리지 않는다. "원 ÷ (원/달러) = 달러". 은행 창구는 엔화를 **100엔에 943.3원** 처럼 고시하지만, yfinance 의 `JPYKRW=X` 는 **1엔에 9.433원**이다. 100엔 고시 숫자로 나누면 엔화 가격이 100분의 1로 나온다. 3-9 에서 이 실수를 실제로 잡는다.

!!! tip "바꿔 보기"
    `/` 를 `*` 로 바꿔 티셔츠가 몇 달러로 나오는지 본다. 말이 안 되는 숫자가 나오면 방향이 틀린 것이다.

<label class="done"><input type="checkbox" data-step="3-4"> 3-4 끝냈어요</label>
