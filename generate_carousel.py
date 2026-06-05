from PIL import Image, ImageDraw, ImageFont
import os, math

W, H  = 1080, 1350
NAVY  = (26, 46, 74)
CREAM = (240, 232, 218)
CREAM2= (228, 218, 200)
GOLD  = (190, 128, 38)
GOLD2 = (210, 155, 60)
WHITE = (255, 255, 255)
GRAY  = (148, 135, 115)
PAD   = 80

BOLD  = "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf"
REG   = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
ITAL  = "/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf"
BDIT  = "/usr/share/fonts/truetype/freefont/FreeSerifBoldItalic.ttf"
SANS  = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

def f(path, size): return ImageFont.truetype(path, size)

def wrap(text, font, draw, max_w):
    words = text.split()
    lines, line = [], ""
    for w in words:
        test = (line + " " + w).strip()
        if draw.textlength(test, font=font) <= max_w:
            line = test
        else:
            if line: lines.append(line)
            line = w
    if line: lines.append(line)
    return lines

def put(draw, lines, font, color, y, gap=1.25):
    for line in lines:
        lw = draw.textlength(line, font=font)
        draw.text(((W - lw) / 2, y), line, font=font, fill=color)
        y += int(font.size * gap)
    return y

def divider(draw, y, color=GOLD, width=1):
    draw.line([(PAD, y), (W - PAD, y)], fill=color, width=width)

def logo(draw, light=False):
    lf = f(SANSB, 30)
    label = "MJ   TRUST LAW"
    lw = draw.textlength(label, font=lf)
    x = (W - lw) / 2
    col = WHITE if light else GOLD
    draw.text((x, 52), label, font=lf, fill=col)
    draw.line([(x, 94), (x + lw, 94)], fill=col, width=2)

def footer(draw, page_num, light=False):
    y = H - 56
    lc = (180, 165, 145) if not light else (200, 200, 200)
    draw.line([(PAD, y - 18), (W - PAD, y - 18)], fill=lc, width=1)
    sf = f(SANS, 22)
    draw.text((PAD, y), "2026", font=sf, fill=lc)
    site = "MJTRUST LAW.COM"
    sw = draw.textlength(site, font=sf)
    draw.text(((W - sw) / 2, y), site, font=sf, fill=lc)
    pn = f"PG0{page_num}"
    pw = draw.textlength(pn, font=sf)
    draw.text((W - PAD - pw, y), pn, font=sf, fill=lc)

# ── DECORATIVE HELPERS ──────────────────────────────────────────────

def bg_dots(draw, color=(210, 200, 185), spacing=54, radius=2):
    """Subtle dot grid texture"""
    for x in range(0, W, spacing):
        for y in range(0, H, spacing):
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)

def bg_circles(draw, light=False):
    """Large decorative circles in corners"""
    c = (210, 198, 178) if not light else (60, 80, 110)
    # Bottom right big circle
    draw.ellipse([W - 420, H - 420, W + 200, H + 200], outline=c, width=3)
    draw.ellipse([W - 320, H - 320, W + 100, H + 100], outline=c, width=1)
    # Top left small circle
    draw.ellipse([-180, -180, 220, 220], outline=c, width=2)

def gold_corner_lines(draw):
    """Gold accent lines in top-right and bottom-left"""
    t = 3
    draw.line([(W - 120, 20), (W - 20, 20)], fill=GOLD, width=t)
    draw.line([(W - 20, 20), (W - 20, 120)], fill=GOLD, width=t)
    draw.line([(20, H - 120), (20, H - 20)], fill=GOLD, width=t)
    draw.line([(20, H - 20), (120, H - 20)], fill=GOLD, width=t)

def diamond_accent(draw, cx, cy, size=18, color=GOLD):
    """Small diamond shape"""
    pts = [(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)]
    draw.polygon(pts, fill=color)

def gold_band_top(draw):
    """Thin gold band under logo area"""
    draw.rectangle([0, 106, W, 115], fill=GOLD)

def scales_watermark(draw):
    """Abstract scales of justice — two circles connected by lines"""
    cx, cy, r = W - 140, H - 200, 55
    lc = (210, 198, 178)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=lc, width=2)
    draw.ellipse([cx - r - 140, cy - r, cx + r - 140, cy + r], outline=lc, width=2)
    draw.line([(cx - 140, cy), (cx, cy)], fill=lc, width=2)
    bx = cx - 70
    draw.line([(bx, cy), (bx, cy - 90)], fill=lc, width=2)
    draw.line([(bx - 80, cy - 90), (bx + 80, cy - 90)], fill=lc, width=2)

def navy_top_band(draw, h=130):
    draw.rectangle([0, 0, W, h], fill=NAVY)

def navy_bottom_band(draw, h=160):
    draw.rectangle([0, H - h, W, H], fill=NAVY)

def base_cream(): return Image.new("RGB", (W, H), CREAM)
def base_navy(): return Image.new("RGB", (W, H), NAVY)

OUT = "/home/user/Vuelta-rapida/carousel"
os.makedirs(OUT, exist_ok=True)

