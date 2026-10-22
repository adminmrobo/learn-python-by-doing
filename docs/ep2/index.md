# 2편 편의점은 언제 바쁜가

동네 편의점 사장님의 질문은 하나다. "언제 사람을 더 둬야 하지?" 이 편에서는 **질문을 먼저 한 줄로 적고**, 그 질문에 맞는 차트를 고른다. 막대, 선, 히스토그램, 히트맵, 벤포드 비교까지 차트 일곱 장(CH-03 ~ CH-09)을 그린다. 아홉 절, 2시간쯤 걸린다.

<div class="say" data-who="asst">차트부터 그리면 안 돼요?</div>
<div class="say" data-who="doc">질문 한 줄부터 적어 볼까요?</div>

| 절 | 할 일 |
|---|---|
| [2-1 질문을 먼저 적고 답을 한 줄로](01-question-first.md) | 질문 → 코드 → 답 한 줄 |
| [2-2 한글 라벨이 깨지면 영어로 다시](02-korean-labels.md) | rename(사전), 영어 라벨 |
| [2-3 평균이냐 합계냐 · CH-03](03-mean-or-sum.md) | estimator='sum', 평균 vs 합계 |
| [2-4 유통기한까지 며칠 남았나 · CH-04](04-expiry-buckets.md) | 날짜 빼기, pd.cut |
| [2-5 cumsum 으로 시재 다시 계산 · CH-05](05-cash-cumsum.md) | cumsum, 선 + annotate |
| [2-6 평균과 중앙값 · CH-06](06-mean-median.md) | mean, median, histplot |
| [2-7 시간대 × 요일 피벗 · CH-07](07-pivot-heatmap.md) | pivot_table, heatmap |
| [2-8 영수증 금액의 첫 자리 · CH-08](08-first-digit.md) | str[0], 벤포드 기대값 |
| [2-9 주말과 딱 떨어지는 금액 · CH-09](09-weekend-round.md) | day_name, % 10000, countplot |

<a class="colab" data-nb="ep2.ipynb">▶ 2편 노트북을 Colab 에서 열기</a>

!!! tip "준비물"
    [ep2-cvs.zip](../data/ep2-cvs.zip) 하나. 0-3 처럼 압축을 풀지 않고 그대로 올린다.

| 파일 | 내용 |
|---|---|
| cvs_sales.csv | 2025년 3월 결제 7,810건 (영수증 번호, 시각, 상품군, 금액, 결제수단). 상품군은 한글 |
| cvs_stock.csv | 3월 31일 밤 진열 상품 56줄의 유통기한 |
| cvs_cash.csv | 일별 현금 들어온 돈 · 나간 돈(은행 입금, 동전 교환) |
