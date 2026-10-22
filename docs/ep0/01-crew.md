# 0-1 상담소 식구를 소개합니다

!!! abstract "이 절에서 할 일"
    이 연습장 곳곳에서 말을 거는 네 식구를 알아 둔다. 누가 무엇을 맡는지 알면 말풍선을 빨리 읽을 수 있다.

동네 상가 2층에 "장부 상담소"가 있다. 카페 Koi, 동네 편의점, 의류 쇼핑몰 사장님들이 장부 파일을 들고 찾아오면, 식구 넷이 Colab 을 켜고 함께 푼다.

<div class="crew" markdown>
<div class="mate"><div class="say only" data-who="doc" data-face="doc_smile"></div><div><b>박사 · 상담소장</b><small>어려운 개념을 비유로 풀고, 꼭 숫자로 닫는다. 편 끝에 핵심 세 줄을 정리한다.</small><q>숫자로 한번 해 볼까요?</q></div></div>
<div class="mate"><div class="say only" data-who="asst" data-face="asst_smile"></div><div><b>세라 · 신입 매니저</b><small>여러분 대신 "왜요?"를 묻고, 실행한 숫자를 소리 내어 읽어 준다. 판정은 하지 않는다.</small><q>잠깐만요, 그건 왜요?</q></div></div>
<div class="mate"><div class="say only" data-who="fly" data-face="fly_point"></div><div><b>초파리 연구원 · 검수 담당</b><small>작지만 날카롭다. 빠진 줄, 숨은 공백을 먼저 의심하고, 편 끝에 다음 편으로 가는 질문을 던진다.</small><q>그 숫자, 처음 보는 데이터로도 맞아?</q></div></div>
<div class="mate"><div class="say only" data-who="robo"></div><div><b>Money-Robo · 계산대 로봇</b><small>계산이 맞는지 얼굴과 가슴 불빛으로 보여 준다. 큰 숫자를 좋아해서 가끔 너무 일찍 기뻐한다.</small><q>삐빅, 계산 중…</q></div></div>
</div>

## Money-Robo 의 불빛 읽는 법

검증 셀을 실행할 때마다 Money-Robo 의 테두리 색이 바뀐다.

<div class="say" data-who="robo" data-state="idle">대기 중. 아직 아무것도 안 봤어.</div>
<div class="say" data-who="robo" data-state="thinking">삐빅, 계산 중…</div>
<div class="say" data-who="robo" data-state="confused">빈칸이 남아 있어. 이대로 더해도 돼?</div>
<div class="say" data-who="robo" data-state="wrong">삐빅! 합계가 안 맞아.</div>
<div class="say" data-who="robo" data-state="success">삐빅! 줄 수도 합계도 맞았어!</div>

| 불빛 | 뜻 | 이럴 때 |
|---|---|---|
| 파랑 | 대기 | 아직 실행 전 |
| 노랑 | 계산 중 | 셀이 도는 중 |
| 주황 | 보류 | 빈칸이나 숨은 공백이 남음 |
| 빨강 | 틀림 | 줄 수나 합계가 안 맞음 |
| 초록 | 맞음 | 줄 수와 합계가 맞음 |

!!! note "말풍선 그림"
    지금은 동그라미 안에 글자(박 · 세 · 초 · R)가 보인다. 캐릭터 그림을 넣으면 자동으로 그림으로 바뀐다.

<label class="done"><input type="checkbox" data-step="0-1"> 0-1 을 끝냈어요</label>