# ══ SLIDE 1 — Hook (Navy top band, cream body, decorative) ══════════
img = base_cream(); d = ImageDraw.Draw(img)
bg_dots(d)
bg_circles(d)
gold_corner_lines(d)
scales_watermark(d)
navy_top_band(d, 130)
logo(d, light=True)

y = 155
lf = f(SANS, 26); label = "ESTATE PLANNING MISTAKE"
lw = d.textlength(label, font=lf)
d.text(((W - lw) / 2, y), label, font=lf, fill=GOLD)
y += 40; divider(d, y, GOLD, 2); y += 28

q = f(BDIT, 68)
lines = wrap('Most people think:', q, d, W - PAD * 2)
y = put(d, lines, q, NAVY, y, 1.15)

q2 = f(ITAL, 72)
for line in ['"Worst case,', 'I forgot a small', 'account…', 'no big deal."']:
    lw2 = d.textlength(line, font=q2)
    d.text(((W - lw2) / 2, y), line, font=q2, fill=NAVY)
    y += 80

y += 8; divider(d, y, GOLD, 2); y += 28

bf = f(BOLD, 40)
sub = wrap("But in California, that tiny mistake can break your entire estate plan.", bf, d, W - PAD * 2)
y = put(d, sub, bf, GOLD, y, 1.35)

y += 16
af = f(BDIT, 32); arr = "Swipe to see how  →"
aw = d.textlength(arr, font=af)
d.text(((W - aw) / 2, y), arr, font=af, fill=GRAY)

footer(d, 1)
img.save(f"{OUT}/slide_01.png"); print("Slide 1 ✓")

# ══ SLIDE 2 — Setup ════════════════════════════════════════════════
img = base_cream(); d = ImageDraw.Draw(img)
bg_dots(d)
bg_circles(d)
gold_corner_lines(d)
navy_top_band(d, 130)
logo(d, light=True)
divider(d, 145, WHITE, 1)

y = 162
hf = f(BOLD, 64)
h = wrap("LET'S SAY YOU HAVE A TRUST.", hf, d, W - PAD * 2)
y = put(d, h, hf, NAVY, y, 1.15)

y += 12; divider(d, y, GOLD, 2); y += 40

items = ["Your home is in it.", "Your beneficiaries are named.", "Everything looks perfect."]
cf = f(REG, 46)
for item in items:
    gf = f(BOLD, 42)
    d.text((PAD + 8, y + 2), "✓", font=gf, fill=GOLD)
    d.text((PAD + 60, y), item, font=cf, fill=NAVY)
    y += 78

y += 12; divider(d, y, GOLD, 2); y += 40

mf = f(BDIT, 62)
miss = "One thing gets missed…"
mw = d.textlength(miss, font=mf)
d.text(((W - mw) / 2, y), miss, font=mf, fill=NAVY)

footer(d, 2)
img.save(f"{OUT}/slide_02.png"); print("Slide 2 ✓")

# ══ SLIDE 3 — The $500 ════════════════════════════════════════════
img = base_cream(); d = ImageDraw.Draw(img)
bg_dots(d)
bg_circles(d)
gold_corner_lines(d)
navy_top_band(d, 130)
logo(d, light=True)

lf3 = f(SANS, 26); label3 = "THE OVERLOOKED ASSET"
lw3 = d.textlength(label3, font=lf3)
d.text(((W - lw3) / 2, 148), label3, font=lf3, fill=GOLD)

# Big $500
bigf = f(BOLD, 148); big = "$500"
bw = d.textlength(big, font=bigf)
d.text(((W - bw) / 2, 185), big, font=bigf, fill=NAVY)

