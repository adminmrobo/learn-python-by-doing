"""4편 원고. build_episode.py 가 코드를 순서대로 실행하고 ⟦식⟧ 자리를 실행 결과로 채운다.
데이터는 1편의 ep1-cafe.zip 을 다시 쓴다."""

TITLE = "4편 가격을 바꾸면 이익이 움직인다"
ZIP = "ep1-cafe.zip"
INTRO = ("카페 Koi 사장님이 다시 왔다. \"원두값이 오르고 환율도 올랐어요. 커피값을 올려야 할까요?\" "
         "이 편은 두 부분이다. 앞 세 절은 **데이터를 여러 방향으로 잘라 보는 법**(데이터 큐브), 뒤 다섯 절은 **가정을 바꿔 가며 이익을 계산하는 법**(민감도)이다. "
         "1편 데이터를 그대로 쓴다. 여덟 절, 2시간쯤 걸린다.")
HEAD_TALK = [("asst", "원두값이 오르면 커피값도 올려야 해요?"), ("doc", "얼마나 올려야 하는지 그림으로 볼까요?")]
FILES = """| koi_sales.csv | 1편과 같은 2025년 영수증 줄. 이번에는 손님 유형(`customer`)을 주로 쓴다 |
| koi_fixed.csv | 1편과 같은 월별 고정비 |"""
NEXT = "[마감 내 가게 한 장 →](../final/index.md)"

