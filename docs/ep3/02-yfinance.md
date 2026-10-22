# 3-2 yfinance 로 환율 받기

!!! abstract "이 절에서 할 일"
    yfinance 로 2025년 환율을 받아 보고, 받지 못했을 때(빈 표)는 멈추지 않고 백업 CSV 로 넘어가는 셀을 만든다.

yfinance 는 Yahoo Finance 의 공개 데이터를 표로 받아 주는 라이브러리다. **공식 서비스가 아니라서** 막히거나 모양이 바뀔 때가 있다. 그래서 바깥 데이터를 받는 셀은 늘 "받았나?"를 먼저 확인하고, 안 되면 백업으로 넘어가게 짠다.

```python
# Colab 에 없으면 설치: !pip install yfinance
import yfinance as yf
tickers = ["USDKRW=X", "JPYKRW=X", "CNYKRW=X"]      # 1달러 · 1엔 · 1위안 = 몇 원
live = yf.download(tickers, start="2025-01-02", end="2026-01-01", progress=False)
print("rows:", len(live), "/ empty:", live.empty)
if live.empty:
    print("받지 못했다 → 백업 CSV 를 쓴다")
else:
    print(live["Close"].tail(3))
```

```text title="실행 결과"
rows: 0 / empty: True
받지 못했다 → 백업 CSV 를 쓴다
```

이 연습장의 숫자는 모두 백업 CSV 로 만들었다. **Colab 에서 실제 환율을 받았더라도 다음 셀부터는 백업을 쓴다.** 그래야 결과를 이 페이지와 맞춰 볼 수 있다.

```python
fx = pd.read_csv("fx_2025_backup.csv", encoding=enc, parse_dates=["Date"], index_col="Date")
print(fx.shape)
print(fx.head(3))
print(fx.tail(2))
```

```text title="실행 결과"
(260, 3)
            CNYKRW=X  JPYKRW=X  USDKRW=X
Date                                    
2025-01-02    199.18     9.326    1458.7
2025-01-03    199.36     9.320    1458.1
2025-01-06    199.60     9.288    1455.6
            CNYKRW=X  JPYKRW=X  USDKRW=X
Date                                    
2025-12-30    206.73     9.436    1468.3
2025-12-31    206.75     9.433    1467.3
```

<div class="say" data-who="robo" data-state="confused">삐빅, 빈 표가 왔어. 그래도 멈추지 않았어!</div>
<div class="say" data-who="fly">빈 표인데 오류가 안 났다고? 그럼 모르고 넘어갈 수도 있잖아.</div>

!!! info "읽는 법"
    yfinance 는 접속에 실패해도 오류 대신 **빈 표**를 돌려줄 때가 많다. 그래서 `try/except` 만으로는 부족하고 `live.empty` 를 꼭 확인한다. 백업은 영업일 260일, 세 통화의 종가다. 1월 2일 1달러는 1,458.7원이다.

!!! warning "Colab 에서 실제로 받았다면"
    `live` 는 열 이름이 두 줄(MultiIndex: `Price` × `Ticker`)인 표로 온다. `live["Close"]` 로 종가만 꺼내면 백업 CSV 와 같은 모양이 된다. 값은 백업과 다르다.

!!! tip "바꿔 보기"
    `tickers` 에 `"EURKRW=X"` (유로)를 더해 본다. Colab 에서는 네 통화가 온다.

<label class="done"><input type="checkbox" data-step="3-2"> 3-2 끝냈어요</label>
