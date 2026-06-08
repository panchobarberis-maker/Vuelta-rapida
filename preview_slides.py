from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1350
NAVY  = (26, 46, 74)
GOLD  = (194, 128, 26)
CREAM = (245, 239, 230)
WHITE = (255, 255, 255)
DARK  = (10, 18, 30)
BROWN = (107, 88, 64)

IMG_DIR = "/home/user/Vuelta-rapida/mjtrust law/"
OUT_DIR = "/home/user/Vuelta-rapida/carousel-html/previews/"
os.makedirs(OUT_DIR, exist_ok=True)

SB  = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SR  = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
PB  = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
PI  = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
PR  = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

def fnt(path, size):
    try: return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

def tw(draw, text, f):
    b = draw.textbbox((0,0), text, font=f); return b[2]-b[0]

def cx_text(draw, text, f, y, col):
    x = (W - tw(draw,text,f))//2
    draw.text((x,y), text, fill=col, font=f)

def wrap(draw, text, f, maxw):
    words = text.split(); lines, line = [], ""
    for w in words:
        t = (line+" "+w).strip()
        if tw(draw,t,f) <= maxw: line = t
        else:
            if line: lines.append(line)
            line = w
    if line: lines.append(line)
    return lines

def load_cover(pw, ph, cx_pct=0.5):
    """Load and cover-crop a photo to pw x ph."""
    from PIL import Image as Img
    pass

def gold_stripe(img):
    ImageDraw.Draw(img).rectangle([(0,0),(W,6)], fill=GOLD)

def counter(img, num, dark=False):
    draw = ImageDraw.Draw(img)
    col = (255,255,255,90) if dark else (26,46,74,90)
    col = (200,190,175) if dark else (160,145,125)
    f = fnt(SB, 18)
    text = f"{num:02d} / 06"
    x = W - 60 - tw(draw,text,f)
    draw.text((x, H-62), text, fill=col, font=f)
    draw.rectangle([(x-50, H-52),(x-18, H-51)], fill=col)

def logo(img, light=False):
    try:
        logo_img = Image.open(IMG_DIR+"logo.jpg").convert("RGBA")
        lw = 200; lh = int(logo_img.size[1]*(lw/logo_img.size[0]))
        logo_img = logo_img.resize((lw,lh), Image.LANCZOS)
        if light:
            bg = Image.new("RGBA", (lw+32, lh+20), (255,255,255,235))
            bg.paste(logo_img, (16,10), logo_img)
            img.paste(bg, (56, 44), bg)
        else:
            img.paste(logo_img, (56, 44), logo_img)
    except:
        draw = ImageDraw.Draw(img)
        draw.text((56,44), "MJ TRUST LAW", fill=WHITE if light else NAVY, font=fnt(SB,26))

def cover_crop(path, target_w, target_h, cx_bias=0.5, cy_bias=0.0):
    photo = Image.open(path).convert("RGBA")
    ow, oh = photo.size
    scale = max(target_w/ow, target_h/oh)
    nw, nh = int(ow*scale), int(oh*scale)
    photo = photo.resize((nw,nh), Image.LANCZOS)
    cx = int((nw-target_w)*cx_bias)
    cy = int((nh-target_h)*cy_bias)
    return photo.crop((cx,cy,cx+target_w,cy+target_h))


# ── S1: Full-bleed photo, dark vignette, text bottom-left ─────────────────────
def slide1():
    photo = cover_crop(IMG_DIR+"10.webp", W, H, cx_bias=0.5, cy_bias=0.0)
    img = photo.copy()

    # dark gradient left
    grad = Image.new("RGBA",(W,H),(0,0,0,0))
    for x in range(W):
        t = max(0, 1 - x/(W*0.65))
        a = int(215 * t)
        for y in range(H): grad.putpixel((x,y),(10,18,30,a))
    img = Image.alpha_composite(img, grad)

    # dark gradient bottom
    grad2 = Image.new("RGBA",(W,H),(0,0,0,0))
    for y in range(H):
        if y > H*0.5:
            t = (y-H*0.5)/(H*0.5)
            a = int(180*t)
            for x in range(W): grad2.putpixel((x,y),(10,18,30,a))
    img = Image.alpha_composite(img, grad2)
    img = img.convert("RGB")

    gold_stripe(img)
    logo(img, light=True)

    draw = ImageDraw.Draw(img)
    y = H - 420
    f_tag = fnt(SB,22); draw.text((64,y),"ESTATE PLANNING · CHULA VISTA",fill=GOLD,font=f_tag); y+=46
    f_h1 = fnt(PI,100); draw.text((64,y),'"No big',fill=WHITE,font=f_h1); y+=108
    f_h2 = fnt(PB,100); draw.text((64,y),'deal."',fill=WHITE,font=f_h2); y+=112
    draw.rectangle([(64,y),(120,y+2)],fill=GOLD); y+=22
    f_body = fnt(SR,26)
    for line in wrap(draw,"In California, that 'small' mistake can break your entire estate plan.",f_body,580):
        draw.text((64,y),line,fill=(220,210,195),font=f_body); y+=38
    y+=16
    f_cta = fnt(SB,20); draw.text((64,y),"SWIPE TO SEE HOW  →",fill=GOLD,font=f_cta)

    counter(img,1,dark=True)
    img.save(OUT_DIR+"slide1.jpg",quality=92)
    print("S1 saved")


