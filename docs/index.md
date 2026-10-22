---
hide: [navigation]
---
# 쉽게 따라 해 보면서 배우는 파이썬

**카페 · 편의점 · 쇼핑몰 데이터로 한 절씩 따라 하는 파이썬 데이터 연습장**

한 절은 Colab 에서 10~15분이면 끝난다. 코드를 붙여 넣고 실행하고, 결과를 이 페이지와 맞춰 보고, 다음 절로 넘어간다. 그게 전부다.

<div class="say" data-who="asst">코드는 처음인데, 정말 따라 할 수 있을까요?</div>
<div class="say" data-who="doc">한 절에 한 가지만 해요. 숫자는 늘 화면에 보이게 하고요.</div>

## 이렇게 짜여 있다

| 편 | 가게 | 이 편에서 익히는 것 |
|---|---|---|
| [0편 시작하기](ep0/index.md) | 장부 상담소 | Colab, 파일 올리기, 코드 읽는 법, 한글 깨짐 |
| [1편 카페 Koi의 장부를 연다](ep1/index.md) | 카페 Koi | 읽기, 청소, map · merge, 합계 검증 |
| [2편 편의점은 언제 바쁜가](ep2/index.md) | 동네 편의점 | 질문 먼저, 차트 7종 |
| [3편 해외 손님에게 가격을 알려 주자](ep3/index.md) | 의류 쇼핑몰 | yfinance 환율, 바깥 데이터 다루기 |
| [4편 가격을 바꾸면 이익이 움직인다](ep4/index.md) | 카페 Koi | 데이터 큐브, 민감도 등고선 |
| [마감 내 가게 한 장](final/index.md) | 셋 중 하나 | 미니 프로젝트 |

## 장부 상담소 식구

동네 상가 2층 "장부 상담소". 가게 사장님들이 장부를 들고 오면 식구 넷이 함께 푼다. 자세한 소개는 [0-1](ep0/01-crew.md) 에 있다.

<div class="crew" markdown>
<div class="mate"><div class="say only" data-who="doc" data-face="doc_smile"></div><div><b>박사 · 상담소장</b><small>비유로 풀고 숫자로 닫는다.</small></div></div>
<div class="mate"><div class="say only" data-who="asst" data-face="asst_smile"></div><div><b>세라 · 신입 매니저</b><small>여러분 대신 "왜요?"를 묻는다.</small></div></div>
<div class="mate"><div class="say only" data-who="fly" data-face="fly_point"></div><div><b>초파리 연구원 · 검수 담당</b><small>늘 한 번 더 의심한다.</small></div></div>
<div class="mate"><div class="say only" data-who="robo"></div><div><b>Money-Robo · 계산대 로봇</b><small>계산이 맞는지 얼굴로 보여 준다.</small></div></div>
</div>

!!! note "이 연습장의 숫자"
    예제 속 가게, 손님, 환율, 금액은 모두 연습용으로 지어낸 값이다. Money-Robo는 저자 서비스의 마스코트이며, 극 중 대사는 비유일 뿐 투자 권유가 아닙니다.