# Gold underline accent
d.rectangle([(W//2 - 120, 358), (W//2 + 120, 365)], fill=GOLD)

sf3 = f(BDIT, 40)
sub3 = "Still in your individual name."
sw3 = d.textlength(sub3, font=sf3)
d.text(((W - sw3) / 2, 378), sub3, font=sf3, fill=GOLD)

y = 435; divider(d, y, GOLD, 2); y += 36

bf3 = f(REG, 42)
body3 = ["Under California's small estate rules,", "on its own — no probate needed."]
y = put(d, body3, bf3, NAVY, y, 1.3)

y += 20; divider(d, y, GOLD, 2); y += 36

wf3 = f(BOLD, 50)
warn3 = wrap("But here's where it gets risky…", wf3, d, W - PAD * 2)
put(d, warn3, wf3, GOLD, y, 1.3)

footer(d, 3)
img.save(f"{OUT}/slide_03.png"); print("Slide 3 ✓")

# ══ SLIDE 4 — Escalation ══════════════════════════════════════════
img = base_cream(); d = ImageDraw.Draw(img)
bg_dots(d)
bg_circles(d)
gold_corner_lines(d)
navy_top_band(d, 130)
logo(d, light=True)

y = 155
hf4 = f(BOLD, 54)
h4 = wrap("THAT ONE ACCOUNT IS OFTEN A SIGN OF A BIGGER ISSUE.", hf4, d, W - PAD * 2)
y = put(d, h4, hf4, NAVY, y, 1.18)

y += 12; divider(d, y, GOLD, 2); y += 36

if4 = f(ITAL, 42)
intro4 = "Something else may have been missed too."
iw4 = d.textlength(intro4, font=if4)
d.text(((W - iw4) / 2, y), intro4, font=if4, fill=NAVY)
y += 70

items4 = ["An old retirement account.", "A second property.", "An investment account you forgot to transfer."]
rf4 = f(REG, 40)
for item in items4:
    d.text((PAD + 8, y + 4), "◆", font=f(BOLD, 32), fill=GOLD)
    lines_i = wrap(item, rf4, d, W - PAD * 2 - 55)
    for li in lines_i:
        d.text((PAD + 52, y), li, font=rf4, fill=NAVY)
        y += 52
    y += 8

y += 12; divider(d, y, GOLD, 2); y += 36

kf4 = f(BOLD, 50)
k1 = "The $500 isn't the problem."
k2 = "What it REVEALS is."
k1w = d.textlength(k1, font=kf4); k2w = d.textlength(k2, font=kf4)
d.text(((W - k1w) / 2, y), k1, font=kf4, fill=NAVY); y += 66
d.text(((W - k2w) / 2, y), k2, font=kf4, fill=GOLD)

footer(d, 4)
img.save(f"{OUT}/slide_04.png"); print("Slide 4 ✓")

# ══ SLIDE 5 — Consequence ═════════════════════════════════════════
img = base_cream(); d = ImageDraw.Draw(img)
bg_dots(d)
bg_circles(d)
gold_corner_lines(d)
scales_watermark(d)
navy_top_band(d, 130)
logo(d, light=True)

lf5 = f(SANS, 26); label5 = "CALIFORNIA PROBATE LAW"
lw5 = d.textlength(label5, font=lf5)
d.text(((W - lw5) / 2, 148), label5, font=lf5, fill=GOLD)
y = 185

hf5 = f(BOLD, 58)
h5 = wrap("PROBATE FEES ARE BASED ON THE GROSS VALUE OF THE ESTATE.", hf5, d, W - PAD * 2)
y = put(d, h5, hf5, NAVY, y, 1.18)

y += 14; divider(d, y, GOLD, 2); y += 36

sf5 = f(ITAL, 40)
subs5 = ["Not the size of the mistake.", "Not just the $500 account."]
y = put(d, subs5, sf5, GRAY, y, 1.4)

y += 14; divider(d, y, GOLD, 2); y += 36

wf5 = f(BOLD, 44)
w5 = wrap("If ANY significant asset is outside the trust — real estate, accounts, property — probate is now on the table.", wf5, d, W - PAD * 2)
put(d, w5, wf5, GOLD, y, 1.3)

footer(d, 5)
img.save(f"{OUT}/slide_05.png"); print("Slide 5 ✓")

# ══ SLIDE 6 — CTA ═════════════════════════════════════════════════
img = base_cream(); d = ImageDraw.Draw(img)
bg_dots(d)
bg_circles(d)
gold_corner_lines(d)
navy_top_band(d, 130)
logo(d, light=True)

y = 155
hf6 = f(BOLD, 58)
h6 = wrap("THE REAL PROBLEM ISN'T THE $500.", hf6, d, W - PAD * 2)
y = put(d, h6, hf6, NAVY, y, 1.18)

y += 14; divider(d, y, GOLD, 2); y += 36

if6 = f(ITAL, 40)
intro6 = "It's what it reveals:"
iw6 = d.textlength(intro6, font=if6)
d.text(((W - iw6) / 2, y), intro6, font=if6, fill=NAVY); y += 68

items6 = ["An incomplete plan.", "Unfunded assets.", "A system that fails your family when it matters most."]
rf6 = f(REG, 38)
for item in items6:
    d.text((PAD + 8, y + 4), "◆", font=f(BOLD, 32), fill=GOLD)
    lines_i = wrap(item, rf6, d, W - PAD * 2 - 55)
    for li in lines_i:
        d.text((PAD + 52, y), li, font=rf6, fill=NAVY)
        y += 52
    y += 10

y += 14; divider(d, y, GOLD, 2); y += 36

cf6 = f(BDIT, 42)
for line in ["It's not the big things that break a plan.", "It's the small ones that get overlooked."]:
    lw6 = d.textlength(line, font=cf6)
    d.text(((W - lw6) / 2, y), line, font=cf6, fill=NAVY)
    y += 58

y += 24
btf = f(SANSB, 36)
cta = "Book a Free Consultation"
ctaw = d.textlength(cta, font=btf)
bx = (W - ctaw - 70) // 2
d.rounded_rectangle([bx, y, bx + ctaw + 70, y + 68], radius=8, fill=NAVY)
d.text((bx + 35, y + 16), cta, font=btf, fill=WHITE)

y += 88
sitef = f(SANS, 28)
site = "mjtrust law.com"
sitew = d.textlength(site, font=sitef)
d.text(((W - sitew) / 2, y), site, font=sitef, fill=GOLD)

footer(d, 6)
img.save(f"{OUT}/slide_06.png"); print("Slide 6 ✓")

print(f"\nDone — {OUT}/")
