"""1편 원고. build_episode.py 가 코드를 순서대로 실행하고 ⟦식⟧ 자리를 실행 결과로 채운다."""

TITLE = "1편 카페 Koi의 장부를 연다"
ZIP = "ep1-cafe.zip"
INTRO = ("카페 Koi 사장님이 2025년 한 해 장부를 들고 왔다. 판매 기록, 지저분한 원가표 엑셀, 배달앱 주문, 고정비, 원두 재고. "
         "이 편에서는 파일을 읽고, 청소하고, 붙이고, **합계가 맞는지 확인한 뒤에** 월별 손익 그림을 그린다. 열세 절, 모두 합쳐 2시간쯤 걸린다.")
HEAD_TALK = [("asst", "장부를 열면 제일 먼저 뭘 봐요?"), ("doc", "몇 줄인지, 빈칸이 몇 개인지부터요.")]
FILES = """| koi_sales.csv | 2025년 영수증 줄 ⟦len(sales_raw)|,⟧줄 (영수증 번호, 날짜, 메뉴, 수량, 단가, 할인, 손님 유형) |
| koi_cost.xlsx | 메뉴 원가표. 제목 줄 · 빈 행 · ₩ 글자 · 숨은 공백이 섞인 엑셀 |
| koi_delivery.json | 배달앱 7월 주문 응답 (JSON) |
| koi_fixed.csv | 월별 고정비 (임대료, 인건비, 공과금) |
| koi_stock.csv | 4월 원두 재고 변동 (kg) |"""
NEXT = "[2편 편의점은 언제 바쁜가 →](../ep2/index.md)"

UPLOAD = '''# 1편 실습 파일 묶음(zip)을 올리고 푼다
from google.colab import files
import zipfile, os
up = files.upload()
zipfile.ZipFile(list(up)[0]).extractall()
print(sorted(f for f in os.listdir() if f.startswith("koi_")))'''

