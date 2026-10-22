"""3편 원고. build_episode.py 가 코드를 순서대로 실행하고 ⟦식⟧ 자리를 실행 결과로 채운다."""

TITLE = "3편 해외 손님에게 가격을 알려 주자"
ZIP = "ep3-shop.zip"
INTRO = ("의류 쇼핑몰에 해외 주문이 늘었다. 사장님 부탁은 두 가지다. \"원화 가격표를 달러 · 엔 · 위안으로도 보여 주고 싶어요. "
         "그리고 해외 주문이 원화로 얼마였는지 다시 계산해 주세요.\" 이 편에서는 **회사 밖 데이터(환율)** 를 받아 와 붙인다. "
         "아홉 절, 2시간쯤 걸린다.")
HEAD_TALK = [("asst", "달러로 얼마예요? 하고 물으면 뭐라고 해요?"), ("doc", "그날 환율로 한번 나눠 볼까요?")]
FILES = """| shop_items.csv | 상품 8개와 원화 가격. 가격은 "₩39,000" 같은 글자, 하나는 "-" |
| shop_orders_global.csv | 2025년 해외 주문 ⟦len(orders)|,⟧건 (미국 · 일본 · 중국, 그 나라 돈으로 낸 값). 주말 주문도 있다 |
| fx_2025_backup.csv | 2025년 영업일 환율 백업 (1달러 · 1엔 · 1위안이 몇 원인지). **연습용 값으로, 실제 고시 환율과 다르다** |
| ai_pricetag.json | AI 가 만들어 준 외국어 가격표. 검증 전이다 |"""
NEXT = "[4편 가격을 바꾸면 이익이 움직인다 →](../ep4/index.md)"

