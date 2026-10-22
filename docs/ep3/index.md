# 3편 해외 손님에게 가격을 알려 주자

의류 쇼핑몰에 해외 주문이 늘었다. 사장님 부탁은 두 가지다. "원화 가격표를 달러 · 엔 · 위안으로도 보여 주고 싶어요. 그리고 해외 주문이 원화로 얼마였는지 다시 계산해 주세요." 이 편에서는 **회사 밖 데이터(환율)** 를 받아 와 붙인다. 아홉 절, 2시간쯤 걸린다.

<div class="say" data-who="asst">달러로 얼마예요? 하고 물으면 뭐라고 해요?</div>
<div class="say" data-who="doc">그날 환율로 한번 나눠 볼까요?</div>

| 절 | 할 일 |
|---|---|
| [3-1 글자 가격을 숫자로](01-text-price.md) | str.replace, to_numeric, dropna |
| [3-2 yfinance 로 환율 받기](02-yfinance.md) | yf.download, .empty, 백업 CSV |
| [3-3 통화 세 개를 한 번에](03-three-currencies.md) | melt, groupby, unstack |
| [3-4 곱할까 나눌까, 그리고 100엔](04-multiply-or-divide.md) | krw ÷ 환율, 단위 |
| [3-5 주말엔 환율이 없다 · CH-10](05-weekend-ffill.md) | merge, reindex, ffill |
| [3-6 단순 평균 환율 vs 주문 가중 평균 환율 · CH-11](06-weighted-rate.md) | 가중 평균 |
| [3-7 환율과 해외 주문 수 · CH-12](07-rate-vs-orders.md) | scatter, polyfit, corr |
| [3-8 $0.50 단위로 반올림한 표시가 · CH-13](08-rounded-tag.md) | 반올림, 차이, axhline |
| [3-9 AI 가격표 JSON 검증하고 저장](09-check-ai-tag.md) | json, 사칙 검증, to_csv |

<a class="colab" data-nb="ep3.ipynb">▶ 3편 노트북을 Colab 에서 열기</a>

!!! tip "준비물"
    [ep3-shop.zip](../data/ep3-shop.zip) 하나. 0-3 처럼 압축을 풀지 않고 그대로 올린다.

| 파일 | 내용 |
|---|---|
| shop_items.csv | 상품 8개와 원화 가격. 가격은 "₩39,000" 같은 글자, 하나는 "-" |
| shop_orders_global.csv | 2025년 해외 주문 1,533건 (미국 · 일본 · 중국, 그 나라 돈으로 낸 값). 주말 주문도 있다 |
| fx_2025_backup.csv | 2025년 영업일 환율 백업 (1달러 · 1엔 · 1위안이 몇 원인지). **연습용 값으로, 실제 고시 환율과 다르다** |
| ai_pricetag.json | AI 가 만들어 준 외국어 가격표. 검증 전이다 |
