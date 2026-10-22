# 1편 카페 Koi의 장부를 연다

카페 Koi 사장님이 2025년 한 해 장부를 들고 왔다. 판매 기록, 지저분한 원가표 엑셀, 배달앱 주문, 고정비, 원두 재고. 이 편에서는 파일을 읽고, 청소하고, 붙이고, **합계가 맞는지 확인한 뒤에** 월별 손익 그림을 그린다. 열세 절, 모두 합쳐 2시간쯤 걸린다.

<div class="say" data-who="asst">장부를 열면 제일 먼저 뭘 봐요?</div>
<div class="say" data-who="doc">몇 줄인지, 빈칸이 몇 개인지부터요.</div>

| 절 | 할 일 |
|---|---|
| [1-1 판매 기록 읽고 모양 보기](01-read-sales.md) | read_csv, shape, head |
| [1-2 자료형과 빈칸부터](02-dtypes-missing.md) | dtypes, isna, value_counts |
| [1-3 지저분한 원가표 엑셀 날것으로 보기](03-raw-excel.md) | read_excel(header=None) |
| [1-4 청소 ① 제목 줄, 빈 행, 열 이름 공백](04-clean-rows.md) | skiprows, dropna, str.strip |
| [1-5 청소 ② "₩4,500", 날짜, "-"](05-clean-values.md) | str.replace, to_numeric, to_datetime |
| [1-6 배달앱 주문 JSON 읽기](06-json.md) | json.load, DataFrame |
| [1-7 열 고르고 조건 거르기](07-select-filter.md) | 열, 조건, &, query |
| [1-8 새 열: 음료/디저트 분류와 순매출](08-new-columns.md) | 열 계산, map |
| [1-9 map 으로 원가 붙이기, 그런데 두 메뉴가 빈다](09-map-trap.md) | dict(zip), map, repr |
| [1-10 공백 지우고 merge, 합계까지 맞추기](10-strip-merge.md) | str.strip, merge(how='left') |
| [1-11 월별 손익표와 CH-01 월별 손익 막대](11-monthly-pl.md) | groupby, 고정비, 막대 + 선 |
| [1-12 검증 세 가지, 잡아낸 것 바로잡기](12-checks.md) | 줄 수 · 합계 · 빈칸, drop_duplicates |
| [1-13 CH-02 재고 폭포](13-stock-waterfall.md) | 사칙검증, ax.bar(bottom=) |

<a class="colab" data-nb="ep1.ipynb">▶ 1편 노트북을 Colab 에서 열기</a>

!!! tip "준비물"
    [ep1-cafe.zip](../data/ep1-cafe.zip) 하나. 0-3 처럼 압축을 풀지 않고 그대로 올린다.

| 파일 | 내용 |
|---|---|
| koi_sales.csv | 2025년 영수증 줄 14,237줄 (영수증 번호, 날짜, 메뉴, 수량, 단가, 할인, 손님 유형) |
| koi_cost.xlsx | 메뉴 원가표. 제목 줄 · 빈 행 · ₩ 글자 · 숨은 공백이 섞인 엑셀 |
| koi_delivery.json | 배달앱 7월 주문 응답 (JSON) |
| koi_fixed.csv | 월별 고정비 (임대료, 인건비, 공과금) |
| koi_stock.csv | 4월 원두 재고 변동 (kg) |