# ── S2: Cream, left accent bar, checklist ────────────────────────────────────
def slide2():
    img = Image.new("RGB",(W,H),CREAM)
    draw = ImageDraw.Draw(img)

    # left bar
    draw.rectangle([(0,0),(6,H)],fill=GOLD)
    # watermark number
    draw.text((W-340,-60),"2",fill=(194,128,26,12),font=fnt(PB,480))

    gold_stripe(img); draw = ImageDraw.Draw(img)
    logo(img)

    y = 180
    f_tag = fnt(SB,22); draw.text((86,y),"LET'S SAY YOU HAVE A TRUST",fill=GOLD,font=f_tag); y+=56

    # checklist with left bar
    items = ["Your home is in it.","Your beneficiaries are named.","Everything looks perfect."]
    f_item = fnt(PB,40)
    for item in items:
        draw.rectangle([(86,y),(90,y+50)],fill=GOLD)
        for line in wrap(draw,item,f_item,W-160):
            draw.text((118,y),line,fill=NAVY,font=f_item); y+=52
        y+=10
    y+=16

    draw.rectangle([(86,y),(W-86,y+1)],fill=(*GOLD,100)); y+=44
    f_close = fnt(PI,68); draw.text((86,y),"One thing",fill=NAVY,font=f_close); y+=76
    draw.text((86,y),"gets missed…",fill=NAVY,font=f_close)

    counter(img,2)
    img.save(OUT_DIR+"slide2.jpg",quality=92)
    print("S2 saved")


