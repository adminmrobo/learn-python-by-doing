# 3-9 AI 가격표 JSON 검증하고 저장

!!! abstract "이 절에서 할 일"
    AI 가 만들어 준 외국어 가격표를 그대로 쓰지 않고, "외화 × 환율 ≈ 원화" 인지 통화마다 확인한 뒤 고쳐서 저장한다.

```python
import json
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
print(a[["usd_ok", "jpy_ok", "cny_ok"]].sum())
```

```text title="실행 결과"
2025-12-31 {'USD': 1467.3, 'JPY_per_100': 943.3, 'CNY': 206.75} JPY rate is per 100 yen
    item     krw    usd  jpy  cny  usd_ok  jpy_ok  cny_ok
0    Tee   19000   13.0   20   92    True   False    True
1  Shirt   39000   26.5   41  189    True   False    True
2   Knit   59000   40.0   63  285    True   False    True
3  Denim   89000   60.5   94  430    True   False    True
4   Coat  189000  129.0  200  914    True   False    True
5    Cap   25000   17.0   27  121    True   False    True
6  Socks    6000    4.0    6   29    True   False    True
usd_ok    7
jpy_ok    0
cny_ok    7
dtype: int64
```

엔화가 전부 실패했다. AI 가 '100엔에 943.3원' 숫자를 1엔 값처럼 나눴다. 1엔 값으로 다시 계산하고, 다시 검증한 뒤 저장한다.

```python
a["jpy"] = (a["krw"] / (r["JPY_per_100"] / 100)).round(-1)     # 1엔 = 9.433원 으로 나누고 10엔 단위
a["jpy_ok"] = (a["jpy"] * r["JPY_per_100"] / 100 / a["krw"] - 1).abs() < 0.01
print(a[["item", "krw", "usd", "jpy", "cny", "jpy_ok"]])
out = a[["item", "krw", "usd", "jpy", "cny"]]
out.to_csv("price_tag_checked.csv", index=False, encoding="utf-8-sig")
print("saved:", len(out), "rows")
```

```text title="실행 결과"
    item     krw    usd      jpy  cny  jpy_ok
0    Tee   19000   13.0   2010.0   92    True
1  Shirt   39000   26.5   4130.0  189    True
2   Knit   59000   40.0   6250.0  285    True
3  Denim   89000   60.5   9430.0  430    True
4   Coat  189000  129.0  20040.0  914    True
5    Cap   25000   17.0   2650.0  121    True
6  Socks    6000    4.0    640.0   29    True
saved: 7 rows
```

<div class="say" data-who="robo" data-state="wrong">삐빅! 엔화 가격이 전부 틀렸어. 100배 작아.</div>
<div class="say" data-who="robo" data-state="success">삐빅! 다시 검증, 세 통화 모두 통과!</div>

!!! info "읽는 법"
    AI 는 `note` 에 "100엔 기준"이라고 적어 놓고도 계산은 1엔 기준처럼 했다. 결과가 그럴듯해 보여도 **되돌려 곱해 보면** 바로 드러난다. 달러(반올림 폭 0.25달러 안)와 위안(1% 안)은 처음부터 통과했고, 엔화는 고친 뒤 통과했다. 검사 기준도 "어떻게 만들었나"에 맞춰 정한다. 0.5달러 단위로 반올림한 값에 1% 기준을 대면 6,000원짜리 양말처럼 싼 상품이 억울하게 떨어진다. 검증한 표만 `utf-8-sig` 로 저장한다(0-6).

!!! warning "AI 답은 초안이다"
    AI 가 만든 숫자는 사람이 만든 숫자와 똑같이 검증한다. 검증 코드는 한 번 써 두면 다음 달 가격표에도 그대로 쓸 수 있다.

!!! tip "바꿔 보기"
    Colab 왼쪽 파일 창에서 `price_tag_checked.csv` 를 내려받아 엑셀로 열어 본다. 한글 없이도 깨지지 않는지 확인한다.

<label class="done"><input type="checkbox" data-step="3-9"> 3-9 끝냈어요</label>

<div class="outro" markdown>
3편 정리

<div class="say" data-who="doc">① 바깥 데이터는 막힐 수 있다, 백업을 둔다 ② 환율은 방향과 단위부터 본다 ③ 빈 날은 채우는 규칙을 정한다</div>
<div class="say" data-who="asst">백업 CSV 로도 같은 표가 나왔고, AI 가격표의 엔화 실수도 잡았어요.</div>
<div class="say" data-who="fly">가격이랑 환율이 같이 바뀌면 이익은?</div>

[4편 가격을 바꾸면 이익이 움직인다 →](../ep4/index.md)
</div>
