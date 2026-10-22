"""0편 시작 데이터(ep0-start.zip)를 만들고, 0편 코드의 실행 결과를 확인한다.
usage: python tools/make_ep0.py"""
import io, os, sys, zipfile, tempfile, contextlib
import pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
menu = pd.DataFrame({
    "menu":     ["Americano", "Latte", "Iced Tea", "Cheesecake", "Croissant"],
    "category": ["Drink", "Drink", "Drink", "Dessert", "Dessert"],
    "price":    [4500, 5000, 5500, 6000, 3500],
    "cost":     [1200, 1600, 1100, 2400, 1300],
})
out = os.path.join(ROOT, "docs", "data", "ep0-start.zip")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("koi_menu.csv", menu.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig") if False else "﻿" + menu.to_csv(index=False))
print("wrote", out)

# 0-6 그림 두 장: 한글이 깨진 차트, 영어 라벨 차트 (Colab 기본 글꼴 DejaVu Sans 그대로)
import warnings
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
img = os.path.join(ROOT, "docs", "ep0", "img"); os.makedirs(img, exist_ok=True)
for name, title, xl, yl in [("hangul-broken", "메뉴별 가격", "메뉴", "가격(원)"), ("english-ok", "Price by menu", "Menu", "Price (KRW)")]:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(menu["menu"], menu["price"], color="#028090")
        ax.set(title=title, xlabel=xl, ylabel=yl)
        ax.tick_params(axis="x", labelsize=8)
        fig.savefig(os.path.join(img, name + ".png"), dpi=90, bbox_inches="tight", facecolor="white")
        plt.close(fig)
print("wrote images")

# Colab 에서 files.upload() 뒤에 하는 일을 그대로 흉내 낸다
tmp = tempfile.mkdtemp(); os.chdir(tmp)
zipfile.ZipFile(out).extractall()
CELLS = {
"0-3 확인": '''import os
print(sorted(f for f in os.listdir() if f.endswith((".csv", ".xlsx", ".json", ".txt"))))''',
"0-3 읽기": '''import pandas as pd
menu = pd.read_csv("koi_menu.csv", encoding="utf-8-sig")
print(menu)''',
"0-6": '''import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5, 3))
ax.bar(menu["menu"], menu["price"], color="#028090")
ax.set(title="Price by menu", xlabel="Menu", ylabel="Price (KRW)")
plt.close(fig)''',
"0-4": '''shop = "Cafe Koi"                      # 이름 = 값
print("store:", shop)                  # 괄호 안을 화면에 보여 준다
price = {"Americano": 4500, "Latte": 5000}   # 사전: 짝을 지어 둔 표
print("latte:", price["Latte"])
print(menu["price"])                   # 표에서 열 하나 꺼내기
print(menu[menu["price"] >= 5000])     # 조건에 맞는 줄만
print("mean price:", menu["price"].mean())   # 값.함수()''',
}
ns = {}
for k, code in CELLS.items():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): exec(code, ns)
    print(f"===== {k}\n{buf.getvalue()}")
