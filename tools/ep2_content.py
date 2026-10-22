"""2편 원고. build_episode.py 가 코드를 순서대로 실행하고 ⟦식⟧ 자리를 실행 결과로 채운다."""

TITLE = "2편 편의점은 언제 바쁜가"
ZIP = "ep2-cvs.zip"
INTRO = ("동네 편의점 사장님의 질문은 하나다. \"언제 사람을 더 둬야 하지?\" 이 편에서는 **질문을 먼저 한 줄로 적고**, 그 질문에 맞는 차트를 고른다. "
         "막대, 선, 히스토그램, 히트맵, 벤포드 비교까지 차트 일곱 장(CH-03 ~ CH-09)을 그린다. 아홉 절, 2시간쯤 걸린다.")
HEAD_TALK = [("asst", "차트부터 그리면 안 돼요?"), ("doc", "질문 한 줄부터 적어 볼까요?")]
FILES = """| cvs_sales.csv | 2025년 3월 결제 ⟦len(cvs)|,⟧건 (영수증 번호, 시각, 상품군, 금액, 결제수단). 상품군은 한글 |
| cvs_stock.csv | 3월 31일 밤 진열 상품 ⟦len(stock)⟧줄의 유통기한 |
| cvs_cash.csv | 일별 현금 들어온 돈 · 나간 돈(은행 입금, 동전 교환) |"""
NEXT = "[3편 해외 손님에게 가격을 알려 주자 →](../ep3/index.md)"

