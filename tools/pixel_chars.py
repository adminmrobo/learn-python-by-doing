"""해상도 통일: 모든 캐릭터를 같은 '그림 픽셀' 격자로 다시 찍는다.
- 초상: 64x64 격자 (머리 약 38칸 = 60%) → 8배 = 512x512
- 대표 그림: 배경(300x200 격자)과 같은 격자에 머리 약 37칸으로 얹은 뒤 4배
AI 그림은 면적 평균으로 줄이고(BOX) 색을 줄여 픽셀아트 결로 맞춘다. 주판봇은 fruitfly-lab-expressions 의 표정 그림(tools/chars_src/jupanbot/)을 같은 격자로 찍는다."""
import math
from PIL import Image

import os
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chars_src")
HEAD = {"doc": ("doc_src.webp", 84, 66, 122), "asst": ("asst_src.webp", 84, 72, 120), "fly": ("fly_src.webp", 88, 52, 80)}

def crisp(im, colors=72):
    """알파는 0/255 로, 색은 팔레트로 줄여 픽셀아트처럼"""
    r, g, b, a = im.split()
    a = a.point(lambda v: 255 if v >= 110 else 0)
    rgb = Image.merge("RGB", (r, g, b)).quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    out = rgb.convert("RGBA"); out.putalpha(a); return out

def downsample(img, w, h):
    # 미리 곱한 알파로 줄여야 테두리가 하얗게 번지지 않는다
    pm = img.convert("RGBa").resize((w, h), Image.BOX).convert("RGBA")
    return crisp(pm)

# ---------- 주판봇: fruitfly-lab-expressions/images/jupanbot 의 표정 그림을 같은 격자로 ----------
# 상태 → 표정 번호 (E13 기본, E09 생각, E24 충격, E15 당황, E10 확인)
ROBO_SRC={"idle":"E13_neutral.png","thinking":"E09_thinking.png","wrong":"E24_shock.png",
          "confused":"E15_flustered.png","success":"E10_confirming.png"}
def robo_src(state):
    """흰 배경을 모서리부터 지워 투명하게 한 원본 (tools/chars_src/jupanbot/)"""
    from PIL import ImageDraw
    im=Image.open(os.path.join(SRC,"jupanbot",ROBO_SRC[state])).convert("RGBA")
    for xy in [(0,0),(im.width-1,0),(0,im.height-1),(im.width-1,im.height-1)]:
        ImageDraw.floodfill(im,xy,(0,0,0,0),thresh=40)
    return im.crop(im.getbbox())

# ---------- 초상 ----------
GRID=64; HEAD_FRAC=0.60; TOP=0.42
def portrait_src(im,cx,cy,h):
    S=h/HEAD_FRAC; x0,y0=cx-S/2,cy-S*TOP
    canvas=Image.new("RGBA",(int(round(S)),)*2,(0,0,0,0))
    canvas.alpha_composite(im.crop((int(round(x0)),int(round(y0)),int(round(x0+S)),int(round(y0+S)))),(0,0))
    return downsample(canvas,GRID,GRID).resize((GRID*8,GRID*8),Image.NEAREST)
def portrait_robo(state, frac=0.86, top=2):
    """주판봇은 몸 전체가 머리 역할이라 전신을 격자의 86% 크기로 위쪽에 맞춘다"""
    r=robo_src(state); S=GRID; k=S*frac/max(r.width,r.height)
    w,h=max(1,round(r.width*k)),max(1,round(r.height*k))
    sm=downsample(r,w,h); canvas=Image.new("RGBA",(S,S),(0,0,0,0)); canvas.alpha_composite(sm,((S-w)//2,top))
    return canvas.resize((S*8,S*8),Image.NEAREST)

# ---------- 대표 그림용 스프라이트 (배경과 같은 격자) ----------
def scene_sprite(name, head_px, flip=False, state="idle"):
    if name=="robo":
        im=robo_src(state); s=head_px/(im.height*0.6)
        r=downsample(im,max(1,round(im.width*s)),max(1,round(im.height*s)))
    else:
        f,cx,cy,h=HEAD[name]; im=Image.open(os.path.join(SRC,f)).convert("RGBA"); s=head_px/h
        r=downsample(im,max(1,round(im.width*s)),max(1,round(im.height*s)))
    return r.transpose(Image.FLIP_LEFT_RIGHT) if flip else r

if __name__=="__main__":
    # usage: python pixel_chars.py <출력 폴더>   (예: assets/chars)
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    names={"doc":"doc_smile","asst":"asst_smile","fly":"fly_point"}
    for k,(f,cx,cy,h) in HEAD.items():
        portrait_src(Image.open(os.path.join(SRC,f)).convert("RGBA"),cx,cy,h).save(os.path.join(out, names[k] + ".png"))
    for st in ["idle","thinking","wrong","confused","success"]:
        portrait_robo(st).save(os.path.join(out, f"robo_{st}.png"))
    print("saved to", out)
