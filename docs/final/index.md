# 마감 내 가게 한 장

카페 Koi, 동네 편의점, 의류 쇼핑몰 중 **한 가게**를 골라 사장님께 드릴 **한 장**을 만든다. 1~4편에서 쓴 파일과 코드를 그대로 다시 쓴다. 1~2시간이면 충분하다.

<div class="say" data-who="fly">그럼 네 가게라면 어떤 그림 한 장이야?</div>
<div class="say" data-who="doc">질문 하나, 표 하나, 검증 셋, 그림 한 장, 답 한 줄. 그거면 돼요.</div>

## 낼 것 다섯 가지

| 순서 | 낼 것 | 예 (편의점) | 다시 볼 곳 |
|---|---|---|---|
| ① | **질문 1개** (사장님 말투로) | "토요일 아침에 알바를 줄여도 될까?" | [2-1](../ep2/01-question-first.md) |
| ② | **표 1개** (질문에 답하는 데 쓴 표) | 요일 × 시간대 하루 평균 결제 수 | [2-7](../ep2/07-pivot-heatmap.md) |
| ③ | **검증 3가지** (줄 수 · 합계 · 빈칸) | 결제 7,810건 그대로, 칸 합 = 전체, 빈칸 0 | [1-12](../ep1/12-checks.md) |
| ④ | **그림 1장** (영어 라벨, 제목에 질문) | CH-07 같은 히트맵 | [0-6](../ep0/06-hangul.md), [4-8](../ep4/08-save-download.md) |
| ⑤ | **답 한 줄** (숫자 포함) | "토요일 6-9시는 하루 21건으로 평일(50건대)의 절반도 안 되니 줄여도 된다." | [2-1](../ep2/01-question-first.md) |

## 시작 셀

빈 노트에 아래 셀을 붙이고, `질문`, `표`, `그림` 자리를 채운다. 파일은 그 편의 zip 을 올린다.

```python
# ① 질문: ____________________________________________
import pandas as pd
import matplotlib.pyplot as plt
enc = "utf-8-sig"
df = pd.read_csv("______.csv", encoding=enc)          # 1·2·3편 중 하나

# ② 표: 질문에 답하는 표 하나
table = ______

# ③ 검증 세 가지
print("① rows:", len(df))                              # 원본 줄 수와 같은가 / 중복은?
print("② sum check:", ______)                          # 표의 합 − 원본의 합 == 0 ?
print("③ missing:", df.isna().sum().sum())             # 계산에 쓴 열에 빈칸은?

# ④ 그림: 제목에 질문을, 라벨은 영어로
fig, ax = plt.subplots(figsize=(7, 3.5))
______
ax.set(title="______?")
fig.savefig("my_store.png", dpi=200, bbox_inches="tight")
plt.show()

# ⑤ 답 한 줄 (숫자 포함)
print("답:", ______)
```

## 스스로 점검표

- [ ] 질문이 "~할까?", "언제 ~?"처럼 **결정**으로 끝난다
- [ ] 표의 숫자가 그림과 답 한 줄에 그대로 나온다
- [ ] 검증 세 가지를 **그림보다 먼저** 실행했다
- [ ] 그림 라벨이 영어이고, 단위(KRW, KRW 10k, %)가 축에 있다
- [ ] 답 한 줄에 숫자가 하나 이상 있다
- [ ] 가정(4편)을 썼다면 그 가정을 답 옆에 적었다
- [ ] 초파리처럼 한 번 더 의심했다: "날 수가 달라도 비교해도 되나?", "같이 움직였을 뿐 아닌가?"

<div class="say" data-who="asst">다 하면 그림 파일 하나랑 답 한 줄을 사장님께 드리면 되는 거죠?</div>
<div class="say" data-who="robo" data-state="success">삐빅! 검증 세 개 통과한 그림이면 자신 있게 드려도 돼!</div>

<label class="done"><input type="checkbox" data-step="9-1"> 내 가게 한 장을 끝냈어요</label>

<div class="outro" markdown>
연습장 정리

<div class="say" data-who="doc">① 읽으면 모양과 빈칸부터 ② 질문이 차트를 고른다 ③ 바깥 데이터는 백업을 둔다 ④ 가정은 한곳에 모은다. 그리고 늘, 검증이 그림보다 먼저다.</div>
<div class="say" data-who="asst">장부 정리 끝. 숫자는 전부 다시 잴 수 있어요.</div>
<div class="say" data-who="fly">다음 장부엔 어떤 함정이 숨어 있을까?</div>

[처음으로 →](../index.md)
</div>