SECTIONS = [
dict(id="2-1", slug="01-question-first", title="질문을 먼저 적고 답을 한 줄로", short="질문 → 코드 → 답 한 줄",
 goal="데이터를 열기 전에 질문을 한 줄로 적고, 코드를 돌린 뒤 답을 한 줄로 적는 틀을 익힌다.",
 cells=[
  dict(before="먼저 [ep2-cvs.zip](../data/ep2-cvs.zip) 을 올리고 결제 기록을 읽는다.",
       code='''# 2편 실습 파일 묶음(zip)을 올리고 푼다
from google.colab import files
import zipfile, os
up = files.upload()
zipfile.ZipFile(list(up)[0]).extractall()
print(sorted(f for f in os.listdir() if f.startswith("cvs_")))''', prefix="Saving ep2-cvs.zip to ep2-cvs.zip\n",
       run='import os\nprint(sorted(f for f in os.listdir() if f.startswith("cvs_")))'),
  dict(code='''import pandas as pd
enc = "utf-8-sig"
cvs = pd.read_csv("cvs_sales.csv", encoding=enc, parse_dates=["time"])
print(cvs.shape)
print(cvs.head(3))'''),
  dict(before="질문을 코드 위에 주석으로 먼저 쓴다. 그리고 답을 `print` 한 줄로 낸다.",
       code='''# 질문: 3월에 결제가 가장 많은 요일은? 가장 적은 요일과 몇 배 차이인가?
cvs["weekday"] = cvs["time"].dt.day_name().str[:3]
cnt = cvs["weekday"].value_counts()
print(cnt)
print(f"답: {cnt.idxmax()} 이 {cnt.max()}건으로 가장 많고, {cnt.idxmin()} 의 {cnt.max() / cnt.min():.2f}배다.")'''),
 ],
 talk=[("fly", "3월엔 토요일이 다섯 번이잖아. 요일마다 날 수가 다른데 그대로 비교해도 돼?"),
       ("doc", "좋은 의심이에요. 3월은 토 · 일 · 월이 5번씩이라, 2-9 에서 하루 평균으로 다시 봐요.")],
 read="질문이 \"가장 많은 요일\"이니 답은 요일 이름과 숫자 하나면 된다. 차트가 필요한지는 답을 적어 본 뒤에 정한다. "
      "이 답에는 날 수 차이가 섞여 있다는 점도 함께 적어 둔다.",
 **{"try": "질문을 \"결제가 가장 많은 시각(0~23시)은?\" 으로 바꾸고 `cvs[\"time\"].dt.hour.value_counts()` 로 답을 한 줄로 적어 본다."}),

dict(id="2-2", slug="02-korean-labels", title="한글 라벨이 깨지면 영어로 다시", short="rename(사전), 영어 라벨",
 goal="한글 상품군 그대로 차트를 그리면 깨지는 모습을 보고, 사전으로 영어 이름을 붙여 다시 그린다.",
 cells=[
  dict(code='''import matplotlib.pyplot as plt
by_cat = cvs.groupby("category")["amount"].sum() / 1e4      # 만원
by_cat.plot.bar(title="상품군별 매출", ylabel="만원", figsize=(5, 3))
plt.show()''', alt="한글 라벨이 네모로 깨진 막대 차트"),
  dict(before="상품군 이름 → 영어 이름 사전을 만들어 `rename` 한다. 표 안의 값은 그대로 두고 **그림에 쓸 이름만** 바꾼다.",
       code='''eng = {"과자": "Snack", "음료": "Drink", "도시락": "Lunchbox", "라면": "Ramen",
       "아이스크림": "Ice cream", "생활용품": "Daily goods"}
cvs["cat_en"] = cvs["category"].map(eng)
print("unmapped:", cvs["cat_en"].isna().sum())
by_cat = cvs.groupby("cat_en")["amount"].sum() / 1e4
by_cat.sort_values().plot.barh(title="Sales by category (March)", xlabel="KRW 10k", figsize=(5, 3))
plt.show()''', alt="영어 라벨로 다시 그린 상품군별 매출 가로 막대"),
 ],
 talk=[("asst", "표에서는 한글이 멀쩡한데 그림만 네모예요."),
       ("doc", "0-6 에서 본 그거예요. 그림 글꼴에 한글이 없어서요.")],
 read="`map(eng)` 뒤에 `unmapped` 가 0 이어야 모든 상품군이 영어 이름을 받은 것이다. 가로 막대(`barh`)로 바꾸고 값 순서로 정렬하면 "
      "이름이 긴 상품군도 읽기 쉽다. 가장 큰 상품군은 ⟦by_cat.idxmax()⟧ (⟦by_cat.max()|,.0f⟧만원)이다.",
 **{"try": "`eng` 에서 `\"생활용품\"` 줄을 지워 본다. `unmapped` 가 늘고 그 막대가 그림에서 사라진다. 확인했으면 되돌린다."}),

dict(id="2-3", slug="03-mean-or-sum", title="평균이냐 합계냐 · CH-03", short="estimator='sum', 평균 vs 합계",
 goal="같은 데이터로 '결제 1건 평균'과 '합계'를 나란히 그려, 질문에 따라 막대 높이가 달라지는 것을 본다.",
 cells=[
  dict(code='''t = cvs.groupby("cat_en")["amount"].agg(["mean", "sum", "count"])
t["sum"] = t["sum"] / 1e4
print(t.round(0).sort_values("sum", ascending=False))'''),
  dict(before="CH-03. seaborn 의 `barplot` 은 기본이 **평균**이다. 합계를 보려면 `estimator=\"sum\"` 을 꼭 넣는다.",
       code='''import seaborn as sns
order = t.sort_values("sum", ascending=False).index
fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
sns.barplot(data=cvs, x="cat_en", y="amount", order=order, errorbar=None, color="#028090", ax=ax[0])
ax[0].set(title="Default = mean per payment", xlabel="", ylabel="KRW")
cvs["amount_10k"] = cvs["amount"] / 1e4               # 합계는 커서 만원 단위로
sns.barplot(data=cvs, x="cat_en", y="amount_10k", order=order, estimator="sum", errorbar=None, color="#D98E22", ax=ax[1])
ax[1].set(title='estimator="sum" (March total)', xlabel="", ylabel="KRW 10k")
for a in ax: a.tick_params(axis="x", rotation=30)
fig.suptitle("CH-03 Sales by category: mean vs sum")
plt.tight_layout()
plt.show()''', alt="CH-03 상품군별 결제 1건 평균과 월 합계 막대"),
 ],
 talk=[("robo", "합계가 제일 크면 제일 잘 팔린 거지? 삐빅.", "confused"),
       ("doc", "질문에 따라 달라요. 한 번에 많이 쓰는 건 ⟦t['mean'].idxmax()⟧, 한 달에 많이 번 건 ⟦t['sum'].idxmax()⟧예요.")],
 read="왼쪽(평균)은 \"결제 한 번에 얼마나 쓰나\", 오른쪽(합계)은 \"한 달에 얼마 벌었나\"에 답한다. ⟦t['mean'].idxmax()⟧ 은 한 번에 ⟦t['mean'].max()|,.0f⟧원으로 가장 비싸지만, "
      "건수가 많은 ⟦t['sum'].idxmax()⟧ 가 합계 1위(⟦t['sum'].max()|,.0f⟧만원)다.",
 **{"try": "`estimator=\"sum\"` 을 `estimator=\"count\"` 로 바꿔 결제 건수 막대도 그려 본다."}),

dict(id="2-4", slug="04-expiry-buckets", title="유통기한까지 며칠 남았나 · CH-04", short="날짜 빼기, pd.cut",
 goal="진열 상품마다 유통기한까지 남은 날을 계산하고, 구간(버킷)으로 묶어 오늘 밤 치워야 할 것을 센다.",
 cells=[
  dict(code='''stock = pd.read_csv("cvs_stock.csv", encoding=enc, parse_dates=["expiry"])
today = pd.Timestamp("2025-03-31")
stock["days_left"] = (stock["expiry"] - today).dt.days
bins   = [-999, -1, 2, 7, 30, 9999]
labels = ["Expired", "0-2 days", "3-7 days", "8-30 days", "30+ days"]
stock["bucket"] = pd.cut(stock["days_left"], bins=bins, labels=labels)
bq = stock.groupby("bucket", observed=False)["qty"].sum()
print(bq)
print(stock[stock["days_left"] < 0][["product", "qty", "expiry"]])'''),
  dict(before="CH-04. 버킷 순서는 `labels` 순서 그대로 둔다. 급한 쪽을 빨갛게 칠한다.",
       code='''colors = ["#C9382A", "#E8A33A", "#F2C230", "#7FB8A4", "#028090"]
ax = bq.plot.bar(color=colors, figsize=(6, 3), rot=0,
                 title="CH-04 Items by days to expiry (Mar 31 night)", xlabel="", ylabel="Items")
ax.bar_label(ax.containers[0])
plt.show()''', alt="CH-04 유통기한까지 남은 날 구간별 상품 개수 막대"),
 ],
 talk=[("fly", "유통기한 지난 게 ⟦int(bq['Expired'])⟧개 아직 진열대에 있다고?")],
 read="`bins` 는 구간의 경계다. `(-1, 2]` 는 0~2일, `(-999, -1]` 은 이미 지난 것이다. 오늘 밤 치울 것 ⟦int(bq['Expired'])⟧개, "
      "내일모레까지 팔아야 할 것 ⟦int(bq['0-2 days'])⟧개다. 구간 차트는 \"얼마나 급한가\"를 한눈에 보여 준다.",
 **{"try": "`today` 를 `pd.Timestamp(\"2025-04-02\")` 로 바꿔 이틀 뒤의 모습을 본다."}),

dict(id="2-5", slug="05-cash-cumsum", title="cumsum 으로 시재 다시 계산 · CH-05", short="cumsum, 선 + annotate",
 goal="날마다 들어온 현금과 나간 현금으로 계산대 잔액(시재)을 다시 계산하고, 가장 낮은 날에 표시를 단 선 그림을 그린다.",
 cells=[
  dict(code='''cash = pd.read_csv("cvs_cash.csv", encoding=enc, parse_dates=["date"])
opening = 200_000                                    # 3월 1일 아침 계산대 현금
cash["drawer"] = opening + (cash["cash_in"] - cash["cash_out"]).cumsum()
print(cash.head(4))
low = cash.loc[cash["drawer"].idxmin()]
print("lowest:", low["date"].date(), int(low["drawer"]))'''),
  dict(before="CH-05. 가장 낮은 날에 화살표를 단다.",
       code='''fig, ax = plt.subplots(figsize=(8, 3))
ax.plot(cash["date"], cash["drawer"] / 1e4, color="#028090", marker=".")
ax.annotate(f"low {low['drawer'] / 1e4:.1f}", xy=(low["date"], low["drawer"] / 1e4),
            xytext=(low["date"] + pd.Timedelta(days=3), 30), arrowprops=dict(arrowstyle="->"))
ax.set(title="CH-05 CVS cash in drawer (end of day)", ylabel="KRW 10k", ylim=(0, 160))
import matplotlib.dates as mdates
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))   # 날짜는 월-일만
plt.show()''', alt="CH-05 편의점 일별 현금 시재 선과 가장 낮은 날 표시"),
 ],
 talk=[("asst", "월요일마다 뚝 떨어져요. 무슨 일이에요?"),
       ("doc", "월요일 밤에 20만원만 남기고 은행에 넣어서 그래요. 톱니 모양이 정상이에요.")],
 read="`cumsum` 은 위에서부터 차례로 더한 값이다. 기초 20만원에 날마다 (들어온 돈 − 나간 돈)을 쌓으면 그날 밤 계산대 잔액이 된다. "
      "가장 낮은 날은 ⟦low['date'].strftime('%m-%d')⟧ (⟦int(low['drawer'])|,⟧원)이다.",
 **{"try": "`opening` 을 `0` 으로 바꿔 본다. 선 모양은 같고 높이만 20만원 내려간다."}),

dict(id="2-6", slug="06-mean-median", title="평균과 중앙값 · CH-06", short="mean, median, histplot",
 goal="결제 금액의 평균과 중앙값을 비교하고, 히스토그램에 두 선을 그어 왜 다른지 본다.",
 cells=[
  dict(code='''print("mean:  ", round(cvs["amount"].mean()))
print("median:", cvs["amount"].median())
print("top 5:", cvs["amount"].nlargest(5).tolist())'''),
  dict(before="CH-06. 금액을 천원 단위로 바꿔 0~30천원 구간만 그린다.",
       code='''k = cvs["amount"] / 1000
ax = sns.histplot(k, binwidth=1, binrange=(0, 30), color="#028090")
ax.axvline(k.mean(), color="#C9382A", linestyle="--", label=f"mean {k.mean():.1f}")
ax.axvline(k.median(), color="#1C2620", label=f"median {k.median():.1f}")
ax.set(title="CH-06 CVS payment amount (March)", xlabel="KRW thousand", ylabel="Payments")
ax.legend()
plt.show()''', alt="CH-06 결제 금액 히스토그램과 평균선, 중앙값선"),
 ],
 talk=[("asst", "평균은 ⟦round(cvs['amount'].mean())|,⟧원인데 중앙값은 ⟦cvs['amount'].median()|,.0f⟧원이에요.")],
 read="결제 대부분은 1~6천원에 몰려 있고, 오른쪽으로 긴 꼬리가 있다. 몇 안 되는 큰 결제(최대 ⟦cvs['amount'].max()|,⟧원)가 평균을 끌어올린다. "
      "\"보통 손님은 얼마를 쓰나\"에는 중앙값이 더 정직한 답이다.",
 **{"try": "`binwidth=1` 을 `binwidth=0.5` 로 바꿔 막대를 더 잘게 나눠 본다."}),

dict(id="2-7", slug="07-pivot-heatmap", title="시간대 × 요일 피벗 · CH-07", short="pivot_table, heatmap",
 goal="요일 × 시간대 표로 결제 수를 세고, 히트맵으로 붐비는 칸을 찾는다. 이 편의 질문(언제 바쁜가)에 대한 답이다.",
 cells=[
  dict(code='''cvs["hour"] = cvs["time"].dt.hour
cvs["band"] = pd.cut(cvs["hour"], bins=[-1, 5, 9, 13, 17, 21, 23],
                     labels=["0-5", "6-9", "10-13", "14-17", "18-21", "22-23"])
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
pv = cvs.pivot_table(index="band", columns="weekday", values="receipt", aggfunc="count", observed=False)
pv = (pv[days] / cvs.groupby("weekday")["time"].apply(lambda s: s.dt.date.nunique())[days]).round(0)   # 하루 평균
print(pv)'''),
  dict(before="CH-07. 하루 평균 결제 수를 색으로 칠한다.",
       code='''fig, ax = plt.subplots(figsize=(7, 3.6))
sns.heatmap(pv, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
ax.set(title="CH-07 Payments per day: time band x weekday", xlabel="", ylabel="Hour")
plt.show()''', alt="CH-07 시간대와 요일별 하루 평균 결제 수 히트맵"),
 ],
 talk=[("asst", "평일은 ⟦pv[['Mon','Tue','Wed','Thu','Fri']].mean(axis=1).idxmax()⟧시, 주말은 ⟦pv[['Sat','Sun']].mean(axis=1).idxmax()⟧시가 제일 바빠요."),
       ("doc", "그 칸에 사람을 더 두면 돼요. 이게 이 편 질문의 답이에요.")],
 read="요일마다 날 수가 달라서(3월은 토 · 일 · 월이 5번) 칸마다 하루 평균으로 나눴다. 가장 진한 칸은 ⟦pv.stack().idxmax()[1]⟧ ⟦pv.stack().idxmax()[0]⟧시 "
      "(하루 ⟦int(pv.stack().max())⟧건)이다. 평일 아침 6-9시는 붐비지만 주말 아침은 한산하다.",
 **{"try": "`aggfunc=\"count\"` 와 `values=\"receipt\"` 를 `aggfunc=\"sum\"`, `values=\"amount\"` 로 바꿔 건수 대신 매출로 칠해 본다(나누기 줄은 빼고)."}),

dict(id="2-8", slug="08-first-digit", title="영수증 금액의 첫 자리 · CH-08", short="str[0], 벤포드 기대값",
 goal="결제 금액의 첫 자리 숫자(1~9) 비율을 세고, 벤포드 법칙의 기대값과 나란히 놓는다.",
 cells=[
  dict(code='''import numpy as np
first = cvs["amount"].astype(str).str[0].astype(int)
obs = first.value_counts(normalize=True).sort_index() * 100
d = np.arange(1, 10)
benford = pd.Series(np.log10(1 + 1 / d) * 100, index=d)
cmp_ = pd.DataFrame({"observed%": obs.round(1), "benford%": benford.round(1)})
print(cmp_)'''),
  dict(before="CH-08. 막대는 관측, 선은 벤포드 기대값이다.",
       code='''fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(d, obs, color="#028090", label="Observed")
ax.plot(d, benford, color="#D98E22", marker="o", label="Benford")
ax.set(title="CH-08 First digit of CVS payments", xlabel="First digit", ylabel="%", xticks=d)
ax.legend()
plt.show()''', alt="CH-08 결제 금액 첫 자리 비율 막대와 벤포드 기대 선"),
 ],
 talk=[("fly", "첫 자리가 1인 영수증이 왜 제일 많아?"),
       ("doc", "여러 자릿수에 걸쳐 퍼진 금액은 원래 1로 시작하는 게 가장 많아요. 이번엔 ⟦cmp_.loc[1,'observed%']⟧%예요.")],
 read="벤포드 법칙은 1이 30.1%, 9가 4.6% 라고 기대한다. 편의점은 금액대가 좁아(대부분 1~6천원) 꼭 맞지는 않는다. "
      "차이가 크게 나는 숫자는 \"이상하다\"가 아니라 \"들여다볼 곳\"이다. 다음 절에서 하나를 들여다본다.",
 **{"try": "`cvs[\"amount\"]` 대신 `cvs.loc[cvs[\"pay\"] == \"Cash\", \"amount\"]` 로 현금 결제만 세어 본다."}),

dict(id="2-9", slug="09-weekend-round", title="주말과 딱 떨어지는 금액 · CH-09", short="day_name, % 10000, countplot",
 goal="요일별 하루 평균 결제 수를 다시 보고, 만원 단위로 딱 떨어지는 결제가 어느 요일 · 시각에 몰리는지 찾는다.",
 cells=[
  dict(code='''nday = cvs.groupby("weekday")["time"].apply(lambda s: s.dt.date.nunique())
per_day = (cnt / nday)[days].round(0)
print(per_day)
cvs["round"] = cvs["amount"] % 10000 == 0           # 만원 단위로 딱 떨어지나
r = cvs[cvs["round"]]
print("round payments:", len(r))
print(r.groupby(["weekday", "pay"]).size().sort_values(ascending=False).head(4))
print("Sun 22-23h share:", round(((r["weekday"] == "Sun") & (r["hour"] >= 22)).mean() * 100), "%")'''),
  dict(before="CH-09. 요일별로 딱 떨어지는 결제 수를 센다.",
       code='''ax = sns.countplot(data=r, x="weekday", order=days, hue="pay", palette=["#C9382A", "#028090", "#D98E22"])
ax.set(title="CH-09 Round-amount payments (x 10,000 KRW) by weekday", xlabel="", ylabel="Payments")
plt.show()''', alt="CH-09 만원 단위 결제의 요일별 개수, 결제수단별 색"),
 ],
 talk=[("robo", "삐빅! 딱 떨어지는 현금 결제가 일요일 밤에 몰려 있어.", "wrong"),
       ("doc", "틀렸다는 게 아니라 확인할 곳이라는 뜻이에요. 그 시간 근무표부터 봐요.")],
 read="날 수로 나누면 그림이 달라진다. 월요일은 2-1 에서 ⟦list(cnt.index).index('Mon')+1⟧위(⟦cnt['Mon']|,⟧건)였지만 하루 평균으로는 ⟦int(per_day['Mon'])⟧건, 7개 요일 중 ⟦int(per_day.rank(ascending=False, method='min')['Mon'])⟧위다. 만원 단위 결제 ⟦len(r)⟧건 가운데 "
      "⟦round(((r['weekday'] == 'Sun') & (r['hour'] >= 22)).mean() * 100)⟧% 가 일요일 22~23시 현금이다. 포스기에 손으로 금액을 친 흔적일 수 있다.",
 warn=("데이터는 의심을 만들 뿐이다", "이 그림만으로 누가 무엇을 했다고 말할 수 없다. 근무표, 영수증 원본, CCTV 처럼 다른 근거와 맞춰 본 다음에 판단한다."),
 **{"try": "`% 10000 == 0` 을 `% 1000 == 0` 으로 바꿔 본다. 천원 단위는 자연스러운 금액도 많아 요일 차이가 흐려진다."}),
]

OUTRO = [("doc", "① 질문이 차트를 고른다 ② 평균과 합계는 다른 답이다 ③ 답은 한 줄로 적는다"),
         ("asst", "히트맵 한 장에 바쁜 시간이 다 보여요. 평일 ⟦pv[['Mon','Tue','Wed','Thu','Fri']].mean(axis=1).idxmax()⟧시, 주말 ⟦pv[['Sat','Sun']].mean(axis=1).idxmax()⟧시."),
         ("fly", "외국 손님은 원화 가격을 어떻게 읽어?")]
