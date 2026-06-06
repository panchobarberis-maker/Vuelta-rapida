from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1350
NAVY   = (26, 46, 74)
GOLD   = (194, 128, 26)
CREAM  = (245, 239, 230)
WHITE  = (255, 255, 255)
DARK   = (10, 18, 30)
GRAY   = (120, 120, 120)
BROWN  = (90, 74, 58)

IMG_DIR = "/home/user/Vuelta-rapida/mjtrust law/"
OUT_DIR = "/home/user/Vuelta-rapida/carousel-html/previews/"
os.makedirs(OUT_DIR, exist_ok=True)

SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS      = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SERIF_B   = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I   = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
SERIF     = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def load_img(filename):
    return Image.open(IMG_DIR + filename).convert("RGBA")

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, line = [], ""
    for w in words:
        test = (line + " " + w).strip()
        if draw.textbbox((0,0), test, font=fnt)[2] <= max_w:
            line = test
        else:
            if line: lines.append(line)
            line = w
    if line: lines.append(line)
    return lines

def draw_text_block(draw, lines_data, x, y, gap=8):
    """lines_data = list of (text, font, color, align='left')"""
    for text, fnt, col, *args in lines_data:
        align = args[0] if args else 'left'
        bbox = draw.textbbox((0,0), text, font=fnt)
        tw = bbox[2] - bbox[0]
        tx = (W - tw) // 2 if align == 'center' else x
        draw.text((tx, y), text, fill=col, font=fnt)
        y += (bbox[3] - bbox[1]) + gap
    return y

def hdr_bar(img):
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0,0),(W,86)], fill=NAVY)
    f = font(SANS_BOLD, 28)
    text = "MJ  /  TRUST LAW"
    bbox = draw.textbbox((0,0), text, font=f)
    tx = (W - (bbox[2]-bbox[0])) // 2
    draw.text((tx, 28), text, fill=WHITE, font=f)

