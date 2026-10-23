"""해상도 통일: 모든 캐릭터를 같은 '그림 픽셀' 격자로 다시 찍는다.
- 초상: 64x64 격자 (머리 약 38칸 = 60%) → 8배 = 512x512
- 대표 그림: 배경(300x200 격자)과 같은 격자에 머리 약 37칸으로 얹은 뒤 4배
AI 그림은 면적 평균으로 줄이고(BOX) 색을 줄여 픽셀아트 결로 맞춘다. Money-Robo 는 같은 격자에서 도형으로 직접 다시 그린다."""
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

# ---------- Money-Robo: 연속 도형을 임의 해상도로 래스터 ----------
K=(28,30,38,255); W=(244,246,250,255); W2=(205,212,224,255); W3=(160,170,188,255)
SCR=(18,22,30,255); Y=(255,214,64,255); Y2=(214,160,30,255); R=(232,72,64,255); G=(76,214,120,255)
B=(70,140,240,255); SH=(0,0,0,70); SW=(120,190,255,255); SP=(255,240,150,255)
LIGHT={"idle":B,"thinking":Y,"wrong":R,"confused":Y,"success":G}
def _seg(px,py,ax,ay,bx,by):
    vx,vy=bx-ax,by-ay; t=max(0,min(1,((px-ax)*vx+(py-ay)*vy)/(vx*vx+vy*vy))); return math.hypot(px-ax-t*vx,py-ay-t*vy)
def robo(state, k):
    """단위: 원래 36칸 격자. k = 한 칸에 몇 픽셀"""
    N=int(round(36*k)); img=Image.new("RGBA",(N,N),(0,0,0,0)); P=img.load()
    hx,hy,hr=16.5,14.5,10.3
    for Yp in range(N):
        for Xp in range(N):
            x,y=(Xp+.5)/k,(Yp+.5)/k; c=None
            if ((x-16.5)/7.5)**2+((y-33.4)/1.3)**2<=1: c=SH
            # 팔
            arms=[(9.6,26,7.4,28.2),(23.4,26,25.6,28.2)] if state!="success" else [(9.6,26,7.2,23.6),(23.4,26,25.8,23.6)]
            for a in arms:
                if _seg(x,y,*a)<=1.0: c=W2
            if ((x-16.5)/7.0)**2+((y-27.0)/4.6)**2<=1: c=W if y<27.5 else W2
            d=math.hypot(x-hx,y-hy)
            if d<=hr: c=W if (x-hx)+(y-hy)<6 else W2
            if hr-1.0<d<=hr and (x-hx)+(y-hy)>4: c=W3
            if abs(x-17)<=0.45 and 2.2<=y<=4.6: c=W3
            if math.hypot(x-17,y-1.6)<=1.25: c=Y if (x-17)+(y-1.6)<0.6 else Y2
            # 화면(둥근 사각)
            if 9<=x<=25 and 10<=y<=20 and not ((x<9.8 or x>24.2) and (y<10.8 or y>19.2)): c=SCR
            # 가슴 표시등
            if math.hypot(x-17,y-26.6)<=1.9: c=LIGHT[state]
            if math.hypot(x-16.4,y-26.0)<=0.5: c=(255,255,255,255)
            # 화면 기호 (선 굵기 일정)
            sym=None
            if state=="idle":
                if (11.8<=x<=13.8 or 19.8<=x<=21.8) and 12.6<=y<=15.6: sym=Y
                if abs(math.hypot(x-17,y-15.4)-2.0)<=0.5 and y>15.6: sym=Y
            elif state=="thinking":
                for cx in (12.5,17,21.5):
                    if abs(x-cx)<=1.0 and abs(y-15)<=1.0: sym=Y
                if 14.6<=x<=19.4 and 11.4<=y<=12.2: sym=Y2
            elif state=="wrong":
                if _seg(x,y,13.6,11.8,20.4,18.6)<=0.85 or _seg(x,y,20.4,11.8,13.6,18.6)<=0.85: sym=R
            elif state=="confused":
                ang=math.atan2(y-15,x-17); rr=math.hypot(x-17,y-15); t=(ang+math.pi)/(2*math.pi)
                if abs(rr-(1.0+2.4*t))<=0.45 and rr<=3.6: sym=Y
                if math.hypot(x-27.2,y-9.4)<=1.0 or (abs(x-27.2)<=0.5 and 7.4<=y<=9): c=SW
            elif state=="success":
                if _seg(x,y,12.2,15.2,15,18)<=0.8 or _seg(x,y,15,18,21.4,11.6)<=0.8: sym=G
                for sx,sy in [(4,5),(30,4),(5,18),(29,19)]:
                    if (abs(x-sx)<=0.35 and abs(y-sy)<=1.4) or (abs(y-sy)<=0.35 and abs(x-sx)<=1.4): c=SP
            if sym and 9<=x<=25 and 10<=y<=20: c=sym
            if c: P[Xp,Yp]=c
    # 바깥 테두리 1픽셀
    out=img.copy(); O=out.load()
    for Yp in range(N):
        for Xp in range(N):
            if P[Xp,Yp][3]==0:
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    xx,yy=Xp+dx,Yp+dy
                    if 0<=xx<N and 0<=yy<N and P[xx,yy][3]==255 and P[xx,yy] not in (SP,SW): O[Xp,Yp]=K; break
    return out
ROBO_HEAD=(16.5,14.5,20.6)  # 머리 중심과 지름(칸)

# ---------- 초상 ----------
GRID=64; HEAD_FRAC=0.60; TOP=0.42
def portrait_src(im,cx,cy,h):
    S=h/HEAD_FRAC; x0,y0=cx-S/2,cy-S*TOP
    canvas=Image.new("RGBA",(int(round(S)),)*2,(0,0,0,0))
    canvas.alpha_composite(im.crop((int(round(x0)),int(round(y0)),int(round(x0+S)),int(round(y0+S)))),(0,0))
    return downsample(canvas,GRID,GRID).resize((GRID*8,GRID*8),Image.NEAREST)
def portrait_robo(state):
    head_px=GRID*HEAD_FRAC; k=head_px/ROBO_HEAD[2]
    r=robo(state,k); S=GRID; cx,cy=ROBO_HEAD[0]*k,ROBO_HEAD[1]*k
    canvas=Image.new("RGBA",(S,S),(0,0,0,0)); canvas.alpha_composite(r,(int(round(S/2-cx)),int(round(S*TOP-cy))))
    return canvas.resize((S*8,S*8),Image.NEAREST)

# ---------- 대표 그림용 스프라이트 (배경과 같은 격자) ----------
def scene_sprite(name, head_px, flip=False, state="idle"):
    if name=="robo":
        r=robo(state, head_px/ROBO_HEAD[2]); r=r.crop(r.getbbox())
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