SECTIONS = [
dict(id="4-1", slug="01-data-cube", title="데이터 큐브: 월 × 요일 × 고객 유형", short="groupby 3축, MultiIndex",
 goal="1편 판매 기록을 다시 읽어 정리하고, 월 · 요일 · 고객 유형 세 방향으로 묶은 '데이터 큐브'를 만든다.",
 cells=[
  dict(before="[ep1-cafe.zip](../data/ep1-cafe.zip) 을 다시 올린다(1편과 같은 파일). 1편에서 한 정리 두 가지(중복 영수증 지우기, 순매출 열)를 먼저 한다.",
       code='''# 1편 실습 파일 묶음(zip)을 다시 올리고 푼다
from google.colab import files
import zipfile, os
up = files.upload()
zipfile.ZipFile(list(up)[0]).extractall()
print(sorted(f for f in os.listdir() if f.startswith("koi_")))''', prefix="Saving ep1-cafe.zip to ep1-cafe.zip\n",
       run='import os\nprint(sorted(f for f in os.listdir() if f.startswith("koi_")))'),
  dict(code='''import pandas as pd
enc = "utf-8-sig"
sales = pd.read_csv("koi_sales.csv", encoding=enc, parse_dates=["date"]).drop_duplicates(subset="receipt_id")
sales["net"] = sales["qty"] * sales["price"] - sales["discount"]
sales["month"] = sales["date"].dt.month
sales["weekday"] = sales["date"].dt.day_name().str[:3]
sales["customer"] = sales["customer"].fillna("Unknown")      # 빈칸은 '모름'으로
cube = sales.groupby(["month", "weekday", "customer"])["net"].sum()
print("cells:", len(cube), "= 12 months x 7 days x", sales["customer"].nunique(), "types")
print(cube.head(8))'''),
 ],
 talk=[("asst", "표가 세로로 길게만 나와요. 이게 큐브예요?"),
       ("doc", "세 방향 이름표(월 · 요일 · 유형)가 붙은 값 목록이에요. 상자를 펼쳐 놓은 모양이죠.")],
 read="큐브는 \"월 × 요일 × 고객 유형\" 칸마다 순매출 합계가 하나씩 들어 있는 상자다. 칸은 ⟦len(cube)⟧개다. 줄 이름이 세 겹(MultiIndex)이라서 "
      "원하는 방향으로 자르거나(4-2) 펼칠(unstack) 수 있다. 1편에서 빈칸이던 손님 유형은 `Unknown` 으로 채웠다.",
 **{"try": "`[\"month\", \"weekday\", \"customer\"]` 에서 `\"weekday\"` 를 빼고 다시 실행해 칸 수가 어떻게 줄어드는지 본다."}),

dict(id="4-2", slug="02-slice", title="한 면 잘라 보기 · CH-14", short="xs, unstack, heatmap",
 goal="큐브에서 '단골(Regular)' 한 면만 잘라 월 × 요일 표로 펴고, 히트맵으로 그린다.",
 cells=[
  dict(code='''days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
regular = cube.xs("Regular", level="customer").unstack("weekday")[days] / 1e4    # 만원
print(regular.round(0))
share = cube.xs("Regular", level="customer").sum() / cube.sum()
print("regular share of sales:", round(share * 100, 1), "%")'''),
  dict(before="CH-14. 단골 매출을 월 × 요일 칸에 칠한다.",
       code='''import matplotlib.pyplot as plt
import seaborn as sns
fig, ax = plt.subplots(figsize=(6.5, 4.2))
sns.heatmap(regular, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
ax.set(title="CH-14 Regular customers' net sales (KRW 10k)", xlabel="", ylabel="Month")
plt.show()''', alt="CH-14 단골 손님 순매출, 월과 요일 히트맵"),
 ],
 talk=[("fly", "단골은 주말에 더 와? 아니면 평일에 와?")],
 read="`xs(\"Regular\", level=\"customer\")` 는 큐브에서 손님 유형이 Regular 인 면만 잘라 낸다. 남은 두 방향(월, 요일) 중 요일을 열로 펴면 히트맵용 표가 된다. "
      "단골 매출은 전체의 ⟦round(share*100,1)⟧% 이다. 칸 평균으로 주말은 ⟦regular[['Sat','Sun']].stack().mean()|.0f⟧만원, 평일은 ⟦regular[['Mon','Tue','Wed','Thu','Fri']].stack().mean()|.0f⟧만원이라 단골도 주말에 더 온다. 가장 큰 칸은 ⟦regular.stack().idxmax()[0]⟧월 ⟦regular.stack().idxmax()[1]⟧ (⟦regular.stack().max()|.0f⟧만원)이다.",
 **{"try": "`\"Regular\"` 를 `\"Tourist\"` 로 바꿔 관광객 면을 잘라 본다. 여름 주말이 진해진다."}),

dict(id="4-3", slug="03-3d-scatter", title="3D 산점, 정말 읽히나 · CH-15", short="projection='3d'",
 goal="큐브 전체를 3D 점으로 찍어 보고, 2D 히트맵보다 읽기 쉬운지 직접 판단한다.",
 cells=[
  dict(code='''import numpy as np
c = cube.reset_index()
c["d"] = c["weekday"].map({d: i for i, d in enumerate(days)})
types = ["Regular", "Walk-in", "Tourist", "Unknown"]
c["t"] = c["customer"].map({t: i for i, t in enumerate(types)})
fig = plt.figure(figsize=(6, 5))
ax = fig.add_subplot(projection="3d")
p = ax.scatter(c["month"], c["d"], c["t"], s=c["net"] / 2e4, c=c["net"] / 1e4, cmap="viridis")
ax.set(xlabel="Month", ylabel="Weekday", title="CH-15 Koi sales cube in 3D",
       yticks=range(7), yticklabels=days, zticks=range(4), zticklabels=types)
fig.colorbar(p, shrink=0.6, pad=0.15, label="KRW 10k")
plt.show()''', alt="CH-15 월, 요일, 고객 유형 3D 산점도"),
  dict(before="가장 큰 칸이 어디인지 그림에서 찾아보고, 아래 답과 맞춰 본다.",
       code='''top = cube.idxmax()
print("largest cell:", top[0], top[1], top[2], "/", round(cube.max() / 1e4), "(KRW 10k)")'''),
 ],
 talk=[("robo", "3D면 더 멋지잖아? 삐빅.", "thinking"),
       ("doc", "멋있죠. 그런데 가장 큰 칸이 ⟦top[0]⟧월 ⟦top[1]⟧ ⟦top[2]⟧ 칸이라는 걸 그림만 보고 찾을 수 있나요?")],
 read="점의 크기 · 색 · 위치가 서로 가리고, 보는 각도에 따라 앞뒤가 바뀐다. 3D 는 \"모양이 있다\"는 느낌을 줄 때는 좋지만 **값을 읽는 데는** 나쁘다. "
      "보고서에는 4-2 처럼 한 면씩 잘라 2D 로 보여 주는 편이 정확하다.",
 **{"try": "`fig.add_subplot(projection=\"3d\")` 아래에 `ax.view_init(elev=20, azim=-60)` 을 넣고 각도를 바꿔 본다. 같은 점이 다르게 보인다."}),

dict(id="4-4", slug="04-assumptions-grid", title="가정은 사전에, 계산은 격자로", short="dict, 함수, meshgrid",
 goal="이익 계산에 쓰는 가정을 사전 하나에 모으고, 판매가 × 원두 값의 모든 조합을 격자로 계산한다.",
 intro="이제부터는 \"만약에\"를 계산한다. 숫자를 코드 곳곳에 흩어 두면 하나 바꿀 때 다른 곳을 빠뜨린다. **가정은 한곳(사전)에** 모은다.",
 cells=[
  dict(code='''# 커피(아메리카노 · 라테) 한 달 잔 수: 2025년 실제 평균
coffee = sales[sales["menu"].isin(["Americano", "Latte"])]
base_cups = round(coffee.groupby("month")["qty"].sum().mean())
assume = {
    "base_cups": base_cups,   # 지금 가격일 때 한 달 잔 수
    "base_price": 4500,       # 지금 판매가 (원)
    "elasticity": -1.0,       # 값이 1% 오르면 잔 수가 1% 준다고 가정
    "grams": 18,              # 한 잔에 드는 원두 (g)
    "usdkrw": 1470,           # 환율 (3편, 12월 수준)
    "other": 600,             # 컵 · 우유 · 시럽 등 한 잔 기타 비용 (원)
    "fixed": 3_600_000,       # 커피에 나눠 준 한 달 고정비 (원)
}
def profit(price, bean_usd, a):
    """한 달 커피 이익(원). bean_usd = 원두 1kg 달러 가격"""
    cups = a["base_cups"] * (price / a["base_price"]) ** a["elasticity"]
    bean = bean_usd * a["usdkrw"] * a["grams"] / 1000     # 한 잔 원두값(원)
    return cups * (price - bean - a["other"]) - a["fixed"]
print(assume)
print("now ($14/kg, 4,500원):", round(profit(4500, 14, assume)))'''),
  dict(before="판매가 3,000~6,000원, 원두 1kg 8~30달러의 모든 조합을 한 번에 계산한다.",
       code='''prices = np.linspace(3000, 6000, 61)      # 50원 간격
beans  = np.linspace(8, 30, 45)           # 0.5달러 간격
P, B = np.meshgrid(prices, beans)
Z = profit(P, B, assume) / 1e4           # 만원
print("grid:", Z.shape, "/ max", round(Z.max()), "/ min", round(Z.min()))'''),
 ],
 talk=[("asst", "탄력성 -1.0 은 어디서 나온 숫자예요?"),
       ("doc", "가정이에요. 그래서 사전에 이름을 붙여 둬요. 나중에 -1.5 로 바꿔 보기 쉽게요.")],
 read="`meshgrid` 는 가격 61개 × 원두값 45개의 모든 짝을 만들어 준다. 함수에 격자를 통째로 넣으면 ⟦Z.size|,⟧칸이 한 번에 계산된다. "
      "지금 상태(원두 $14, 4,500원)의 한 달 커피 이익은 ⟦round(profit(4500, 14, assume))|,⟧원이다.",
 warn=("이건 예측이 아니라 가정 계산이다", "잔 수가 가격에 어떻게 반응할지(탄력성), 고정비를 얼마나 커피에 나눌지는 모두 가정이다. 결과는 \"이 가정이라면\" 으로 읽는다."),
 **{"try": "`\"elasticity\": -1.0` 을 `-1.5` 로 바꾸고 `now` 이익이 어떻게 변하는지 본다. 바꾼 뒤엔 되돌린다."}),

dict(id="4-5", slug="05-contour", title="판매가 × 원두 단가 이익 등고선 · CH-16", short="contourf, contour(levels=[0])",
 goal="격자 이익을 등고선으로 그리고, 이익이 0 이 되는 선(손익분기선)을 굵게 표시한다.",
 cells=[
  dict(code='''fig, ax = plt.subplots(figsize=(6.5, 4))
cf = ax.contourf(P, B, Z, levels=20, cmap="RdYlGn")
zero = ax.contour(P, B, Z, levels=[0], colors="black", linewidths=2)
ax.clabel(zero, fmt="break-even")
ax.plot(4500, 14, "w*", markersize=14, markeredgecolor="black")      # 지금 위치
ax.set(title="CH-16 Koi coffee monthly profit (KRW 10k)", xlabel="Price (KRW)", ylabel="Beans (USD per kg)")
fig.colorbar(cf, label="KRW 10k")
plt.show()''', alt="CH-16 판매가와 원두 가격에 따른 커피 이익 등고선과 손익분기선"),
  dict(before="원두 값마다 손익이 0 이 되는 최소 판매가를 숫자로도 뽑는다.",
       code='''def breakeven(bean_usd, a):
    ok = prices[profit(prices, bean_usd, a) >= 0]
    return int(ok.min()) if len(ok) else None
for b in [10, 14, 20, 26]:
    print(f"beans ${b}/kg -> break-even price {breakeven(b, assume)}")'''),
 ],
 talk=[("asst", "원두가 $14 에서 $20 으로 오르면 최소 ⟦breakeven(20, assume)|,⟧원은 받아야 해요."),
       ("fly", "근데 값을 올리면 손님이 줄잖아. 그것까지 들어간 거야?")],
 read="초록은 이익, 빨강은 손실이다. 검은 선이 손익분기선이고, 흰 별이 지금 위치다. 선 오른쪽 아래로 갈수록 여유가 크다. "
      "가격을 올리면 잔 수가 줄도록(탄력성) 함수에 넣었기 때문에, 가격을 올린다고 이익이 끝없이 늘지는 않는다.",
 **{"try": "`levels=20` 을 `levels=[-100, -50, 0, 50, 100]` 으로 바꿔 50만원 간격 선만 그려 본다."}),

dict(id="4-6", slug="06-change-fx", title="가정 바꾸기: 환율이 오르면", short="사전 복사, 다시 계산",
 goal="환율 가정 하나만 10% 올려 다시 계산하고, 손익분기선이 어디로 움직이는지 두 선을 겹쳐 본다.",
 cells=[
  dict(code='''hi = dict(assume)                       # 원래 가정은 그대로 두고 복사
hi["usdkrw"] = round(assume["usdkrw"] * 1.10)
Z2 = profit(P, B, hi) / 1e4
for b in [14, 20]:
    print(f"beans ${b}: break-even {breakeven(b, assume)} -> {breakeven(b, hi)}")
print("now profit:", round(profit(4500, 14, assume)), "->", round(profit(4500, 14, hi)))'''),
  dict(code='''fig, ax = plt.subplots(figsize=(6.5, 4))
c1 = ax.contour(P, B, Z, levels=[0], colors="black", linewidths=2)
c2 = ax.contour(P, B, Z2, levels=[0], colors="#C9382A", linewidths=2, linestyles="--")
ax.clabel(c1, fmt=f"USD/KRW {assume['usdkrw']}"); ax.clabel(c2, fmt=f"USD/KRW {hi['usdkrw']}")
ax.plot(4500, 14, "k*", markersize=12)
ax.set(title="Break-even line moves when USD/KRW rises 10%", xlabel="Price (KRW)", ylabel="Beans (USD per kg)")
plt.show()''', alt="환율 10% 상승 전후 손익분기선 두 개"),
 ],
 talk=[("fly", "환율이 10% 뛰면 손익 0 선은 어디로 가?"),
       ("asst", "원두 $20 기준으로 손익분기 가격이 ⟦breakeven(20, assume)|,⟧원에서 ⟦breakeven(20, hi)|,⟧원으로 올라요.")],
 read="`dict(assume)` 로 복사해야 원래 가정이 바뀌지 않는다. 그냥 `hi = assume` 이라고 쓰면 두 이름이 같은 사전을 가리켜서 원래 값까지 바뀐다. "
      "환율이 ⟦assume['usdkrw']|,⟧ → ⟦hi['usdkrw']|,⟧원이 되면 원두 한 잔 값이 오르므로 손익분기선이 아래로 내려온다. 같은 가격에서 버틸 수 있는 원두 값이 낮아진다는 뜻이다. "
      "지금 위치의 이익은 ⟦round(profit(4500, 14, assume))|,⟧원 → ⟦round(profit(4500, 14, hi))|,⟧원이다.",
 **{"try": "`hi = dict(assume)` 를 `hi = assume` 으로 바꿔 실행한 뒤 `print(assume[\"usdkrw\"])` 를 찍어 본다. 원래 가정까지 바뀐 것을 확인하고 되돌린다."}),

dict(id="4-7", slug="07-surface-vs-contour", title="3D 곡면 vs 2D 등고선", short="plot_surface, subplots",
 goal="같은 격자를 3D 곡면과 2D 등고선으로 나란히 그려, 무엇이 더 잘 읽히는지 비교한다.",
 cells=[dict(code='''fig = plt.figure(figsize=(11, 4.5))
ax1 = fig.add_subplot(1, 2, 1, projection="3d")
ax1.plot_surface(P, B, Z, cmap="RdYlGn")
ax1.set(title="3D surface", xlabel="Price", ylabel="Beans $", zlabel="Profit")
ax2 = fig.add_subplot(1, 2, 2)
ax2.contourf(P, B, Z, levels=20, cmap="RdYlGn")
ax2.contour(P, B, Z, levels=[0], colors="black", linewidths=2)
ax2.set(title="2D contour", xlabel="Price (KRW)", ylabel="Beans (USD per kg)")
fig.subplots_adjust(wspace=0.35)
plt.show()''', alt="같은 이익 격자를 3D 곡면과 2D 등고선으로 나란히 그린 그림")],
 talk=[("robo", "삐빅. 3D 가 멋있긴 한데 0 선은 오른쪽이 더 잘 보여.", "success")],
 read="3D 곡면은 \"가격이 낮고 원두가 비싸면 크게 떨어진다\"는 전체 모양을 한눈에 준다. 하지만 손익분기선이 어디인지, 지금 위치에서 얼마나 여유가 있는지는 "
      "2D 등고선에서 훨씬 정확하게 읽힌다. **설명할 때는 3D, 결정할 때는 2D.**",
 **{"try": "`plot_surface` 줄 아래에 `ax1.view_init(elev=35, azim=-130)` 을 넣어 다른 각도에서 본다."}),

dict(id="4-8", slug="08-save-download", title="보고서용으로 저장하고 내려받기", short="savefig(dpi), files.download",
 goal="사장님께 드릴 그림을 고해상도 PNG 로 저장하고, Colab 에서 내 컴퓨터로 내려받는다.",
 cells=[
  dict(code='''fig, ax = plt.subplots(figsize=(6.5, 4))
cf = ax.contourf(P, B, Z, levels=20, cmap="RdYlGn")
ax.contour(P, B, Z, levels=[0], colors="black", linewidths=2)
ax.plot(4500, 14, "w*", markersize=14, markeredgecolor="black")
ax.set(title="Koi coffee: price x bean cost -> monthly profit", xlabel="Price (KRW)", ylabel="Beans (USD per kg)")
fig.colorbar(cf, label="KRW 10k")
fig.savefig("koi_breakeven.png", dpi=200, bbox_inches="tight")    # 보고서용 고해상도
print("saved:", round(os.path.getsize("koi_breakeven.png") / 1024), "KB")
plt.close(fig)'''),
  dict(code='''# Colab 에서만 동작한다. 브라우저가 파일을 내려받는다
try:
    from google.colab import files
    files.download("koi_breakeven.png")
except ImportError:
    print("Colab 이 아니면 왼쪽 파일 목록이나 작업 폴더에서 직접 연다")''', run='print("Colab 이 아니면 왼쪽 파일 목록이나 작업 폴더에서 직접 연다")',
       after="Colab 에서는 아무것도 찍히지 않고 브라우저 아래쪽에 내려받기가 뜬다. 처음이면 \"여러 파일 다운로드 허용\" 창이 나올 수 있다."),
 ],
 talk=[("asst", "dpi 는 왜 200 이에요?"), ("doc", "화면용은 100 이면 되지만, 인쇄하면 흐려져요. 보고서는 200 이상으로 저장해요.")],
 read="`bbox_inches=\"tight\"` 는 그림 둘레의 빈 여백을 잘라 준다. `plt.close(fig)` 는 저장만 하고 화면에는 다시 그리지 않는다. "
      "저장한 파일 크기는 ⟦round(os.path.getsize('koi_breakeven.png')/1024)⟧KB 다.",
 **{"try": "`dpi=200` 을 `dpi=80` 으로 바꿔 저장하고 두 파일을 확대해 비교해 본다."}),
]

OUTRO = [("doc", "① 큐브는 잘라야 읽힌다 ② 가정은 한곳에 모은다 ③ 이번 데이터에서는 등고선이 더 잘 읽힌다"),
         ("asst", "환율 가정 한 줄 바꾸니 손익분기 가격이 ⟦breakeven(20, hi) - breakeven(20, assume)|,⟧원 올라갔어요."),
         ("fly", "그럼 네 가게라면 어떤 그림 한 장이야?")]
