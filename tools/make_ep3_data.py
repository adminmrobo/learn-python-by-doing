"""3편 실습 데이터(ep3-shop.zip)를 만든다.
환율 백업은 2025년 흐름을 흉내 낸 연습용 값이다(실제 고시 환율과 다르다).
usage: python tools/make_ep3_data.py"""
import json, os, zipfile
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(303)

# ---------- fx_2025_backup.csv : 영업일 종가 (1달러 · 1엔 · 1위안 = 몇 원) ----------
days = pd.bdate_range("2025-01-02", "2025-12-31")
anchor = {"USDKRW=X": [1455, 1445, 1458, 1440, 1395, 1365, 1375, 1390, 1393, 1420, 1458, 1470],
          "JPYKRW=X": [9.30, 9.50, 9.80, 9.95, 9.65, 9.45, 9.35, 9.42, 9.40, 9.35, 9.40, 9.45],
          "CNYKRW=X": [199.5, 198.5, 200.5, 197.5, 193.0, 190.0, 191.5, 193.5, 195.5, 199.5, 205.0, 207.0]}
mid = pd.to_datetime([f"2025-{m:02d}-15" for m in range(1, 13)])
fx = pd.DataFrame(index=days)
for t, a in anchor.items():
    base = np.interp(days.astype("int64"), mid.astype("int64"), a)
    noise = np.cumsum(rng.normal(0, 0.0025, len(days))); noise -= pd.Series(noise).rolling(15, min_periods=1, center=True).mean().values
    fx[t] = base * (1 + noise)
fx["USDKRW=X"] = fx["USDKRW=X"].round(1); fx["JPYKRW=X"] = fx["JPYKRW=X"].round(3); fx["CNYKRW=X"] = fx["CNYKRW=X"].round(2)
fx = fx[["CNYKRW=X", "JPYKRW=X", "USDKRW=X"]]; fx.index.name = "Date"

# ---------- shop_items.csv ----------
items = pd.DataFrame({
    "item": ["Tee", "Shirt", "Knit", "Denim", "Coat", "Cap", "Socks", "Tote bag"],
    "name_ko": ["티셔츠", "셔츠", "니트", "청바지", "코트", "모자", "양말", "토트백"],
    "price": ["₩19,000", "₩39,000", "₩59,000", "₩89,000", "₩189,000", "₩25,000", "₩6,000", "-"],
})
krw = {"Tee": 19000, "Shirt": 39000, "Knit": 59000, "Denim": 89000, "Coat": 189000, "Cap": 25000, "Socks": 6000}

# ---------- shop_orders_global.csv : 해외 주문 (주말 포함) ----------
cal = pd.date_range("2025-01-01", "2025-12-31")
fxd = fx.reindex(cal).ffill().bfill()
rows, oid = [], 50001
for d in cal:
    r = fxd.loc[d]
    lam = {"US": max(0.4, 1.2 + (r["USDKRW=X"] - 1380) / 45), "JP": max(0.4, 0.9 + (r["JPYKRW=X"] - 9.4) * 2.2), "CN": 0.7}
    for c, cur, t in [("US", "USD", "USDKRW=X"), ("JP", "JPY", "JPYKRW=X"), ("CN", "CNY", "CNYKRW=X")]:
        for _ in range(rng.poisson(lam[c] * (1.25 if d.dayofweek >= 5 else 1.0))):
            it = rng.choice(list(krw), p=[.24, .18, .14, .14, .06, .14, .10])
            fc = krw[it] / r[t]
            fc = round(fc * 2) / 2 if cur == "USD" else (round(fc, -1) if cur == "JPY" else round(fc))
            rows.append([oid, d.strftime("%Y-%m-%d"), c, cur, it, int(rng.choice([1, 1, 1, 2])), fc]); oid += 1
orders = pd.DataFrame(rows, columns=["order_id", "date", "country", "currency", "item", "qty", "unit_price"])

# ---------- ai_pricetag.json : AI 가 만든 외국어 가격표 (엔화를 100엔 고시로 잘못 나눔) ----------
last = fx.iloc[-1]
rates_used = {"USD": float(last["USDKRW=X"]), "JPY_per_100": round(float(last["JPYKRW=X"]) * 100, 1), "CNY": float(last["CNYKRW=X"])}
tag = []
for it, k in krw.items():
    tag.append({"item": it, "krw": k, "usd": round(k / rates_used["USD"] * 2) / 2,
                "jpy": round(k / rates_used["JPY_per_100"]), "cny": round(k / rates_used["CNY"])})   # jpy 가 100배 작게 나온다
ai = {"base_date": str(fx.index[-1].date()), "rates_used": rates_used, "note": "JPY rate is per 100 yen", "items": tag}

out = os.path.join(ROOT, "docs", "data", "ep3-shop.zip")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("fx_2025_backup.csv", "﻿" + fx.to_csv())
    z.writestr("shop_items.csv", "﻿" + items.to_csv(index=False))
    z.writestr("shop_orders_global.csv", "﻿" + orders.to_csv(index=False))
    z.writestr("ai_pricetag.json", json.dumps(ai, ensure_ascii=False, indent=2))
print("wrote", out, "| fx days", len(fx), "| orders", len(orders), orders.country.value_counts().to_dict())
