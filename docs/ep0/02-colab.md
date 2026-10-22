# 0-2 Colab 열기

!!! abstract "이 절에서 할 일"
    Colab 에 새 노트를 만들고, 셀 하나를 실행해 본다.

Colab 은 브라우저 안의 파이썬 연습장이다. 설치할 것이 없고, 구글 계정만 있으면 된다.

1. 브라우저에서 [colab.research.google.com](https://colab.research.google.com) 에 들어가 구글 계정으로 로그인한다.
2. **새 노트**를 누르면 빈 노트북이 열린다. 회색 상자 하나가 **셀(코드 칸)** 이다.
3. 아래 코드를 셀에 붙여 넣고 ++shift+enter++ 를 누른다. 결과는 셀 바로 아래에 나온다.
4. 다음 코드는 **+ 코드** 버튼으로 새 셀을 만들어 붙여 넣는다. **한 셀에 한 단계씩** 넣는다.

```python
# 첫 셀: 화면에 인사를 찍어 본다
print("Hello, Cafe Koi!")
print(4500 * 2)
```

```text title="실행 결과"
Hello, Cafe Koi!
9000
```

<div class="say" data-who="asst">처음 실행이 좀 느린데, 고장 난 거예요?</div>
<div class="say" data-who="doc">처음 한 번은 Colab 이 컴퓨터를 빌려 오느라 몇 초 걸려요.</div>

!!! info "읽는 법"
    `print(...)` 는 괄호 안을 화면에 보여 준다. 따옴표 안은 글자 그대로, 따옴표 밖의 `4500 * 2` 는 계산한 값이 나온다.

!!! tip "바꿔 보기"
    `4500 * 2` 를 `4500 * 3 + 5000` 으로 바꿔 아메리카노 세 잔과 라테 한 잔 값을 계산해 본다.

!!! tip "노트북을 통째로 열고 싶다면"
    이 편의 코드를 모두 담은 노트북이 있다. <a class="colab" data-nb="ep0.ipynb">▶ Colab 에서 열기</a> 를 누르고, 상단 **드라이브에 사본 저장**을 하면 내 노트로 고쳐 쓸 수 있다.

<label class="done"><input type="checkbox" data-step="0-2"> 0-2 를 끝냈어요</label>