SECTIONS = [
dict(id="1-1", slug="01-read-sales", title="판매 기록 읽고 모양 보기", short="read_csv, shape, head",
 goal="판매 기록 CSV 를 표로 읽고, 줄 수 · 열 수와 첫 세 줄을 본다.",
 cells=[
  dict(before="먼저 [ep1-cafe.zip](../data/ep1-cafe.zip) 을 올린다. 0-3 과 같은 셀이다.",
       code=UPLOAD, prefix="Saving ep1-cafe.zip to ep1-cafe.zip\n",
       run='import os\nprint(sorted(f for f in os.listdir() if f.startswith("koi_")))'),
  dict(before="판매 기록을 표로 읽는다. `parse_dates` 를 주면 날짜 글자가 처음부터 날짜형으로 읽힌다.",
       code='''# 판매 기록(CSV)을 표로 읽는다
import pandas as pd
enc = "utf-8-sig"
sales = pd.read_csv("koi_sales.csv", encoding=enc, parse_dates=["date"])
sales_raw = sales.copy()          # 나중에 비교할 원본을 따로 둔다
print("rows x cols:", sales.shape)
print(sales.head(3))'''),
 ],
 talk=[("asst", "⟦len(sales)|,⟧줄이면 엑셀로도 열 수 있지 않아요?"),
       ("doc", "열 수는 있어요. 그런데 월별로 묶고 검증하는 건 여기가 훨씬 빨라요.")],
 read="`(⟦sales.shape[0]⟧, ⟦sales.shape[1]⟧)` 은 영수증 줄 ⟦len(sales)|,⟧개, 열 ⟦sales.shape[1]⟧개라는 뜻이다. 한 줄이 영수증의 메뉴 한 줄이다. "
      "`price` 는 한 개 값, `qty` 는 개수, `discount` 는 그 줄에서 깎아 준 금액이다(단골 할인). 금액 단위는 원.",
 **{"try": "`sales.head(3)` 을 `sales.tail(3)` 으로 바꿔 12월 31일 마지막 영수증을 본다."}),

dict(id="1-2", slug="02-dtypes-missing", title="자료형과 빈칸부터", short="dtypes, isna, value_counts",
 goal="계산하기 전에 열마다 자료형(dtype)과 빈칸 수, 메뉴별 줄 수를 확인한다.",
 cells=[dict(code='''# 열마다 자료형, 빈칸(NaN) 수, 메뉴별 줄 수
print(sales.dtypes)
print(sales.isna().sum())
print(sales["menu"].value_counts())''')],
 talk=[("fly", "손님 유형이 ⟦sales['customer'].isna().sum()⟧칸 비었네. 그 줄은 버려?"),
       ("doc", "아직요. 매출은 멀쩡하니 손님 유형만 '모름'인 거예요.")],
 read="`date` 가 `datetime64[ns]` 면 날짜형으로 잘 읽힌 것이다. 금액 열이 `int64` 라 바로 더할 수 있다. "
      "`customer` 의 빈칸 ⟦sales['customer'].isna().sum()⟧개는 포스기에서 손님 유형을 안 누른 줄이다.",
 **{"try": "`sales[\"customer\"].value_counts(dropna=False)` 로 빈칸(NaN)까지 함께 세어 본다."}),

dict(id="1-3", slug="03-raw-excel", title="지저분한 원가표 엑셀 날것으로 보기", short="read_excel(header=None)",
 goal="제목 줄 · 빈 행 · ₩ 글자가 섞인 엑셀을 손대지 않고 먼저 본다.",
 cells=[dict(code='''# header=None: 첫 줄을 열 이름으로 쓰지 말고 있는 그대로 보여 달라
raw = pd.read_excel("koi_cost.xlsx", header=None)
print(raw)''')],
 talk=[("asst", "위에 두 줄은 제목이고, 진짜 열 이름은 세 번째 줄이네요?"),
       ("doc", "맞아요. 사람이 보기 좋게 만든 엑셀은 거의 다 이래요.")],
 read="0 · 1번 줄은 병합된 제목, 2번 줄이 진짜 열 이름, 5번 줄은 통째로 빈 줄이다. 가격과 원가는 `₩4,500` 처럼 **글자**로 들어 있고, "
      "Croissant 의 `updated` 는 `-` 다. 무엇을 청소해야 할지 이 화면에서 정한다.",
 **{"try": "`header=None` 을 빼고 읽어 본다. 제목 줄이 열 이름이 되어 버리는 모습을 확인한다."}),

dict(id="1-4", slug="04-clean-rows", title="청소 ① 제목 줄, 빈 행, 열 이름 공백", short="skiprows, dropna, str.strip",
 goal="제목 두 줄을 건너뛰고, 완전히 빈 행을 지우고, 열 이름의 앞뒤 공백을 없앤다.",
 cells=[dict(code='''# 위 두 줄(제목)을 건너뛰고 읽는다
cost = pd.read_excel("koi_cost.xlsx", skiprows=2)
print("before:", list(cost.columns))
cost = cost.dropna(how="all")              # 칸이 전부 빈 줄만 지운다
cost.columns = cost.columns.str.strip()    # 열 이름 앞뒤 공백 지우기
print("after: ", list(cost.columns))
print(cost)''')],
 talk=[("fly", "' menu' 랑 'menu' 가 달라? 눈으로는 똑같은데.")],
 read="`before` 의 `' menu'`, `'price '` 처럼 열 이름에 공백이 붙어 있으면 `cost[\"menu\"]` 가 `KeyError` 를 낸다. "
      "`dropna(how=\"all\")` 은 모든 칸이 빈 줄만 지우므로, 일부만 빈 줄은 살아남는다. 줄 번호 2 가 빠진 것이 지운 빈 행이다.",
 **{"try": "`how=\"all\"` 을 빼고 `cost.dropna()` 만 써 본다. `updated` 가 비어 있는 줄이 생기면 그 줄까지 사라질 수 있다."}),

dict(id="1-5", slug="05-clean-values", title='청소 ② "₩4,500", 날짜, "-"', short="str.replace, to_numeric, to_datetime",
 goal="`₩4,500` 같은 글자를 숫자로, 날짜 글자를 날짜형으로, `-` 를 빈칸(NaT)으로 바꾼다.",
 cells=[dict(code='''# ₩ 와 콤마를 지우고 숫자로 바꾼다
for col in ["price", "cost"]:
    cost[col] = pd.to_numeric(cost[col].str.replace("₩", "").str.replace(",", ""), errors="coerce")
# 날짜 글자를 날짜형으로. '-' 처럼 날짜가 아닌 것은 NaT(빈 날짜)가 된다
cost["updated"] = pd.to_datetime(cost["updated"], errors="coerce")
print(cost)
print(cost.dtypes)''')],
 talk=[("robo", "삐빅, 숫자가 됐어. 이제 더할 수 있어!", "success")],
 read="`errors=\"coerce\"` 는 \"바꿀 수 없는 값은 멈추지 말고 빈칸으로\" 라는 뜻이다. Croissant 의 `-` 가 `NaT` 가 됐다. "
      "`price` 와 `cost` 가 `int64` 가 되어 이제 계산할 수 있다.",
 **{"try": "`errors=\"coerce\"` 를 빼고 `pd.to_datetime(cost[\"updated\"])` 만 실행해 본다. `-` 때문에 오류가 나는 것을 확인한다."}),

dict(id="1-6", slug="06-json", title="배달앱 주문 JSON 읽기", short="json.load, DataFrame",
 goal="배달앱이 보내 준 주문 응답(JSON)을 열어 `status` 를 확인하고, 주문 목록을 표로 바꾼다.",
 cells=[dict(code='''# JSON 은 사전(dict) 모양으로 읽힌다. 표는 "orders" 안에 있다
import json
with open("koi_delivery.json", encoding="utf-8") as f:
    reply = json.load(f)
print(reply["status"], reply["month"], reply["count"])
delivery = pd.DataFrame(reply["orders"])
delivery["amount"] = delivery["qty"] * delivery["price"]
print(delivery.head())
print("orders:", len(delivery), "/ total:", delivery["amount"].sum())''')],
 talk=[("asst", "status 가 ok 가 아니면요?"), ("doc", "그땐 표로 바꾸기 전에 멈춰야 해요. 비어 있는 응답일 수 있거든요.")],
 read="`reply` 는 사전이다. `reply[\"orders\"]` 는 주문 ⟦len(delivery)⟧건짜리 목록이고, `pd.DataFrame` 이 목록의 항목 하나를 한 줄로 만든다. "
      "7월 배달 매출은 ⟦delivery['amount'].sum()|,⟧원이다.",
 **{"try": "`print(reply.keys())` 를 실행해 이 응답에 어떤 칸들이 있는지 본다."}),

dict(id="1-7", slug="07-select-filter", title="열 고르고 조건 거르기", short="열, 조건, &, query",
 goal="열 하나 · 여러 열 · 조건 거르기 · `query` 네 가지를 차례로 해 본다.",
 cells=[dict(code='''# 열 하나, 여러 열
print(sales["menu"].head(3))
print(sales[["date", "menu", "qty"]].head(3))
# 조건: 7월 줄만
july = sales[sales["date"].dt.month == 7]
print("July rows:", len(july))
# 조건 두 개: 아이스티를 3개 이상 산 줄
big_tea = sales[(sales["menu"] == "Iced Tea") & (sales["qty"] >= 3)]
print("Iced Tea x3+:", len(big_tea))
# 같은 조건을 글자로
print(len(sales.query("menu == 'Iced Tea' and qty >= 3")))''')],
 talk=[("fly", "& 대신 and 쓰면 안 돼?"), ("doc", "표의 조건끼리는 & 예요. 괄호도 꼭 씌우고요. query 안에서는 and 를 써요.")],
 read="`sales[\"date\"].dt.month == 7` 은 줄마다 True/False 를 만들고, `sales[...]` 가 True 인 줄만 남긴다. 7월은 ⟦len(july)|,⟧줄, "
      "아이스티 3개 이상은 ⟦len(big_tea)⟧줄이다.",
 **{"try": "`== 7` 을 `== 1` 로 바꿔 1월 줄 수와 비교해 본다. 아이스티 줄은 여름에 몰려 있다."}),

dict(id="1-8", slug="08-new-columns", title="새 열: 음료/디저트 분류와 순매출", short="열 계산, map",
 goal="메뉴를 음료/디저트로 나누는 열(map)과, 수량 × 단가 − 할인으로 순매출 열을 만든다.",
 cells=[dict(code='''# 메뉴 → 분류 사전
kind = {"Americano": "Drink", "Latte": "Drink", "Iced Tea": "Drink",
        "Cheesecake": "Dessert", "Croissant": "Dessert"}
sales["category"] = sales["menu"].map(kind)
# 순매출 = 수량 × 단가 − 할인
sales["net"] = sales["qty"] * sales["price"] - sales["discount"]
print(sales[["menu", "category", "qty", "price", "discount", "net"]].head())
print("unmapped:", sales["category"].isna().sum())
print("total net:", sales["net"].sum())''')],
 talk=[("robo", "삐빅, 분류 빈칸 ⟦sales['category'].isna().sum()⟧개. 다 짝을 찾았어.", "⟦'success' if sales['category'].isna().sum()==0 else 'wrong'⟧")],
 read="열끼리 계산하면 같은 줄끼리 계산된다. 3번 줄은 라테 1개 5,000원에서 단골 할인 500원을 뺀 4,500원이다. "
      "한 해 순매출은 ⟦sales['net'].sum()|,⟧원이다.",
 **{"try": "`kind` 사전에서 `\"Croissant\"` 를 지우고 다시 실행한다. `unmapped` 가 크루아상 줄 수만큼 늘어난다. 확인했으면 되돌린다."}),

dict(id="1-9", slug="09-map-trap", title="map 으로 원가 붙이기, 그런데 두 메뉴가 빈다", short="dict(zip), map, repr",
 goal="원가표에서 메뉴 → 원가 사전을 만들어 붙여 보고, 못 찾은 줄이 왜 생기는지 본다.",
 cells=[
  dict(code='''# 원가표의 두 열로 사전을 만든다 (엑셀의 VLOOKUP 자리)
unit = dict(zip(cost["menu"], cost["cost"]))
sales["unit_cost"] = sales["menu"].map(unit)
print("missing:", sales["unit_cost"].isna().sum())
print(sales.loc[sales["unit_cost"].isna(), "menu"].value_counts())'''),
  dict(before="눈으로는 같은 이름인데 왜 못 찾았을까. `repr` 로 감춰진 글자까지 찍어 본다.",
       code='''print([repr(m) for m in cost["menu"]])'''),
 ],
 talk=[("asst", "Latte 랑 Croissant 만 비었어요. 왜요?"),
       ("fly", "'Latte ' 끝에 공백 하나. 그거 하나로 ⟦sales['unit_cost'].isna().sum()|,⟧줄이 날아갔어.")],
 read="원가표 쪽 이름이 `'Latte '`, `'Croissant '` 로 끝에 공백이 있다. 사전은 글자가 **완전히 같아야** 짝을 찾으므로, "
      "판매 기록의 `'Latte'` 와 짝이 되지 않는다. 메뉴 두 종류, 줄로는 ⟦sales['unit_cost'].isna().sum()|,⟧줄이 비었다.",
 **{"try": "`print(len(\"Latte\"), len(\"Latte \"))` 를 실행해 두 글자의 길이가 5 와 6 으로 다른 것을 확인한다."}),

dict(id="1-10", slug="10-strip-merge", title="공백 지우고 merge, 합계까지 맞추기", short="str.strip, merge(how='left')",
 goal="원가표 이름의 공백을 지우고 `merge` 로 붙인 뒤, 줄 수와 빈칸 수로 제대로 붙었는지 확인한다.",
 cells=[dict(code='''# 이름 끝 공백을 지우고, 판매 기록 왼쪽에 원가를 붙인다
cost["menu"] = cost["menu"].str.strip()
m = sales.drop(columns="unit_cost").merge(cost[["menu", "cost"]], on="menu", how="left")
print("rows:", len(sales), "->", len(m))
print("missing cost:", m["cost"].isna().sum())
m["cogs"] = m["qty"] * m["cost"]        # 재료비 = 수량 × 한 개 원가
print(m[["menu", "qty", "net", "cost", "cogs"]].head())''')],
 talk=[("robo", "삐빅! 줄 수 그대로, 빈칸 ⟦m['cost'].isna().sum()⟧개. 다 붙었어!", "⟦'success' if (len(m)==len(sales) and m['cost'].isna().sum()==0) else 'wrong'⟧")],
 read="`how=\"left\"` 는 왼쪽 표(판매 기록)의 줄을 하나도 버리지 않는다. 붙인 뒤 줄 수가 ⟦len(sales)|,⟧ → ⟦len(m)|,⟧ 로 같고 빈칸이 0 이면 "
      "제대로 붙은 것이다. 줄 수가 늘었다면 원가표에 같은 메뉴가 두 번 있다는 뜻이다.",
 **{"try": "`str.strip()` 줄을 지우고(앞 절 상태로) 다시 실행하면 `missing cost` 가 몇이 되는지 본다. 그다음 되돌린다."}),

dict(id="1-11", slug="11-monthly-pl", title="월별 손익표와 CH-01 월별 손익 막대", short="groupby, 고정비, 막대 + 선",
 goal="월별로 순매출 · 재료비 · 고정비를 모아 손익표를 만들고, CH-01 그림 한 장으로 그린다.",
 cells=[
  dict(code='''# 월별로 묶어 더한다
m["month"] = m["date"].dt.month
fixed = pd.read_csv("koi_fixed.csv", encoding=enc)
pl = m.groupby("month")[["net", "cogs"]].sum()
pl["fixed"] = fixed.groupby("month")["amount"].sum()
pl["profit"] = pl["net"] - pl["cogs"] - pl["fixed"]
print((pl / 10000).round(1))     # 만원 단위로 보기'''),
  dict(before="CH-01. 막대는 순매출과 비용(재료비 + 고정비), 선은 이익이다. 라벨은 영어로 쓴다(0-6).",
       code='''import matplotlib.pyplot as plt
k = pl / 1e4                      # 만원
fig, ax = plt.subplots(figsize=(8, 3.6))
x = k.index
ax.bar(x - 0.2, k["net"], width=0.4, label="Net sales", color="#028090")
ax.bar(x + 0.2, k["cogs"] + k["fixed"], width=0.4, label="Costs", color="#D98E22")
ax.plot(x, k["profit"], marker="o", color="#1C2620", label="Profit")
ax.axhline(0, color="gray", linewidth=0.8)
ax.set(title="CH-01 Cafe Koi monthly P&L (2025)", xlabel="Month", ylabel="KRW 10k", xticks=list(x), ylim=(0, 1400))
ax.legend(ncol=3, loc="upper left")
plt.show()''', alt="CH-01 카페 Koi 월별 순매출, 비용 막대와 이익 선"),
 ],
 talk=[("asst", "7 · 8월 이익이 ⟦round(pl.loc[7,'profit']/1e4)|,⟧만원, ⟦round(pl.loc[8,'profit']/1e4)|,⟧만원으로 제일 커요."),
       ("fly", "근데 이 합계, 믿어도 돼? 아직 검증 안 했잖아.")],
 read="한 해 이익은 ⟦round(pl['profit'].sum()/1e4)|,⟧만원이다. 여름에 아이스티와 손님이 늘어 7 · 8월이 가장 좋고, "
      "고정비가 비슷한데 매출이 낮은 2월이 가장 작다(⟦round(pl.loc[2,'profit']/1e4)|,⟧만원).",
 **{"try": "`pl.sort_values(\"profit\")` 을 실행해 이익이 작은 달부터 늘어놓아 본다."}),

dict(id="1-12", slug="12-checks", title="검증 세 가지, 잡아낸 것 바로잡기", short="줄 수 · 합계 · 빈칸, drop_duplicates",
 goal="그림을 믿기 전에 세 가지를 확인한다. ① 영수증이 한 번씩만 있나 ② 월별 합계가 전체와 같나 ③ 빈칸이 없나.",
 cells=[
  dict(code='''# 검증 세 가지
c1 = m["receipt_id"].duplicated().sum()            # ① 두 번 찍힌 영수증 줄
c2 = pl["net"].sum() - m["net"].sum()               # ② 월별 합 − 전체 합 (0 이어야)
c3 = m[["net", "cost"]].isna().sum().sum()          # ③ 계산에 쓴 열의 빈칸
print("① duplicated receipts:", c1)
print("② monthly sum - total:", c2)
print("③ missing values:", c3)'''),
  dict(before="①이 0 이 아니다. 어떤 줄인지 들여다본다.",
       code='''print(m.loc[m["receipt_id"].duplicated(keep=False), ["receipt_id", "date", "menu", "qty", "net"]])'''),
  dict(before="똑같은 영수증이 두 번씩 찍혀 있다. 하나씩만 남기고 다시 모은다.",
       code='''m2 = m.drop_duplicates(subset="receipt_id")
pl2 = m2.groupby("month")[["net", "cogs"]].sum()
pl2["fixed"] = pl["fixed"]
pl2["profit"] = pl2["net"] - pl2["cogs"] - pl2["fixed"]
print("rows:", len(m), "->", len(m2))
print("profit change by month:")
print((pl2["profit"] - pl["profit"])[lambda s: s != 0])
print("duplicated now:", m2["receipt_id"].duplicated().sum())'''),
 ],
 talk=[("robo", "삐빅! 같은 영수증이 ⟦c1⟧번 더 찍혔어.", "wrong"),
       ("asst", "고치니까 ⟦len(m)-len(m2)⟧줄이 빠지고, 이익이 ⟦', '.join(str(i)+'월' for i in (pl2['profit']-pl['profit'])[lambda s: s!=0].index)⟧에서 줄었어요."),
       ("robo", "삐빅! 이제 세 가지 다 통과!", "⟦'success' if m2['receipt_id'].duplicated().sum()==0 else 'wrong'⟧")],
 read="②와 ③은 0 으로 통과했지만 ①이 ⟦c1⟧ 이다. ②는 \"더하는 방법\"이 맞는지를, ①은 \"더할 재료\"가 맞는지를 본다. "
      "둘은 다른 검사라서 ②가 통과해도 ①이 틀릴 수 있다. 이후 계산은 `m2`, `pl2` 로 한다.",
 warn=("검증은 그림보다 먼저", "1-11 의 그림은 중복 줄이 섞인 숫자로 그린 것이다. 차이는 작지만, 순서를 지키는 습관이 큰 실수를 막는다."),
 **{"try": "`subset=\"receipt_id\"` 를 빼고 `m.drop_duplicates()` 로 해 본다. 줄 전체가 같은 경우만 지우므로 이번에는 결과가 같다."}),

dict(id="1-13", slug="13-stock-waterfall", title="CH-02 재고 폭포", short="사칙검증, ax.bar(bottom=)",
 goal="4월 원두 재고를 기초 + 입고 − 사용 − 폐기 = 기말 로 맞춰 보고, 실제로 센 재고와 같은지 확인한 뒤 폭포 그림으로 그린다.",
 cells=[
  dict(code='''st = pd.read_csv("koi_stock.csv", encoding=enc)
kg = st.groupby("type")["kg"].sum().round(1)
print(kg)
calc = round(kg["opening"] + kg["in"] - kg["used"] - kg["waste"], 1)
print("calculated closing:", calc, "/ counted:", kg["count"], "/ same:", calc == kg["count"])'''),
  dict(before="CH-02. 막대마다 바닥(`bottom`)을 앞 막대가 끝난 높이로 두면 폭포가 된다.",
       code='''steps  = ["Opening", "In", "Used", "Waste", "Closing"]
height = [kg["opening"], kg["in"], kg["used"], kg["waste"], calc]
bottom = [0, kg["opening"], kg["opening"] + kg["in"] - kg["used"], calc, 0]
colors = ["#1F3A5F", "#028090", "#D98E22", "#C9382A", "#1F3A5F"]
fig, ax = plt.subplots(figsize=(6.5, 3.4))
ax.bar(steps, height, bottom=bottom, color=colors)
for i, (h, b) in enumerate(zip(height, bottom)):
    sign = "-" if steps[i] in ("Used", "Waste") else ("+" if steps[i] == "In" else "")
    ax.text(i, b + h + 0.8, f"{sign}{h:.1f}", ha="center")
ax.set(title="CH-02 Cafe Koi coffee beans, April 2025 (kg)", ylabel="kg", ylim=(0, 38))
plt.show()''', alt="CH-02 4월 원두 재고 폭포: 기초, 입고, 사용, 폐기, 기말"),
 ],
 talk=[("fly", "계산이랑 실제로 센 재고가 다르면 어떡해?"),
       ("doc", "그 차이가 바로 찾아야 할 일이에요. 이번엔 ⟦calc⟧kg 로 같네요.")],
 read="기초 ⟦kg['opening']⟧ + 입고 ⟦kg['in']⟧ − 사용 ⟦kg['used']⟧ − 폐기 ⟦kg['waste']⟧ = ⟦calc⟧kg 이 4월 30일에 실제로 센 ⟦kg['count']⟧kg 과 같다. "
      "폭포 그림은 \"어디서 늘고 어디서 줄었나\"를 한 줄로 보여 준다.",
 **{"try": "`koi_stock.csv` 에서 폐기 한 줄을 빼먹었다고 가정하고 `kg[\"waste\"]` 대신 `0.8` 을 넣어 본다. 계산값과 센 값이 어긋난다."}),
]

OUTRO = [("doc", "① 읽으면 모양과 빈칸부터 본다 ② 붙이기 전에 공백을 지운다 ③ 합계가 맞아야 그린다"),
         ("asst", "숨은 공백 하나에 ⟦sales['unit_cost'].isna().sum()|,⟧줄이 비었고, 중복 영수증 ⟦c1⟧줄도 잡았어요."),
         ("fly", "표는 맞췄어. 그럼 무슨 그림을 그려?")]
