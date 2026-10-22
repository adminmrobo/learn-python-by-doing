# 1-4 청소 ① 제목 줄, 빈 행, 열 이름 공백

!!! abstract "이 절에서 할 일"
    제목 두 줄을 건너뛰고, 완전히 빈 행을 지우고, 열 이름의 앞뒤 공백을 없앤다.

```python
# 위 두 줄(제목)을 건너뛰고 읽는다
cost = pd.read_excel("koi_cost.xlsx", skiprows=2)
print("before:", list(cost.columns))
cost = cost.dropna(how="all")              # 칸이 전부 빈 줄만 지운다
cost.columns = cost.columns.str.strip()    # 열 이름 앞뒤 공백 지우기
print("after: ", list(cost.columns))
print(cost)
```

```text title="실행 결과"
before: [' menu', 'price ', ' cost ', 'updated']
after:  ['menu', 'price', 'cost', 'updated']
         menu   price    cost     updated
0   Americano  ₩4,500  ₩1,200  2025-01-02
1      Latte   ₩5,000  ₩1,600  2025-01-02
3    Iced Tea  ₩5,500  ₩1,100  2025-05-20
4  Cheesecake  ₩6,000  ₩2,400  2025-03-11
5  Croissant   ₩3,500  ₩1,300           -
```

<div class="say" data-who="fly">' menu' 랑 'menu' 가 달라? 눈으로는 똑같은데.</div>

!!! info "읽는 법"
    `before` 의 `' menu'`, `'price '` 처럼 열 이름에 공백이 붙어 있으면 `cost["menu"]` 가 `KeyError` 를 낸다. `dropna(how="all")` 은 모든 칸이 빈 줄만 지우므로, 일부만 빈 줄은 살아남는다. 줄 번호 2 가 빠진 것이 지운 빈 행이다.

!!! tip "바꿔 보기"
    `how="all"` 을 빼고 `cost.dropna()` 만 써 본다. `updated` 가 비어 있는 줄이 생기면 그 줄까지 사라질 수 있다.

<label class="done"><input type="checkbox" data-step="1-4"> 1-4 끝냈어요</label>
