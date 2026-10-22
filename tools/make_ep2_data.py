"""2편 실습 데이터(ep2-cvs.zip)를 만든다. 값은 모두 연습용으로 지어낸 것이다.
usage: python tools/make_ep2_data.py"""
import os, zipfile
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(31)

# ---------- cvs_sales.csv : 2025년 3월 결제 1건 = 1줄 ----------
CAT = {"과자": 1800, "음료": 1700, "도시락": 4000, "라면": 1500, "아이스크림": 1600, "생활용품": 3500}
hour_w = np.array([3, 2, 1, 1, 1, 2, 4, 9, 12, 7, 5, 6, 12, 10, 5, 5, 6, 8, 11, 12, 9, 7, 5, 4], float)
rows = []
for d in pd.date_range("2025-03-01", "2025-03-31"):
    wk = d.dayofweek >= 5
    n = rng.poisson(270 if wk else 235)
    hw = hour_w.copy()
    if wk: hw[6:10] *= 0.5; hw[10:18] *= 1.9; hw[18:22] *= 0.8; hw[22:24] *= 1.3     # 주말: 출근 시간 한산, 오후 · 밤 북적
    hours = rng.choice(24, n, p=hw / hw.sum())
    for h in hours:
        cat = rng.choice(list(CAT), p=[.26, .33, .09, .14, .08, .10])
        items = 1 + rng.poisson(0.9)
        amt = sum(CAT[cat] * rng.lognormal(0, 0.45) for _ in range(items))
        amt = int(round(amt / 100) * 100)
        pay = rng.choice(["Card", "Mobile", "Cash"], p=[.58, .30, .12])
        rows.append([d + pd.Timedelta(hours=int(h), minutes=int(rng.integers(0, 60))), cat, max(amt, 600), pay])
sales = pd.DataFrame(rows, columns=["time", "category", "amount", "pay"])
# 함정: 일요일 밤 수기 입력으로 보이는 딱 떨어지는 현금 금액
sun = sales[(sales.time.dt.dayofweek == 6) & (sales.time.dt.hour >= 22)].sample(26, random_state=3).index
sales.loc[sun, "amount"] = rng.choice([10000, 20000, 30000, 50000], len(sun))
sales.loc[sun, "pay"] = "Cash"
sales = sales.sort_values("time").reset_index(drop=True)
sales.insert(0, "receipt", np.arange(1, len(sales) + 1) + 30000)
sales["time"] = sales["time"].dt.strftime("%Y-%m-%d %H:%M")

# ---------- cvs_stock.csv : 3월 31일 밤 진열 상품의 유통기한 ----------
prods = [("삼각김밥", "도시락", 1, 3), ("샌드위치", "도시락", 1, 4), ("도시락 A", "도시락", 0, 3), ("우유 200ml", "음료", 2, 12),
         ("바나나우유", "음료", 3, 14), ("요거트", "음료", 4, 20), ("컵라면", "라면", 60, 200), ("봉지라면", "라면", 90, 240),
         ("감자칩", "과자", 40, 180), ("초코바", "과자", 60, 300), ("아이스바", "아이스크림", 200, 600), ("생수", "음료", 120, 500)]
st = []
for name, cat, lo, hi in prods:
    for k in range(int(rng.integers(3, 7))):
        st.append([name, cat, int(rng.integers(1, 9)), (pd.Timestamp("2025-03-31") + pd.Timedelta(days=int(rng.integers(lo, hi)) - (1 if k == 0 and lo <= 1 else 0))).strftime("%Y-%m-%d")])
st += [["삼각김밥", "도시락", 2, "2025-03-30"], ["우유 200ml", "음료", 1, "2025-03-29"]]   # 함정: 이미 지난 것
stock = pd.DataFrame(st, columns=["product", "category", "qty", "expiry"])

# ---------- cvs_cash.csv : 일별 현금 입출 ----------
cash_sales = pd.to_datetime(sales["time"]).dt.date[sales["pay"] == "Cash"]
cin = sales.loc[sales["pay"] == "Cash"].groupby(pd.to_datetime(sales["time"]).dt.strftime("%Y-%m-%d"))["amount"].sum()
cash = pd.DataFrame({"date": cin.index, "cash_in": cin.values})
cash["cash_out"] = 0
bal = 200_000                                   # 3월 1일 아침 계산대 현금
for i, r in cash.iterrows():
    bal += r["cash_in"]
    if pd.Timestamp(r["date"]).dayofweek == 0:  # 월요일 밤: 20만원만 남기고 10만원 단위로 은행 입금
        dep = int((bal - 200_000) // 100_000 * 100_000)
        cash.loc[i, "cash_out"] = dep; bal -= dep
    if r["date"] == "2025-03-14":               # 거스름돈 동전 교환
        cash.loc[i, "cash_out"] += 150_000; bal -= 150_000
out = os.path.join(ROOT, "docs", "data", "ep2-cvs.zip")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for name, df in [("cvs_sales.csv", sales), ("cvs_stock.csv", stock), ("cvs_cash.csv", cash)]:
        z.writestr(name, "﻿" + df.to_csv(index=False))
print("wrote", out, "| sales", len(sales), "| stock", len(stock), "| cash days", len(cash))
