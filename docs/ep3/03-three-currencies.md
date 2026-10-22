# 3-3 통화 세 개를 한 번에

!!! abstract "이 절에서 할 일"
    가로로 놓인 통화 세 열을 세로(긴) 표로 바꿔 한 번에 월평균을 내고, 다시 가로 표로 펼친다.

```python
# 가로 표 → 세로 표: 통화 이름이 한 열(ticker)로 내려온다
long = fx.reset_index().melt(id_vars="Date", var_name="ticker", value_name="krw")
print(long.head(4))
long["month"] = long["Date"].dt.month
monthly = long.groupby(["month", "ticker"])["krw"].mean().unstack("ticker").round(2)
print(monthly)
```

```text title="실행 결과"
        Date    ticker     krw
0 2025-01-02  CNYKRW=X  199.18
1 2025-01-03  CNYKRW=X  199.36
2 2025-01-06  CNYKRW=X  199.60
3 2025-01-07  CNYKRW=X  199.98
ticker  CNYKRW=X  JPYKRW=X  USDKRW=X
month                               
1         199.28      9.33   1453.61
2         198.95      9.51   1449.07
3         199.76      9.79   1452.49
4         197.41      9.89   1436.27
5         192.95      9.66   1395.61
6         190.63      9.46   1370.17
7         191.64      9.37   1375.52
8         193.52      9.40   1389.20
9         195.78      9.40   1395.80
10        199.87      9.36   1423.13
11        204.57      9.40   1455.78
12        206.81      9.45   1467.95
```

<div class="say" data-who="asst">세 통화를 따로따로 평균 내면 안 돼요?</div>
<div class="say" data-who="doc">돼요. 그런데 통화가 열 개면 열 줄이죠. 세로로 세우면 한 줄이에요.</div>

!!! info "읽는 법"
    `melt` 는 가로 표를 "날짜 · 통화 · 값" 세 열짜리 긴 표로 바꾼다. 긴 표는 `groupby` 한 번으로 모든 통화를 같이 계산할 수 있다. `unstack("ticker")` 는 다시 통화를 열로 펼친다. 달러는 12월이 가장 비쌌고(1,467.95원) 6월이 가장 쌌다(1,370.17원).

!!! tip "바꿔 보기"
    `.mean()` 을 `.max()` 로 바꿔 달마다 가장 높았던 환율을 본다.

<label class="done"><input type="checkbox" data-step="3-3"> 3-3 끝냈어요</label>
