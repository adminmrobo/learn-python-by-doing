# 0-5 실행 규칙 세 가지

!!! abstract "이 절에서 할 일"
    결과가 이 페이지와 다르게 나올 때 대부분은 아래 세 규칙 중 하나를 놓친 것이다. 미리 알아 둔다.

1. **위에서부터 순서대로 실행한다.**
   뒤 절은 앞 절에서 만든 이름(예: `menu`, `book`)을 쓴다. 0-4 를 0-3 보다 먼저 실행하면 `NameError: name 'menu' is not defined` 가 나온다.
2. **멈췄으면 업로드 셀부터 다시.**
   Colab 을 다시 열었거나 파일이 사라졌다면, 그 편의 업로드 셀부터 순서대로 다시 실행한다. 메뉴 **런타임 → 이전 셀 모두 실행**을 쓰면 빠르다.
3. **결과는 이 페이지와 같아야 한다.**
   다르면 앞 절을 건너뛰었거나 숫자를 바꿔 둔 것이다. "바꿔 보기"는 원래 값으로 한 번 실행한 **뒤에** 하고, 끝나면 원래대로 되돌린다.

<div class="say" data-who="asst">오류 메시지가 빨갛고 길어요. 어디부터 봐요?</div>
<div class="say" data-who="doc">맨 아래 줄부터요. 거기에 무엇이 틀렸는지 한 줄로 적혀 있어요.</div>

```text title="자주 보는 맨 아래 줄"
NameError: name 'menu' is not defined          ← 앞 셀을 실행하지 않았다
FileNotFoundError: ... 'koi_menu.csv'          ← 파일이 없다 (업로드 셀부터 다시)
KeyError: 'Price'                              ← 열 이름 철자가 다르다 (price)
SyntaxError: unterminated string literal       ← 따옴표를 하나 빠뜨렸다
```

!!! tip "바꿔 보기"
    일부러 `print(menu["Price"])` 를 실행해 `KeyError` 를 직접 만나 본다. 그다음 `"price"` 로 고쳐 다시 실행한다.

<label class="done"><input type="checkbox" data-step="0-5"> 0-5 를 끝냈어요</label>
