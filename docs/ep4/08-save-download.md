# 4-8 보고서용으로 저장하고 내려받기

!!! abstract "이 절에서 할 일"
    사장님께 드릴 그림을 고해상도 PNG 로 저장하고, Colab 에서 내 컴퓨터로 내려받는다.

```python
fig, ax = plt.subplots(figsize=(6.5, 4))
cf = ax.contourf(P, B, Z, levels=20, cmap="RdYlGn")
ax.contour(P, B, Z, levels=[0], colors="black", linewidths=2)
ax.plot(4500, 14, "w*", markersize=14, markeredgecolor="black")
ax.set(title="Koi coffee: price x bean cost -> monthly profit", xlabel="Price (KRW)", ylabel="Beans (USD per kg)")
fig.colorbar(cf, label="KRW 10k")
fig.savefig("koi_breakeven.png", dpi=200, bbox_inches="tight")    # 보고서용 고해상도
print("saved:", round(os.path.getsize("koi_breakeven.png") / 1024), "KB")
plt.close(fig)
```

```text title="실행 결과"
saved: 91 KB
```

```python
# Colab 에서만 동작한다. 브라우저가 파일을 내려받는다
try:
    from google.colab import files
    files.download("koi_breakeven.png")
except ImportError:
    print("Colab 이 아니면 왼쪽 파일 목록이나 작업 폴더에서 직접 연다")
```

```text title="실행 결과"
Colab 이 아니면 왼쪽 파일 목록이나 작업 폴더에서 직접 연다
```

Colab 에서는 아무것도 찍히지 않고 브라우저 아래쪽에 내려받기가 뜬다. 처음이면 "여러 파일 다운로드 허용" 창이 나올 수 있다.

<div class="say" data-who="asst">dpi 는 왜 200 이에요?</div>
<div class="say" data-who="doc">화면용은 100 이면 되지만, 인쇄하면 흐려져요. 보고서는 200 이상으로 저장해요.</div>

!!! info "읽는 법"
    `bbox_inches="tight"` 는 그림 둘레의 빈 여백을 잘라 준다. `plt.close(fig)` 는 저장만 하고 화면에는 다시 그리지 않는다. 저장한 파일 크기는 91KB 다.

!!! tip "바꿔 보기"
    `dpi=200` 을 `dpi=80` 으로 바꿔 저장하고 두 파일을 확대해 비교해 본다.

<label class="done"><input type="checkbox" data-step="4-8"> 4-8 끝냈어요</label>

<div class="outro" markdown>
4편 정리

<div class="say" data-who="doc">① 큐브는 잘라야 읽힌다 ② 가정은 한곳에 모은다 ③ 이번 데이터에서는 등고선이 더 잘 읽힌다</div>
<div class="say" data-who="asst">환율 가정 한 줄 바꾸니 손익분기 가격이 200원 올라갔어요.</div>
<div class="say" data-who="fly">그럼 네 가게라면 어떤 그림 한 장이야?</div>

[마감 내 가게 한 장 →](../final/index.md)
</div>
