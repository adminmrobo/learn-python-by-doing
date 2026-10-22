# 쉽게 따라 해 보면서 배우는 파이썬

**카페 · 편의점 · 쇼핑몰 데이터로 한 절씩 따라 하는 파이썬 데이터 연습장**

위키독스처럼 왼쪽 목차에서 절을 골라 한 페이지씩 따라 합니다. 절마다 Colab 코드, 실제 실행 결과, 읽는 법, 바꿔 보기, 완료 체크가 있고, 장부 상담소 식구 넷(박사 · 세라 · 초파리 · Money-Robo)이 중간중간 묻고 답합니다.

| 편 | 상태 |
|---|---|
| 0편 시작하기 (6절) | 완성 |
| 1편 카페 Koi의 장부를 연다 (13절) | 완성 |
| 2편 편의점은 언제 바쁜가 (9절) | 완성 |
| 3편 해외 손님에게 가격을 알려 주자 (9절) | 완성 |
| 4편 가격을 바꾸면 이익이 움직인다 (8절) | 완성 |
| 마감 내 가게 한 장 | 완성 |

## GitHub Pages 에 올리기 (처음 한 번)
1. `mkdocs.yml` 맨 위의 `site_url`, `repo_url` 에서 `USER` 를 내 GitHub 계정으로 바꿉니다(repo 이름이 다르면 그것도). **"Colab 에서 열기" 버튼이 이 주소로 노트북을 엽니다.**
2. 이 폴더를 repo 에 올립니다(`main` 브랜치).
3. Settings → Pages → Source 를 **GitHub Actions** 로 고릅니다.
4. Actions 탭에서 `deploy` 가 초록색이 되면 `https://<계정>.github.io/learn-python-by-doing/` 에서 열립니다. 이후에는 `main` 에 올릴 때마다 자동으로 다시 만들어집니다.

## 내 컴퓨터에서 미리 보기
```bash
pip install -r requirements.txt
mkdocs serve          # http://127.0.0.1:8000
```

## 폴더
```
docs/                 사이트 원고 (마크다운). 절 하나 = 파일 하나
  ep0/ … ep4/, final/ 편별 페이지
  data/               편별 실습 zip (ep0-start.zip)
  notebooks/          편별 Colab 노트북 (ep0.ipynb)
  assets/chars/       캐릭터 그림 넣는 곳 (없으면 글자 배지)
  stylesheets/, javascripts/   말풍선 · Colab 버튼 · 완료 체크
tools/make_ep0.py     0편 데이터와 그림을 만들고 실행 결과를 확인
tools/make_ep1_data.py   1편 실습 데이터(ep1-cafe.zip)를 만든다
tools/ep1_content.py     1편 원고 (설명, 코드, 대사)
tools/make_ep2_data.py   2편 실습 데이터(ep2-cvs.zip)
tools/ep2_content.py     2편 원고
tools/make_ep3_data.py   3편 실습 데이터(ep3-shop.zip). 환율 백업은 연습용 값
tools/ep3_content.py     3편 원고
tools/ep4_content.py     4편 원고 (데이터는 1편 ep1-cafe.zip 을 다시 쓴다)
tools/build_episode.py   원고의 코드를 실제로 실행해 docs/ep1/*.md, 그림, 노트북, 목차를 만든다
mkdocs.yml            사이트 설정과 목차
```

## 편 고치기
원고 `tools/epN_content.py` 를 고친 뒤 아래를 실행하면 페이지와 실행 결과, 그림, 노트북이 다시 만들어진다. 문장 속 `⟦식⟧` 자리는 실행한 숫자로 채워진다.
```bash
pip install pandas==2.2.3 matplotlib openpyxl
python tools/build_episode.py 1     # 2편이면 2
```

## 말풍선 쓰는 법 (마크다운 안에서)
```html
<div class="say" data-who="asst">세라의 질문</div>
<div class="say" data-who="doc">박사의 답</div>
<div class="say" data-who="fly">초파리의 의심</div>
<div class="say" data-who="robo" data-state="success">삐빅! 맞았어!</div>   <!-- idle|thinking|confused|wrong|success -->
```

---
제작 안상선 (Ahn, Sang-Sun) · sangsun.ahn@gmail.com · © 2026 All rights reserved.
예제 속 가게와 숫자는 모두 지어낸 것입니다. Money-Robo는 저자 서비스의 마스코트이며, 극 중 대사는 비유일 뿐 투자 권유가 아닙니다.