def ftr_bar(img, pg, light=True):
    draw = ImageDraw.Draw(img)
    col = (138,122,106) if light else (255,255,255,100)
    col_line = (*GOLD, 90)
    draw.rectangle([(0, H-68),(W, H)], fill=(0,0,0,0))
    draw.line([(0, H-68),(W, H-68)], fill=col_line if light else (255,255,255,40), width=1)
    f = font(SANS, 22)
    draw.text((56, H-44), "2026", fill=col, font=f)
    label = "MJTRUST LAW.COM"
    bbox = draw.textbbox((0,0), label, font=f)
    draw.text(((W-(bbox[2]-bbox[0]))//2, H-44), label, fill=col, font=f)
    draw.text((W-120, H-44), f"PG{pg:02d}", fill=col, font=f)

def rule(draw, x, y, w, col=GOLD, h=2):
    draw.rectangle([(x, y),(x+w, y+h)], fill=col)

def page_indicator(img, current, total=6, dark=False):
    draw = ImageDraw.Draw(img)
    bar_w, bar_h, gap = 44, 3, 10
    total_w = total * bar_w + (total - 1) * gap
    x0 = (W - total_w) // 2
    y_bars = H - 102
    for i in range(total):
        x = x0 + i * (bar_w + gap)
        col = GOLD if i == current - 1 else ((255,255,255) if dark else (26,46,74,46))
        if i != current - 1 and not dark:
            col = (180, 165, 140)
        draw.rounded_rectangle([(x, y_bars),(x+bar_w, y_bars+bar_h)], radius=2, fill=col)
    f_num = font(SANS, 18)
    num_text = f"{current:02d} / {total:02d}"
    bbox = draw.textbbox((0,0), num_text, font=f_num)
    num_col = (200,190,175) if dark else (176,152,120)
    draw.text(((W-(bbox[2]-bbox[0]))//2, H-86), num_text, fill=num_col, font=f_num)

def dotgrid(draw, x, y, w, h, col=(194,128,26,80)):
    for gx in range(x, x+w, 24):
        for gy in range(y, y+h, 24):
            draw.ellipse([(gx-1,gy-1),(gx+1,gy+1)], fill=col[:3])

# ── SLIDE 1 ───────────────────────────────────────────────────────────────────
def slide1():
    img = Image.new("RGBA", (W, H), CREAM)

    # Photo right 72%, cover crop at 35%
    try:
        photo = load_img("10.webp")
        pw = int(W * 0.72)
        ow, oh = photo.size
        scale = max(pw/ow, H/oh)
        nw, nh = int(ow*scale), int(oh*scale)
        photo = photo.resize((nw, nh), Image.LANCZOS)
        cx = int((nw - pw) * 0.35)
        region = photo.crop((cx, 0, cx+pw, H))
        img.paste(region, (W-pw, 0), region)
    except Exception as e:
        print(f"Photo error: {e}")

    # Cream gradient overlay
    panel_w = int(W * 0.72)
    blend_start = int(panel_w * 0.36)
    blend_end   = int(panel_w * 0.78)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    for x in range(blend_end):
        a = 255 if x <= blend_start else int(255 * (1 - (x-blend_start)/(blend_end-blend_start)))
        for y in range(H):
            overlay.putpixel((x, y), CREAM+(a,))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # Logo
    try:
        logo = Image.open(IMG_DIR+"logo.jpg").convert("RGBA")
        lw = 210; lh = int(logo.size[1]*(lw/logo.size[0]))
        logo = logo.resize((lw,lh), Image.LANCZOS)
        img.paste(logo, (80,72))
    except:
        draw.text((80,80), "MJ TRUST LAW", fill=NAVY, font=font(SANS_BOLD,28))

    # Content
    y = 290
    f_tag = font(SANS_BOLD, 22)
    draw.text((80, y), "ESTATE PLANNING", fill=GOLD, font=f_tag); y += 36
    rule(draw, 80, y, 64); y += 28

    f_italic = font(SERIF_I, 40)
    draw.text((80, y), "Most people think:", fill=GRAY, font=f_italic); y += 56

    f_h = font(SERIF_B, 80)
    draw.text((80, y), '"No big', fill=NAVY, font=f_h); y += 90
    draw.text((80, y), 'deal."', fill=NAVY, font=f_h); y += 100

    rule(draw, 80, y, 64); y += 28
    f_body = font(SANS_BOLD, 26)
    for line in wrap(draw, "In California, that 'small' mistake can break your entire estate plan.", f_body, 480):
        draw.text((80, y), line, fill=NAVY, font=f_body); y += 38
    y += 16
    f_cta = font(SERIF_I, 26)
    draw.text((80, y), "Swipe to see how  →", fill=GOLD, font=f_cta)

    img = img.convert("RGB")
    page_indicator(img, 1, dark=False)
    img.save(OUT_DIR+"slide1.jpg", quality=90)
    print("Slide 1 saved")

# ── SLIDE 2 ───────────────────────────────────────────────────────────────────
def slide2():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    hdr_bar(img); draw = ImageDraw.Draw(img)
    dotgrid(draw, W-240, H-300, 200, 200)
    draw.ellipse([(W-380,-260),(W+260,380)], outline=(*GOLD,40), width=2)

    # watermark number
    draw.text((W-300, 110), "2", fill=(26,46,74,18), font=font(SERIF_B,240))

    y = 140
    f_tag = font(SANS_BOLD, 22); draw.text((72, y), "THE SCENARIO", fill=GOLD, font=f_tag); y += 38
    f_h = font(SERIF_B, 80)
    draw.text((72, y), "Let's say", fill=NAVY, font=f_h); y += 90
    draw.text((72, y), "you have", fill=NAVY, font=f_h); y += 90
    f_hi = font(SERIF_I, 80)
    draw.text((72, y), "a Trust.", fill=GOLD, font=f_hi); y += 100
    rule(draw, 72, y, W-144); y += 32

    f_check = font(SANS_BOLD, 28)
    f_item  = font(SERIF, 30)
    for item in ["Your home is in it.", "Your beneficiaries are named.", "Everything looks perfect."]:
        draw.text((72, y), "✓", fill=GOLD, font=f_check)
        draw.text((120, y+2), item, fill=NAVY, font=f_item)
        y += 50

    rule(draw, 72, y, W-144); y += 32
    f_end = font(SERIF_I, 52)
    draw.text((72, y), "One thing", fill=NAVY, font=f_end); y += 64
    draw.text((72, y), "gets missed…", fill=NAVY, font=f_end)

    page_indicator(img, 2, dark=False)
    ftr_bar(img, 2)
    img.save(OUT_DIR+"slide2.jpg", quality=90)
    print("Slide 2 saved")

# ── SLIDE 3 ───────────────────────────────────────────────────────────────────
def slide3():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    hdr_bar(img); draw = ImageDraw.Draw(img)
    # big circle
    r = 390; cx_c, cy_c = W//2, H//2+50
    draw.ellipse([(cx_c-r,cy_c-r),(cx_c+r,cy_c+r)], outline=(*GOLD,40), width=2)
    dotgrid(draw, W-230, 100, 190, 190)

    y = 140
    f_tag = font(SANS_BOLD, 22)
    tw = draw.textbbox((0,0),"THE OVERLOOKED ASSET",font=f_tag)[2]
    draw.text(((W-tw)//2, y), "THE OVERLOOKED ASSET", fill=GOLD, font=f_tag); y += 40

    # giant $500
    f_dollar = font(SERIF_B, 54)
    f_num    = font(SERIF_B, 200)
    bbox_d = draw.textbbox((0,0),"$",font=f_dollar)
    bbox_n = draw.textbbox((0,0),"500",font=f_num)
    total_w = (bbox_d[2]-bbox_d[0]) + (bbox_n[2]-bbox_n[0])
    sx = (W - total_w) // 2
    draw.text((sx, y+30), "$", fill=NAVY, font=f_dollar)
    draw.text((sx + bbox_d[2]-bbox_d[0], y-10), "500", fill=NAVY, font=f_num)
    y += 220

    rule(draw, (W-520)//2, y, 520); y += 28

    f_italic = font(SERIF_I, 36)
    tw2 = draw.textbbox((0,0),"Still in your individual name.",font=f_italic)[2]
    draw.text(((W-tw2)//2, y), "Still in your individual name.", fill=NAVY, font=f_italic); y += 52

    f_body = font(SANS, 26)
    for line in wrap(draw, "Under California's small estate rules, on its own — no probate needed.", f_body, 760):
        tw3 = draw.textbbox((0,0),line,font=f_body)[2]
        draw.text(((W-tw3)//2, y), line, fill=BROWN, font=f_body); y += 40
    y += 16

    rule(draw, (W-520)//2, y, 520); y += 28

    f_risky = font(SANS_BOLD, 30)
    tw4 = draw.textbbox((0,0),"But here's where it gets risky…",font=f_risky)[2]
    draw.text(((W-tw4)//2, y), "But here's where it gets risky…", fill=GOLD, font=f_risky); y += 48

    for line in wrap(draw, "One forgotten account is all it takes to expose your entire estate to probate court.", f_body, 760):
        tw5 = draw.textbbox((0,0),line,font=f_body)[2]
        draw.text(((W-tw5)//2, y), line, fill=BROWN, font=f_body); y += 38

    page_indicator(img, 3, dark=False)
    ftr_bar(img, 3)
    img.save(OUT_DIR+"slide3.jpg", quality=90)
    print("Slide 3 saved")

# ── SLIDE 4 ───────────────────────────────────────────────────────────────────
def slide4():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    hdr_bar(img); draw = ImageDraw.Draw(img)
    dotgrid(draw, 30, 220, 160, 400)
    draw.ellipse([(-80,-80),(420,420)], outline=(*GOLD,35), width=2)

    y = 130
    f_tag = font(SANS_BOLD, 22)
    draw.text((72, y), "THE BIGGER PICTURE", fill=GOLD, font=f_tag); y += 40
    f_h = font(SANS_BOLD, 52)
    for line in wrap(draw, "That one account is often a sign of a bigger issue.", f_h, W-144):
        draw.text((72, y), line, fill=NAVY, font=f_h); y += 62
    y += 4

    rule(draw, 72, y, W-144); y += 30
    f_it = font(SERIF_I, 28)
    draw.text((72, y), "Something else may have been missed too.", fill=BROWN, font=f_it); y += 46

    f_item = font(SERIF, 30)
    for item in ["An old retirement account.", "A second property.", "An investment account you forgot to transfer."]:
        draw.text((72, y), "◆", fill=GOLD, font=font(SANS_BOLD,24))
        draw.text((118, y), item, fill=NAVY, font=f_item); y += 50
    y += 8

    rule(draw, 72, y, W-144); y += 30
    f_reveal1 = font(SANS_BOLD, 38)
    tw = draw.textbbox((0,0),"The $500 isn't the problem.",font=f_reveal1)[2]
    draw.text(((W-tw)//2, y), "The $500 isn't the problem.", fill=NAVY, font=f_reveal1); y += 52
    f_reveal2 = font(SANS_BOLD, 38)
    tw2 = draw.textbbox((0,0),"What it REVEALS is.",font=f_reveal2)[2]
    draw.text(((W-tw2)//2, y), "What it REVEALS is.", fill=GOLD, font=f_reveal2); y += 52
    f_pattern = font(SERIF_I, 26)
    tw3 = draw.textbbox((0,0),"It's a pattern. And patterns need fixing.",font=f_pattern)[2]
    draw.text(((W-tw3)//2, y), "It's a pattern. And patterns need fixing.", fill=BROWN, font=f_pattern)

    page_indicator(img, 4, dark=False)
    ftr_bar(img, 4)
    img.save(OUT_DIR+"slide4.jpg", quality=90)
    print("Slide 4 saved")

# ── SLIDE 5 ───────────────────────────────────────────────────────────────────
def slide5():
    # Cream with inner frame — same visual design as before, California Law content
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # inner frame border
    pad = 52
    draw.rectangle([(pad,pad),(W-pad,H-pad)], outline=(*GOLD,64), width=2)
    # big decorative quote mark
    draw.text((86, 40), '"', fill=(194,128,26,28), font=font(SERIF_B,220))
    # dot grid bottom-right
    dotgrid(draw, W-250, H-280, 165, 165)

    # logo
    try:
        logo = Image.open(IMG_DIR+"logo.jpg").convert("RGBA")
        lw = 210; lh = int(logo.size[1]*(lw/logo.size[0]))
        logo = logo.resize((lw,lh), Image.LANCZOS)
        img.paste(logo, (80,72))
    except:
        draw.text((80,80), "MJ TRUST LAW", fill=NAVY, font=font(SANS_BOLD,28))

    draw = ImageDraw.Draw(img)
    y = 210
    f_tag = font(SANS_BOLD, 22)
    draw.text((96, y), "CALIFORNIA LAW", fill=GOLD, font=f_tag); y += 38
    rule(draw, 96, y, 64); y += 32

    f_h = font(SERIF_B, 56)
    for line in wrap(draw, "Probate fees are based on the gross value of the estate.", f_h, W-192):
        draw.text((96, y), line, fill=NAVY, font=f_h); y += 68
    y += 4
    rule(draw, 96, y, 64); y += 28

    f_it = font(SERIF_I, 30)
    draw.text((96, y), "Not the size of the mistake.", fill=(107,88,64), font=f_it); y += 44
    draw.text((96, y), "Not just the $500 account.", fill=(107,88,64), font=f_it); y += 50
    rule(draw, 96, y, 64); y += 28

    f_bold = font(SANS_BOLD, 24)
    for line in wrap(draw, "If ANY significant asset sits outside your trust — real estate, accounts, property — probate is on the table.", f_bold, W-192):
        draw.text((96, y), line, fill=GOLD, font=f_bold); y += 36
    y += 8
    f_body = font(SANS, 22)
    for line in wrap(draw, "Probate in California means months of court process, public records, and fees that can reach 4–6% of your gross estate.", f_body, W-192):
        draw.text((96, y), line, fill=(90,74,58), font=f_body); y += 34

    page_indicator(img, 5, dark=False)
    img.save(OUT_DIR+"slide5.jpg", quality=90)
    print("Slide 5 saved")

# ── SLIDE 6 ───────────────────────────────────────────────────────────────────
def slide6():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    hdr_bar(img); draw = ImageDraw.Draw(img)
    r = 400; cx_c, cy_c = W//2, H//2+60
    draw.ellipse([(cx_c-r,cy_c-r),(cx_c+r,cy_c+r)], outline=(*GOLD,40), width=2)
    dotgrid(draw, W-230, H-300, 190, 200)

    y = 130
    f_h = font(SANS_BOLD, 54)
    tw1 = draw.textbbox((0,0),"THE REAL PROBLEM",font=f_h)[2]
    draw.text(((W-tw1)//2, y), "THE REAL PROBLEM", fill=NAVY, font=f_h); y += 64
    tw2 = draw.textbbox((0,0),"ISN'T THE $500.",font=f_h)[2]
    draw.text(((W-tw2)//2, y), "ISN'T THE $500.", fill=NAVY, font=f_h); y += 72

    rule(draw, (W-520)//2, y, 520); y += 30

    f_it = font(SERIF_I, 30)
    tw3 = draw.textbbox((0,0),"It's what it reveals:",font=f_it)[2]
    draw.text(((W-tw3)//2, y), "It's what it reveals:", fill=BROWN, font=f_it); y += 52

    f_item = font(SERIF, 30)
    for item in ["An incomplete plan.", "Unfunded assets.", "A system that fails your family when it matters most."]:
        draw.text((W//2-340, y), "◆", fill=GOLD, font=font(SANS_BOLD,24))
        for line in wrap(draw, item, f_item, 580):
            draw.text((W//2-290, y), line, fill=NAVY, font=f_item); y += 44

    y += 8; rule(draw, (W-520)//2, y, 520); y += 28

    f_bold_it = font(SERIF_I, 28)
    for line in ["It's not the big things that break a plan.", "It's the small ones that get overlooked."]:
        tw = draw.textbbox((0,0),line,font=f_bold_it)[2]
        draw.text(((W-tw)//2, y), line, fill=NAVY, font=f_bold_it); y += 44
    y += 24

    # CTA button
    btn_w, btn_h = 680, 80; bx = (W-btn_w)//2
    draw.rectangle([(bx, y),(bx+btn_w, y+btn_h)], fill=NAVY)
    f_btn = font(SANS_BOLD, 26)
    btn_text = "Book a Free Consultation"
    bbox = draw.textbbox((0,0),btn_text,font=f_btn)
    tx = bx + (btn_w-(bbox[2]-bbox[0]))//2; ty = y + (btn_h-(bbox[3]-bbox[1]))//2
    draw.text((tx,ty), btn_text, fill=WHITE, font=f_btn); y += btn_h + 22

    f_url = font(SANS_BOLD, 24)
    tw_url = draw.textbbox((0,0),"mjtrust law.com",font=f_url)[2]
    draw.text(((W-tw_url)//2, y), "mjtrust law.com", fill=GOLD, font=f_url)

    page_indicator(img, 6, dark=False)
    ftr_bar(img, 6)
    img.save(OUT_DIR+"slide6.jpg", quality=90)
    print("Slide 6 saved")


slide1()
slide2()
slide3()
slide4()
slide5()
slide6()
print("All slides rendered.")
