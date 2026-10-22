# 4편 가격을 바꾸면 이익이 움직인다

카페 Koi 사장님이 다시 왔다. "원두값이 오르고 환율도 올랐어요. 커피값을 올려야 할까요?" 이 편은 두 부분이다. 앞 세 절은 **데이터를 여러 방향으로 잘라 보는 법**(데이터 큐브), 뒤 다섯 절은 **가정을 바꿔 가며 이익을 계산하는 법**(민감도)이다. 1편 데이터를 그대로 쓴다. 여덟 절, 2시간쯤 걸린다.

<div class="say" data-who="asst">원두값이 오르면 커피값도 올려야 해요?</div>
<div class="say" data-who="doc">얼마나 올려야 하는지 그림으로 볼까요?</div>

| 절 | 할 일 |
|---|---|
| [4-1 데이터 큐브: 월 × 요일 × 고객 유형](01-data-cube.md) | groupby 3축, MultiIndex |
| [4-2 한 면 잘라 보기 · CH-14](02-slice.md) | xs, unstack, heatmap |
| [4-3 3D 산점, 정말 읽히나 · CH-15](03-3d-scatter.md) | projection='3d' |
| [4-4 가정은 사전에, 계산은 격자로](04-assumptions-grid.md) | dict, 함수, meshgrid |
| [4-5 판매가 × 원두 단가 이익 등고선 · CH-16](05-contour.md) | contourf, contour(levels=[0]) |
| [4-6 가정 바꾸기: 환율이 오르면](06-change-fx.md) | 사전 복사, 다시 계산 |
| [4-7 3D 곡면 vs 2D 등고선](07-surface-vs-contour.md) | plot_surface, subplots |
| [4-8 보고서용으로 저장하고 내려받기](08-save-download.md) | savefig(dpi), files.download |

<a class="colab" data-nb="ep4.ipynb">▶ 4편 노트북을 Colab 에서 열기</a>

!!! tip "준비물"
    [ep1-cafe.zip](../data/ep1-cafe.zip) 하나. 0-3 처럼 압축을 풀지 않고 그대로 올린다.

| 파일 | 내용 |
|---|---|
| koi_sales.csv | 1편과 같은 2025년 영수증 줄. 이번에는 손님 유형(`customer`)을 주로 쓴다 |
| koi_fixed.csv | 1편과 같은 월별 고정비 |