# ── S3: Family photo, dark overlay, massive $500 centered ────────────────────
def slide3():
    photo = cover_crop(IMG_DIR+"depositphotos_2348091-stock-photo-hispanic-family-portrait-in-the.jpg",W,H,0.5,0.3)
    img = photo.copy()
    overlay = Image.new("RGBA",(W,H),(10,18,30,184))
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB")

    gold_stripe(img)
    logo(img, light=True)
    draw = ImageDraw.Draw(img)

    # centered content
    f_tag = fnt(SB,22)
    cx_text(draw,"THE OVERLOOKED ASSET",f_tag,230,GOLD)

    # $500 massive
    f_big = fnt(PB,240)
    text = "$500"
    x = (W-tw(draw,text,f_big))//2
    draw.text((x,310),text,fill=WHITE,font=f_big)

    draw.rectangle([(W//2-48,570),(W//2+48,572)],fill=GOLD)

    f_it = fnt(PI,38)
    cx_text(draw,"Still in your individual name.",f_it,590,WHITE)

    f_body = fnt(SR,24)
    body = "Under California's small estate rules, on its own — no probate needed. But here's where it gets risky…"
    y=652
    for line in wrap(draw,body,f_body,820):
        cx_text(draw,line,f_body,y,(210,200,185)); y+=38

    f_risky = fnt(SB,30)
    y+=20; cx_text(draw,"One forgotten account exposes your entire estate to probate.",f_risky,y,GOLD)

    counter(img,3,dark=True)
    img.save(OUT_DIR+"slide3.jpg",quality=92)
    print("S3 saved")


# ── S4: Cream, right bar, grid list, dark CTA box ────────────────────────────
def slide4():
    img = Image.new("RGB",(W,H),CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([(W-6,0),(W,H)],fill=GOLD)
    draw.text((W-560,60),"RISK",fill=(26,46,74,10),font=fnt(SB,200))

    gold_stripe(img); draw=ImageDraw.Draw(img)
    logo(img)

    y = 180
    f_tag = fnt(SB,22); draw.text((72,y),"THE BIGGER PICTURE",fill=GOLD,font=f_tag); y+=48
    f_h = fnt(PB,56)
    for line in wrap(draw,"That one account is often a sign of a bigger issue.",f_h,W-144):
        draw.text((72,y),line,fill=NAVY,font=f_h); y+=64
    y+=8
    draw.rectangle([(72,y),(W-72,y+1)],fill=(*GOLD,90)); y+=36
    f_it = fnt(PI,28); draw.text((72,y),"Something else may have been missed too.",fill=BROWN,font=f_it); y+=48

    # 2-col grid
    items = ["An old retirement account","A second property","An investment account you forgot to transfer","A joint account not retitled"]
    f_gi = fnt(SB,22); cols=[72,W//2+20]; row_h=72
    for i,item in enumerate(items):
        cx = cols[i%2]; cy = y + (i//2)*row_h
        draw.rectangle([(cx,cy+4),(cx+3,cy+40)],fill=GOLD)
        for line in wrap(draw,item,f_gi,400):
            draw.text((cx+18,cy),line,fill=NAVY,font=f_gi); cy+=28
    y += 2*(row_h)+24

    # dark box
    draw.rectangle([(72,y),(W-72,y+120)],fill=NAVY)
    f_box = fnt(SB,28); draw.text((96,y+18),"The $500 isn't the problem.",fill=WHITE,font=f_box)
    draw.text((96,y+56),"What it REVEALS is.",fill=GOLD,font=f_box)

    counter(img,4)
    img.save(OUT_DIR+"slide4.jpg",quality=92)
    print("S4 saved")


# ── S5: Dark navy, bold law statement ────────────────────────────────────────
def slide5():
    img = Image.new("RGB",(W,H),NAVY)
    draw = ImageDraw.Draw(img)

    # subtle horizontal lines
    for y in range(0,H,60):
        draw.rectangle([(0,y),(W,y+1)],fill=(255,255,255,7))

    gold_stripe(img); draw=ImageDraw.Draw(img)
    logo(img, light=True)

    y=180
    f_tag = fnt(SB,22); draw.text((72,y),"CALIFORNIA LAW",fill=GOLD,font=f_tag); y+=48
    f_h = fnt(PB,68)
    for line in wrap(draw,"Probate fees are based on the gross value of the estate.",f_h,W-144):
        draw.text((72,y),line,fill=WHITE,font=f_h); y+=76
    y+=8
    draw.rectangle([(72,y),(144,y+3)],fill=GOLD); y+=28
    f_it = fnt(PI,32)
    draw.text((72,y),"Not the size of the mistake.",fill=(255,255,255,165),font=f_it); y+=46
    draw.text((72,y),"Not just the $500 account.",fill=(255,255,255,165),font=f_it); y+=60

    # bordered box
    draw.rectangle([(72,y),(W-72,y+140)],outline=(*GOLD,100),width=1)
    f_box = fnt(SB,25)
    yb=y+24
    for line in wrap(draw,"If ANY significant asset sits outside your trust — real estate, accounts, property — probate is on the table.",f_box,W-200):
        draw.text((96,yb),line,fill=GOLD,font=f_box); yb+=36
    y+=156

    f_body = fnt(SR,22)
    for line in wrap(draw,"Months of court process. Public records. Fees that can reach 4–6% of your gross estate.",f_body,W-144):
        draw.text((72,y),line,fill=(255,255,255,140),font=f_body); y+=34

    counter(img,5,dark=True)
    img.save(OUT_DIR+"slide5.jpg",quality=92)
    print("S5 saved")


# ── S6: Cream, navy top bar, centered CTA ────────────────────────────────────
def slide6():
    img = Image.new("RGB",(W,H),CREAM)
    draw = ImageDraw.Draw(img)

    # navy top bar
    draw.rectangle([(0,0),(W,120)],fill=NAVY)
    gold_stripe(img); draw=ImageDraw.Draw(img)

    # logo white inside navy bar
    try:
        logo_img = Image.open(IMG_DIR+"logo.jpg").convert("RGBA")
        lw=200; lh=int(logo_img.size[1]*(lw/logo_img.size[0]))
        logo_img=logo_img.resize((lw,lh),Image.LANCZOS)
        bg=Image.new("RGBA",(W,H),(0,0,0,0))
        bg.paste(logo_img,((W-lw)//2,38),logo_img)
        img=Image.alpha_composite(img.convert("RGBA"),bg).convert("RGB")
    except: pass

    draw=ImageDraw.Draw(img)

    y=180
    f_tag=fnt(SB,22); cx_text(draw,"THE REAL PROBLEM",f_tag,y,GOLD); y+=48
    f_h=fnt(PB,62)
    line1="It's not the big things"
    line2="that break a plan."
    line3="It's the small ones."
    for line,col in [(line1,NAVY),(line2,NAVY),(line3,GOLD)]:
        cx_text(draw,line,f_h,y,col); y+=72
    y+=8
    draw.rectangle([(W//2-44,y),(W//2+44,y+2)],fill=GOLD); y+=36

    # CTA button
    bx,bw,bh=72,W-144,86
    draw.rectangle([(bx,y),(bx+bw,y+bh)],fill=NAVY)
    f_btn=fnt(SB,24); btn="BOOK A FREE CONSULTATION"
    bx2=bx+(bw-tw(draw,btn,f_btn))//2
    draw.text((bx2,y+(bh-30)//2),btn,fill=WHITE,font=f_btn); y+=bh+28

    f_body=fnt(SR,22)
    body="No forms. No commitment. We review your trust, find the gaps, and tell you exactly what you need."
    for line in wrap(draw,body,f_body,W-160):
        cx_text(draw,line,f_body,y,(138,122,106)); y+=34
    y+=28
    f_url=fnt(SB,22); cx_text(draw,"mjtrust law.com",f_url,y,GOLD)

    counter(img,6)
    img.save(OUT_DIR+"slide6.jpg",quality=92)
    print("S6 saved")


slide1()
slide2()
slide3()
slide4()
slide5()
slide6()
print("Done.")