SECTIONS = [
dict(id="3-1", slug="01-text-price", title="글자 가격을 숫자로", short="str.replace, to_numeric, dropna",
 goal="\"₩39,000\" 처럼 글자로 된 원화 가격을 숫자로 바꾸고, 값이 없는 상품을 따로 빼 둔다.",
 cells=[
  dict(before="[ep3-shop.zip](../data/ep3-shop.zip) 을 올린다.",
       code='''# 3편 실습 파일 묶음(zip)을 올리고 푼다
from google.colab import files
import zipfile, os
up = files.upload()
zipfile.ZipFile(list(up)[0]).extractall()
print(sorted(f for f in os.listdir() if f.startswith(("shop_", "fx_", "ai_"))))''', prefix="Saving ep3-shop.zip to ep3-shop.zip\n",
       run='import os\nprint(sorted(f for f in os.listdir() if f.startswith(("shop_", "fx_", "ai_"))))'),
  dict(code='''import pandas as pd
enc = "utf-8-sig"
items = pd.read_csv("shop_items.csv", encoding=enc)
items["krw"] = pd.to_numeric(items["price"].str.replace("₩", "").str.replace(",", ""), errors="coerce")
print(items)
print("no price:", items.loc[items["krw"].isna(), "item"].tolist())
items = items.dropna(subset=["krw"])      # 가격이 없는 상품은 가격표에서 뺀다'''),
 ],
 talk=[("asst", "토트백은 왜 가격이 '-' 예요?"), ("doc", "아직 값을 안 정한 상품이에요. 빼 두고 사장님께 물어봐요.")],
 read="1-5 와 같은 청소다. `₩` 와 `,` 를 지우면 `\"39000\"` 이라는 글자가 되고, `to_numeric` 이 숫자로 바꾼다. `-` 는 숫자가 될 수 없어 `NaN` 이 됐다. "
      "가격표에 남은 상품은 ⟦len(items)⟧개다.",
 **{"try": "`dropna(subset=[\"krw\"])` 줄을 지우고 실행해 `items` 에 토트백이 남는 것을 확인한다. 확인했으면 되돌린다."}),

dict(id="3-2", slug="02-yfinance", title="yfinance 로 환율 받기", short="yf.download, .empty, 백업 CSV",
 goal="yfinance 로 2025년 환율을 받아 보고, 받지 못했을 때(빈 표)는 멈추지 않고 백업 CSV 로 넘어가는 셀을 만든다.",
 intro="yfinance 는 Yahoo Finance 의 공개 데이터를 표로 받아 주는 라이브러리다. **공식 서비스가 아니라서** 막히거나 모양이 바뀔 때가 있다. "
       "그래서 바깥 데이터를 받는 셀은 늘 \"받았나?\"를 먼저 확인하고, 안 되면 백업으로 넘어가게 짠다.",
 cells=[
  dict(code='''# Colab 에 없으면 설치: !pip install yfinance
import yfinance as yf
tickers = ["USDKRW=X", "JPYKRW=X", "CNYKRW=X"]      # 1달러 · 1엔 · 1위안 = 몇 원
live = yf.download(tickers, start="2025-01-02", end="2026-01-01", progress=False)
print("rows:", len(live), "/ empty:", live.empty)
if live.empty:
    print("받지 못했다 → 백업 CSV 를 쓴다")
else:
    print(live["Close"].tail(3))''',
       run='''live = pd.DataFrame()      # 이 페이지를 만든 곳은 Yahoo 에 접속할 수 없어 빈 표가 왔다
print("rows:", len(live), "/ empty:", live.empty)
if live.empty:
    print("받지 못했다 → 백업 CSV 를 쓴다")'''),
  dict(before="이 연습장의 숫자는 모두 백업 CSV 로 만들었다. **Colab 에서 실제 환율을 받았더라도 다음 셀부터는 백업을 쓴다.** 그래야 결과를 이 페이지와 맞춰 볼 수 있다.",
       code='''fx = pd.read_csv("fx_2025_backup.csv", encoding=enc, parse_dates=["Date"], index_col="Date")
print(fx.shape)
print(fx.head(3))
print(fx.tail(2))'''),
 ],
 talk=[("robo", "삐빅, 빈 표가 왔어. 그래도 멈추지 않았어!", "confused"),
       ("fly", "빈 표인데 오류가 안 났다고? 그럼 모르고 넘어갈 수도 있잖아.")],
 read="yfinance 는 접속에 실패해도 오류 대신 **빈 표**를 돌려줄 때가 많다. 그래서 `try/except` 만으로는 부족하고 `live.empty` 를 꼭 확인한다. "
      "백업은 영업일 ⟦len(fx)⟧일, 세 통화의 종가다. 1월 2일 1달러는 ⟦fx['USDKRW=X'].iloc[0]|,⟧원이다.",
 warn=("Colab 에서 실제로 받았다면", "`live` 는 열 이름이 두 줄(MultiIndex: `Price` × `Ticker`)인 표로 온다. `live[\"Close\"]` 로 종가만 꺼내면 백업 CSV 와 같은 모양이 된다. 값은 백업과 다르다."),
 **{"try": "`tickers` 에 `\"EURKRW=X\"` (유로)를 더해 본다. Colab 에서는 네 통화가 온다."}),

dict(id="3-3", slug="03-three-currencies", title="통화 세 개를 한 번에", short="melt, groupby, unstack",
 goal="가로로 놓인 통화 세 열을 세로(긴) 표로 바꿔 한 번에 월평균을 내고, 다시 가로 표로 펼친다.",
 cells=[dict(code='''# 가로 표 → 세로 표: 통화 이름이 한 열(ticker)로 내려온다
long = fx.reset_index().melt(id_vars="Date", var_name="ticker", value_name="krw")
print(long.head(4))
long["month"] = long["Date"].dt.month
monthly = long.groupby(["month", "ticker"])["krw"].mean().unstack("ticker").round(2)
print(monthly)''')],
 talk=[("asst", "세 통화를 따로따로 평균 내면 안 돼요?"), ("doc", "돼요. 그런데 통화가 열 개면 열 줄이죠. 세로로 세우면 한 줄이에요.")],
 read="`melt` 는 가로 표를 \"날짜 · 통화 · 값\" 세 열짜리 긴 표로 바꾼다. 긴 표는 `groupby` 한 번으로 모든 통화를 같이 계산할 수 있다. "
      "`unstack(\"ticker\")` 는 다시 통화를 열로 펼친다. 달러는 ⟦monthly['USDKRW=X'].idxmax()⟧월이 가장 비쌌고(⟦monthly['USDKRW=X'].max()|,⟧원) "
      "⟦monthly['USDKRW=X'].idxmin()⟧월이 가장 쌌다(⟦monthly['USDKRW=X'].min()|,⟧원).",
 **{"try": "`.mean()` 을 `.max()` 로 바꿔 달마다 가장 높았던 환율을 본다."}),

dict(id="3-4", slug="04-multiply-or-divide", title="곱할까 나눌까, 그리고 100엔", short="krw ÷ 환율, 단위",
 goal="원화 가격을 외화로 바꿀 때 곱하는지 나누는지 정하고, 은행 고시의 '100엔 기준'과 yfinance 의 '1엔 기준'을 섞지 않는다.",
 cells=[dict(code='''rate = fx.iloc[-1]                     # 마지막 영업일 환율
print(rate)
# 1달러 = 1,4xx원 이므로, 원 → 달러는 '나누기'
tag = items[["item", "krw"]].copy()
tag["usd"] = (tag["krw"] / rate["USDKRW=X"]).round(2)
tag["jpy"] = (tag["krw"] / rate["JPYKRW=X"]).round(0)      # yfinance 는 1엔 기준
tag["cny"] = (tag["krw"] / rate["CNYKRW=X"]).round(1)
print(tag)
print("bank notice style: 100 JPY =", round(rate["JPYKRW=X"] * 100, 1), "KRW")''')],
 talk=[("asst", "⟦rate['USDKRW=X']|,⟧으로 곱해요, 나눠요?"),
       ("doc", "1달러가 ⟦rate['USDKRW=X']|,⟧원이니까, 원을 달러로 바꿀 땐 나눠요.")],
 read="단위를 말로 적으면 헷갈리지 않는다. \"원 ÷ (원/달러) = 달러\". 은행 창구는 엔화를 **100엔에 ⟦round(rate['JPYKRW=X']*100,1)⟧원** 처럼 고시하지만, "
      "yfinance 의 `JPYKRW=X` 는 **1엔에 ⟦rate['JPYKRW=X']⟧원**이다. 100엔 고시 숫자로 나누면 엔화 가격이 100분의 1로 나온다. 3-9 에서 이 실수를 실제로 잡는다.",
 **{"try": "`/` 를 `*` 로 바꿔 티셔츠가 몇 달러로 나오는지 본다. 말이 안 되는 숫자가 나오면 방향이 틀린 것이다."}),

dict(id="3-5", slug="05-weekend-ffill", title="주말엔 환율이 없다 · CH-10", short="merge, reindex, ffill",
 goal="주말 주문에 붙일 환율이 없는 문제를 확인하고, 달력 날짜로 펴서 직전 영업일 환율로 채운 뒤 주문에 붙인다.",
 cells=[
  dict(code='''orders = pd.read_csv("shop_orders_global.csv", encoding=enc, parse_dates=["date"])
orders["fc"] = orders["qty"] * orders["unit_price"]          # 그 나라 돈으로 낸 금액
print(orders.head(3))
# 영업일 환율만 그대로 붙이면?
t1 = orders.merge(fx, left_on="date", right_index=True, how="left")
print("orders:", len(orders), "/ no rate:", t1["USDKRW=X"].isna().sum())
print(t1.loc[t1["USDKRW=X"].isna(), "date"].dt.day_name().value_counts())'''),
  dict(before="달력의 모든 날짜로 편 다음, 빈 날은 **바로 앞 영업일 값**으로 채운다(`ffill`). 1월 1일처럼 앞 값이 없는 날은 뒤 값으로 채운다(`bfill`).",
       code='''cal = pd.date_range("2025-01-01", "2025-12-31")
fxd = fx.reindex(cal).ffill().bfill()
fxd.index.name = "date"
print(fxd.loc["2025-01-03":"2025-01-06", ["USDKRW=X"]])
t2 = orders.merge(fxd, left_on="date", right_index=True, how="left")
print("no rate now:", t2["USDKRW=X"].isna().sum())'''),
  dict(before="CH-10. 영업일 점과 주말을 채운 선을 함께 그린다.",
       code='''import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8, 3))
ax.plot(fxd.index, fxd["USDKRW=X"], color="#D98E22", linewidth=1, label="Calendar (weekend filled)")
ax.plot(fx.index, fx["USDKRW=X"], ".", color="#1F3A5F", markersize=3, label="Business days")
ax.set(title="CH-10 USD/KRW 2025 (practice backup)", ylabel="KRW per USD")
ax.legend()
plt.show()''', alt="CH-10 2025년 원/달러 환율 선, 영업일 점과 주말 채운 선"),
 ],
 talk=[("fly", "토요일 주문은 무슨 환율로 계산해?"),
       ("doc", "규칙을 정하면 돼요. 여기선 '직전 영업일(금요일) 값'으로 해요.")],
 read="그냥 붙이면 주문 ⟦len(orders)|,⟧건 중 ⟦t1['USDKRW=X'].isna().sum()⟧건이 환율을 못 받는다. 거의 다 토 · 일 주문이다. "
      "`reindex` 로 달력 날짜를 모두 만든 뒤 `ffill` 하면 1월 4일(토) · 5일(일)이 3일(금) 값을 받는다. 채운 뒤에는 빈 줄이 ⟦t2['USDKRW=X'].isna().sum()⟧개다.",
 warn=("채우는 규칙은 적어 둔다", "직전 값(ffill), 다음 값(bfill), 앞뒤 평균 중 무엇을 쓸지는 회사마다 다르다. 어떤 규칙을 썼는지 결과 옆에 꼭 적는다."),
 **{"try": "`.ffill().bfill()` 을 `.bfill()` 만으로 바꿔 본다. 토 · 일이 다음 월요일 값을 받는다."}),

dict(id="3-6", slug="06-weighted-rate", title="단순 평균 환율 vs 주문 가중 평균 환율 · CH-11", short="가중 평균",
 goal="달러 주문만 골라, 그달 환율의 단순 평균과 '주문이 들어온 만큼 무게를 둔' 가중 평균을 비교한다.",
 cells=[
  dict(code='''us = t2[t2["currency"] == "USD"].copy()
us["krw"] = us["fc"] * us["USDKRW=X"]                  # 그날 환율로 바꾼 원화
us["month"] = us["date"].dt.month
g = us.groupby("month")[["fc", "krw"]].sum()
g["weighted"] = (g["krw"] / g["fc"]).round(1)                 # 주문 금액 가중 평균 환율
g["simple"] = fxd.groupby(fxd.index.month)["USDKRW=X"].mean().round(1)   # 달력 평균
g["diff"] = (g["weighted"] - g["simple"]).round(1)
print(g[["fc", "simple", "weighted", "diff"]])
print("year: simple", round(fxd["USDKRW=X"].mean(), 1), "/ weighted", round(us["krw"].sum() / us["fc"].sum(), 1))'''),
  dict(before="CH-11. 달마다 두 평균을 나란히 놓는다. 차이가 작아서 차이만 따로 그린다.",
       code='''fig, ax = plt.subplots(figsize=(7, 3))
ax.bar(g.index, g["diff"], color=["#C9382A" if v > 0 else "#028090" for v in g["diff"]])
ax.axhline(0, color="black", linewidth=0.8)
ax.set(title="CH-11 Weighted minus simple average USD/KRW", xlabel="Month", ylabel="KRW", xticks=list(g.index))
plt.show()''', alt="CH-11 달별 주문 가중 평균 환율과 단순 평균 환율의 차이 막대"),
 ],
 talk=[("asst", "1년으로 보면 단순 평균은 ⟦round(fxd['USDKRW=X'].mean(),1)|,⟧원, 가중 평균은 ⟦round(us['krw'].sum()/us['fc'].sum(),1)|,⟧원이에요."),
       ("doc", "주문은 달러가 비쌀 때 많이 들어왔어요. 그래서 가중 평균이 더 높아요.")],
 read="가중 평균 = (원화 합계) ÷ (달러 합계). 주문이 많은 날의 환율이 더 큰 무게를 갖는다. 연간 차이는 "
      "⟦round(us['krw'].sum()/us['fc'].sum() - fxd['USDKRW=X'].mean(),1)⟧원이다. 달 안에서는 차이가 작지만(최대 ⟦g['diff'].abs().max()⟧원), "
      "1년을 한꺼번에 평균 내면 \"언제 많이 팔렸나\"가 섞여 차이가 커진다.",
 **{"try": "`currency == \"USD\"` 를 `\"JPY\"` 로, `USDKRW=X` 를 `JPYKRW=X` 로 바꿔 엔화 주문의 가중 평균을 구해 본다."}),

dict(id="3-7", slug="07-rate-vs-orders", title="환율과 해외 주문 수 · CH-12", short="scatter, polyfit, corr",
 goal="달마다 원/달러 평균 환율과 미국 주문 수를 점으로 찍고, 추세선과 상관계수를 구한다.",
 cells=[
  dict(code='''import numpy as np
m = pd.DataFrame({
    "usdkrw": fxd.groupby(fxd.index.month)["USDKRW=X"].mean(),
    "us_orders": t2[t2["country"] == "US"].groupby(t2["date"].dt.month).size(),
})
print(m.round(1))
slope, intercept = np.polyfit(m["usdkrw"], m["us_orders"], 1)
print("slope:", round(slope, 3), "/ corr:", round(m["usdkrw"].corr(m["us_orders"]), 2))'''),
  dict(before="CH-12. 점마다 달 숫자를 붙인다.",
       code='''fig, ax = plt.subplots(figsize=(6, 3.6))
ax.scatter(m["usdkrw"], m["us_orders"], color="#1F3A5F")
for mon, r in m.iterrows():
    ax.annotate(str(mon), (r["usdkrw"], r["us_orders"]), xytext=(4, 3), textcoords="offset points", fontsize=8)
xs = np.linspace(m["usdkrw"].min(), m["usdkrw"].max(), 50)
ax.plot(xs, slope * xs + intercept, color="#D98E22", label="trend")
ax.set(title="CH-12 USD/KRW vs US orders (monthly)", xlabel="KRW per USD (monthly mean)", ylabel="US orders")
ax.legend()
plt.show()''', alt="CH-12 월평균 원/달러 환율과 미국 주문 수 산점도와 추세선"),
 ],
 talk=[("robo", "환율 오르면 주문도 오르는 거지? 삐빅.", "thinking"),
       ("fly", "같이 움직였을 뿐이야. 11 · 12월은 연말 쇼핑 철이기도 하잖아.")],
 read="상관계수 ⟦round(m['usdkrw'].corr(m['us_orders']),2)⟧ 은 둘이 강하게 같이 움직였다는 뜻이다. 추세선 기울기 ⟦round(slope,3)⟧ 은 "
      "\"환율이 10원 높은 달에 미국 주문이 약 ⟦round(slope*10,1)⟧건 많았다\"로 읽는다. 하지만 이것만으로 **환율 때문에** 주문이 늘었다고 말할 수는 없다. "
      "계절, 광고, 신상품처럼 함께 움직인 다른 이유를 따로 확인해야 한다.",
 **{"try": "`US` 를 `CN` 으로, `USDKRW=X` 를 `CNYKRW=X` 로 바꿔 본다. 중국 주문은 환율과 별 관계가 없게 만들었다."}),

dict(id="3-8", slug="08-rounded-tag", title="$0.50 단위로 반올림한 표시가 · CH-13", short="반올림, 차이, axhline",
 goal="가격표에 \"$26.58\" 대신 \"$26.50\" 처럼 0.5달러 단위로 보기 좋게 적었을 때, 상품마다 원화로 얼마나 덜(더) 받는지 계산한다.",
 cells=[
  dict(code='''usd_rate = rate["USDKRW=X"]
tag["usd_tag"] = (tag["usd"] * 2).round() / 2          # 0.5 단위로 반올림
tag["diff_krw"] = (tag["usd_tag"] * usd_rate - tag["krw"]).round(0)
print(tag[["item", "krw", "usd", "usd_tag", "diff_krw"]])
print("total diff (one each):", tag["diff_krw"].sum())'''),
  dict(before="CH-13. 0 선 위는 더 받는 상품, 아래는 덜 받는 상품이다.",
       code='''fig, ax = plt.subplots(figsize=(6.5, 3))
ax.bar(tag["item"], tag["diff_krw"], color=["#028090" if v >= 0 else "#C9382A" for v in tag["diff_krw"]])
ax.axhline(0, color="black", linewidth=0.8)
ax.set(title="CH-13 Rounded USD tag vs exact price", ylabel="KRW (tag - exact)")
plt.show()''', alt="CH-13 상품별 0.5달러 반올림 표시가와 정확한 가격의 원화 차이 막대"),
 ],
 talk=[("asst", "가장 많이 덜 받는 건 ⟦tag.loc[tag['diff_krw'].idxmin(),'item']⟧, ⟦-tag['diff_krw'].min()|,.0f⟧원이에요."),
       ("doc", "한 벌에 그 정도면 보기 좋은 값을 고르는 비용으로 괜찮아요. 판단은 사장님 몫이에요.")],
 read="`(x * 2).round() / 2` 는 0.5 단위 반올림이다. 차이는 상품마다 ±⟦round(usd_rate/4)⟧원(0.25달러) 안에 들어온다. 모두 한 벌씩 팔리면 "
      "합계 ⟦tag['diff_krw'].sum()|,.0f⟧원 차이다. 가격표를 바꿀지는 이 숫자를 보고 사람이 정한다.",
 **{"try": "`* 2` 와 `/ 2` 를 `* 1` 과 `/ 1` 로 바꿔 1달러 단위 반올림을 해 본다. 차이가 두 배쯤 커진다."}),

dict(id="3-9", slug="09-check-ai-tag", title="AI 가격표 JSON 검증하고 저장", short="json, 사칙 검증, to_csv",
 goal="AI 가 만들어 준 외국어 가격표를 그대로 쓰지 않고, \"외화 × 환율 ≈ 원화\" 인지 통화마다 확인한 뒤 고쳐서 저장한다.",
 cells=[
  dict(code='''import json
with open("ai_pricetag.json", encoding="utf-8") as f:
    ai = json.load(f)
print(ai["base_date"], ai["rates_used"], ai["note"])
a = pd.DataFrame(ai["items"])
r = ai["rates_used"]
# 되돌려 곱해 원화와 비교
# 달러는 0.5달러 단위로 반올림했으므로 0.25달러(반올림 폭)까지, 엔 · 위안은 1% 까지 통과
a["usd_ok"] = (a["usd"] * r["USD"] - a["krw"]).abs() <= 0.25 * r["USD"]
a["jpy_ok"] = (a["jpy"] * r["JPY_per_100"] / 100 / a["krw"] - 1).abs() < 0.01
a["cny_ok"] = (a["cny"] * r["CNY"] / a["krw"] - 1).abs() < 0.01
print(a)
print(a[["usd_ok", "jpy_ok", "cny_ok"]].sum())'''),
  dict(before="엔화가 전부 실패했다. AI 가 '100엔에 943.3원' 숫자를 1엔 값처럼 나눴다. 1엔 값으로 다시 계산하고, 다시 검증한 뒤 저장한다.",
       code='''a["jpy"] = (a["krw"] / (r["JPY_per_100"] / 100)).round(-1)     # 1엔 = 9.433원 으로 나누고 10엔 단위
a["jpy_ok"] = (a["jpy"] * r["JPY_per_100"] / 100 / a["krw"] - 1).abs() < 0.01
print(a[["item", "krw", "usd", "jpy", "cny", "jpy_ok"]])
out = a[["item", "krw", "usd", "jpy", "cny"]]
out.to_csv("price_tag_checked.csv", index=False, encoding="utf-8-sig")
print("saved:", len(out), "rows")'''),
 ],
 talk=[("robo", "삐빅! 엔화 가격이 전부 틀렸어. 100배 작아.", "wrong"),
       ("robo", "삐빅! 다시 검증, 세 통화 모두 통과!", "⟦'success' if a[['usd_ok','jpy_ok','cny_ok']].all().all() else 'wrong'⟧")],
 read="AI 는 `note` 에 \"100엔 기준\"이라고 적어 놓고도 계산은 1엔 기준처럼 했다. 결과가 그럴듯해 보여도 **되돌려 곱해 보면** 바로 드러난다. "
      "달러(반올림 폭 0.25달러 안)와 위안(1% 안)은 처음부터 통과했고, 엔화는 고친 뒤 통과했다. 검사 기준도 \"어떻게 만들었나\"에 맞춰 정한다. 0.5달러 단위로 반올림한 값에 1% 기준을 대면 6,000원짜리 양말처럼 싼 상품이 억울하게 떨어진다. 검증한 표만 `utf-8-sig` 로 저장한다(0-6).",
 warn=("AI 답은 초안이다", "AI 가 만든 숫자는 사람이 만든 숫자와 똑같이 검증한다. 검증 코드는 한 번 써 두면 다음 달 가격표에도 그대로 쓸 수 있다."),
 **{"try": "Colab 왼쪽 파일 창에서 `price_tag_checked.csv` 를 내려받아 엑셀로 열어 본다. 한글 없이도 깨지지 않는지 확인한다."}),
]

OUTRO = [("doc", "① 바깥 데이터는 막힐 수 있다, 백업을 둔다 ② 환율은 방향과 단위부터 본다 ③ 빈 날은 채우는 규칙을 정한다"),
         ("asst", "백업 CSV 로도 같은 표가 나왔고, AI 가격표의 엔화 실수도 잡았어요."),
         ("fly", "가격이랑 환율이 같이 바뀌면 이익은?")]
