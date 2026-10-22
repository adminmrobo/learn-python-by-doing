# 1-3 지저분한 원가표 엑셀 날것으로 보기

!!! abstract "이 절에서 할 일"
    제목 줄 · 빈 행 · ₩ 글자가 섞인 엑셀을 손대지 않고 먼저 본다.

```python
# header=None: 첫 줄을 열 이름으로 쓰지 말고 있는 그대로 보여 달라
raw = pd.read_excel("koi_cost.xlsx", header=None)
print(raw)
```

```text title="실행 결과"
                  0       1       2           3
0     카페 Koi 메뉴 원가표     NaN     NaN         NaN
1  2025년 기준 · 단위: 원     NaN     NaN         NaN
2              menu  price    cost      updated
3         Americano  ₩4,500  ₩1,200  2025-01-02
4            Latte   ₩5,000  ₩1,600  2025-01-02
5               NaN     NaN     NaN         NaN
6          Iced Tea  ₩5,500  ₩1,100  2025-05-20
7        Cheesecake  ₩6,000  ₩2,400  2025-03-11
8        Croissant   ₩3,500  ₩1,300           -
```

<div class="say" data-who="asst">위에 두 줄은 제목이고, 진짜 열 이름은 세 번째 줄이네요?</div>
<div class="say" data-who="doc">맞아요. 사람이 보기 좋게 만든 엑셀은 거의 다 이래요.</div>

!!! info "읽는 법"
    0 · 1번 줄은 병합된 제목, 2번 줄이 진짜 열 이름, 5번 줄은 통째로 빈 줄이다. 가격과 원가는 `₩4,500` 처럼 **글자**로 들어 있고, Croissant 의 `updated` 는 `-` 다. 무엇을 청소해야 할지 이 화면에서 정한다.

!!! tip "바꿔 보기"
    `header=None` 을 빼고 읽어 본다. 제목 줄이 열 이름이 되어 버리는 모습을 확인한다.

<label class="done"><input type="checkbox" data-step="1-3"> 1-3 끝냈어요</label>
