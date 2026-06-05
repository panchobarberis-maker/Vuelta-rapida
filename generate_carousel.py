from PIL import Image, ImageDraw, ImageFont
import os

W, H  = 1080, 1350
NAVY  = (26, 46, 74)
NAVY2 = (18, 32, 54)
CREAM = (242, 234, 220)
GOLD  = (190, 128, 38)
GOLD2 = (215, 165, 70)
WHITE = (255, 255, 255)
GRAY  = (148, 135, 115)
PAD   = 72

BOLD  = "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf"
REG   = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
ITAL  = "/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf"
BDIT  = "/usr/share/fonts/truetype/freefont/FreeSerifBoldItalic.ttf"
SANS  = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANSI = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

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

def put_c(draw, lines, font, color, y, gap=1.25):
    for line in lines:
        lw = draw.textlength(line, font=font)
        draw.text(((W - lw) / 2, y), line, font=font, fill=color)
        y += int(font.size * gap)
    return y

def put_l(draw, lines, font, color, x, y, gap=1.25):
    for line in lines:
        draw.text((x, y), line, font=font, fill=color)
        y += int(font.size * gap)
    return y

def dots(draw, color=(215, 205, 188)):
    for x in range(36, W, 54):
        for y in range(36, H, 54):
            draw.ellipse([x-2, y-2, x+2, y+2], fill=color)

def corner_ornament(draw, light=False):
    c = GOLD if not light else GOLD2
    s = 3
    draw.line([(W-110,22),(W-22,22)], fill=c, width=s)
    draw.line([(W-22,22),(W-22,110)], fill=c, width=s)
    draw.line([(22,H-110),(22,H-22)], fill=c, width=s)
    draw.line([(22,H-22),(110,H-22)], fill=c, width=s)

def big_circle_bg(draw, cx, cy, r, color):
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=2)
    draw.ellipse([cx-r+30, cy-r+30, cx+r-30, cy+r-30], outline=color, width=1)

def logo_bar(draw, bg="cream"):
    col = WHITE if bg == "navy" else NAVY
    line_col = GOLD
    lf = f(SANSB, 30)
    label = "MJ   TRUST LAW"
    lw = draw.textlength(label, font=lf)
    x = (W - lw) / 2
    draw.text((x, 48), label, font=lf, fill=col)
    draw.line([(x, 92), (x + lw, 92)], fill=line_col, width=2)

def footer(draw, n, bg="cream"):
    lc = GRAY if bg == "cream" else (110, 130, 160)
    y = H - 52
    draw.line([(PAD, y-16),(W-PAD, y-16)], fill=lc, width=1)
    sf = f(SANS, 22)
    draw.text((PAD, y), "2026", font=sf, fill=lc)
    site = "MJTRUST LAW.COM"
    sw = draw.textlength(site, font=sf)
    draw.text(((W-sw)/2, y), site, font=sf, fill=lc)
    pn = f"PG0{n}"
    pw = draw.textlength(pn, font=sf)
    draw.text((W-PAD-pw, y), pn, font=sf, fill=lc)

OUT = "/home/user/Vuelta-rapida/carousel"
os.makedirs(OUT, exist_ok=True)

# ══════════════════════════════════════════════════════════════
# SLIDE 1 — Hook (photo placeholder — navy split layout)
# ══════════════════════════════════════════════════════════════
img = Image.new("RGB", (W, H), NAVY2)
d = ImageDraw.Draw(img)

# Photo placeholder panel (right side, full height)
ph_x = W // 2
d.rectangle([ph_x, 0, W, H], fill=(35, 52, 80))
pf = f(SANSI, 26)
pw2 = d.textlength("[ foto abogada ]", font=pf)
d.text((ph_x + (W//2 - pw2)//2, H//2 - 20), "[ foto abogada ]", font=pf, fill=(70, 90, 120))

# Left panel content
logo_bar(d, "navy")
corner_ornament(d, light=True)

# Big decorative quote mark
qf = f(BOLD, 220)
d.text((PAD - 18, 90), "“", font=qf, fill=(40, 62, 96))

y = 195
lf1 = f(SANS, 24)
lab = "ESTATE PLANNING"
lw1 = d.textlength(lab, font=lf1)
d.text((PAD, y), lab, font=lf1, fill=GOLD)
d.line([(PAD, y+34),(PAD+lw1, y+34)], fill=GOLD, width=2)
y += 58

hf1 = f(BOLD, 74)
for line in ["Most", "people", "think:"]:
    d.text((PAD, y), line, font=hf1, fill=WHITE)
    y += 84

y += 10
d.line([(PAD, y),(ph_x - 40, y)], fill=GOLD, width=2)
y += 24

if1 = f(ITAL, 48)
for line in ["“No big", "deal.”"]:
    d.text((PAD, y), line, font=if1, fill=GOLD2)
    y += 60

y += 16
sf1 = f(BOLD, 34)
sub_lines = wrap("In California, that 'small' mistake can break your entire estate plan.", sf1, d, ph_x - PAD - 40)
y = put_l(d, sub_lines, sf1, WHITE, PAD, y, 1.3)

y += 24
af1 = f(SANSI, 28)
d.text((PAD, y), "Swipe to see how  →", font=af1, fill=GRAY)

footer(d, 1, "navy")
img.save(f"{OUT}/slide_01.png"); print("Slide 1 ✓")

# ══════════════════════════════════════════════════════════════
# SLIDE 2 — Setup (cream full)
# ══════════════════════════════════════════════════════════════
img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
dots(d)
big_circle_bg(d, W+80, -80, 380, (215, 205, 185))
big_circle_bg(d, -60, H+60, 300, (215, 205, 185))
corner_ornament(d)

# Navy top accent bar
d.rectangle([0, 0, W, 110], fill=NAVY)
logo_bar(d, "navy")

# Big slide label
y = 130
d.rectangle([PAD, y, W-PAD, y+3], fill=GOLD)
y += 20

# Giant number "2" as decorative element
nf = f(BOLD, 280)
d.text((W - 200, 100), "2", font=nf, fill=(228, 220, 206))

hf2 = f(BOLD, 72)
d.text((PAD, y), "LET'S SAY", font=hf2, fill=NAVY)
y += 86
d.text((PAD, y), "YOU HAVE", font=hf2, fill=NAVY)
y += 86
gf2 = f(BDIT, 82)
d.text((PAD, y), "A TRUST.", font=gf2, fill=GOLD)
y += 105

d.rectangle([PAD, y, W-PAD, y+3], fill=GOLD)
y += 32

items = [
    ("✓", "Your home is in it."),
    ("✓", "Your beneficiaries are named."),
    ("✓", "Everything looks perfect."),
]
cf2 = f(REG, 46)
glyph_f = f(BOLD, 46)
for glyph, item in items:
    d.text((PAD, y), glyph, font=glyph_f, fill=GOLD)
    d.text((PAD + 58, y), item, font=cf2, fill=NAVY)
    y += 76

y += 20
d.rectangle([PAD, y, W-PAD, y+3], fill=GOLD)
y += 36

mf2 = f(BDIT, 68)
miss = "One thing"
miss2 = "gets missed…"
d.text((PAD, y), miss, font=mf2, fill=NAVY); y += 80
d.text((PAD, y), miss2, font=mf2, fill=NAVY); y += 80

# Subtle arrow pointing right at bottom
d.text((W - 110, y - 30), "→", font=f(BOLD, 80), fill=GOLD)

footer(d, 2)
img.save(f"{OUT}/slide_02.png"); print("Slide 2 ✓")

# ══════════════════════════════════════════════════════════════
# SLIDE 3 — $500
# ══════════════════════════════════════════════════════════════
img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
dots(d)
big_circle_bg(d, W//2, H//2, 420, (215, 205, 185))
corner_ornament(d)

d.rectangle([0, 0, W, 110], fill=NAVY)
logo_bar(d, "navy")

lf3 = f(SANSB, 26); lab3 = "THE OVERLOOKED ASSET"
lw3 = d.textlength(lab3, font=lf3)
d.text(((W-lw3)/2, 128), lab3, font=lf3, fill=GOLD)

# Massive $500
bf3 = f(BOLD, 200)
big = "$500"
bw = d.textlength(big, font=bf3)
d.text(((W-bw)/2, 160), big, font=bf3, fill=NAVY)

d.rectangle([PAD, 388, W-PAD, 391], fill=GOLD)

y = 410
sf3 = f(BDIT, 44)
s3 = "Still in your individual name."
sw3 = d.textlength(s3, font=sf3)
d.text(((W-sw3)/2, y), s3, font=sf3, fill=GOLD)
y += 66

rf3 = f(REG, 40)
lines_b3 = wrap("Under California's small estate rules, on its own — no probate needed.", rf3, d, W-PAD*2)
y = put_c(d, lines_b3, rf3, NAVY, y, 1.35)

y += 20
d.rectangle([PAD, y, W-PAD, y+3], fill=GOLD); y += 36

wf3 = f(BOLD, 56)
warn = wrap("But here's where it gets risky…", wf3, d, W-PAD*2)
y = put_c(d, warn, wf3, GOLD, y, 1.3)

y += 30
xf3 = f(REG, 38)
lines_x3 = wrap("One forgotten account is all it takes to expose your entire estate to probate court.", xf3, d, W-PAD*2)
y = put_c(d, lines_x3, xf3, NAVY, y, 1.35)

footer(d, 3)
img.save(f"{OUT}/slide_03.png"); print("Slide 3 ✓")

# ══════════════════════════════════════════════════════════════
# SLIDE 4 — Escalation
# ══════════════════════════════════════════════════════════════
img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
dots(d)
big_circle_bg(d, W+100, H//2, 380, (215,205,185))
corner_ornament(d)

d.rectangle([0, 0, W, 110], fill=NAVY)
logo_bar(d, "navy")

y = 128
lf4 = f(SANSB, 26); lab4 = "THE BIGGER PICTURE"
lw4 = d.textlength(lab4, font=lf4)
d.text(((W-lw4)/2, y), lab4, font=lf4, fill=GOLD)
y += 42

hf4 = f(BOLD, 62)
h4 = wrap("THAT ONE ACCOUNT IS OFTEN A SIGN OF A BIGGER ISSUE.", hf4, d, W-PAD*2)
y = put_c(d, h4, hf4, NAVY, y, 1.18)

d.rectangle([PAD, y+10, W-PAD, y+13], fill=GOLD); y += 44

if4 = f(ITAL, 44)
intro4 = "Something else may have been missed too."
iw4 = d.textlength(intro4, font=if4)
d.text(((W-iw4)/2, y), intro4, font=if4, fill=NAVY); y += 72

items4 = ["An old retirement account.", "A second property.", "An investment account you\nforgot to transfer."]
rf4 = f(REG, 42)
df4 = f(BOLD, 32)
for item in items4:
    for i, line in enumerate(item.split("\n")):
        if i == 0:
            d.text((PAD+8, y+5), "◆", font=df4, fill=GOLD)
            d.text((PAD+52, y), line, font=rf4, fill=NAVY)
        else:
            d.text((PAD+52, y), line, font=rf4, fill=NAVY)
        y += 56
    y += 6

d.rectangle([PAD, y+8, W-PAD, y+11], fill=GOLD); y += 42

kf4 = f(BOLD, 58)
k1 = "The $500 isn't the problem."
k2 = "What it REVEALS is."
k1w = d.textlength(k1, font=kf4); k2w = d.textlength(k2, font=kf4)
d.text(((W-k1w)/2, y), k1, font=kf4, fill=NAVY); y += 72
d.text(((W-k2w)/2, y), k2, font=kf4, fill=GOLD); y += 80

af4 = f(SANSI, 34)
note = "It’s a pattern. And patterns need fixing."
nw4 = d.textlength(note, font=af4)
d.text(((W-nw4)/2, y), note, font=af4, fill=GRAY)

footer(d, 4)
img.save(f"{OUT}/slide_04.png"); print("Slide 4 ✓")

# ══════════════════════════════════════════════════════════════
# SLIDE 5 — Consequence (navy bg)
# ══════════════════════════════════════════════════════════════
img = Image.new("RGB", (W, H), NAVY2)
d = ImageDraw.Draw(img)
big_circle_bg(d, W+120, H-120, 480, (38, 58, 90))
big_circle_bg(d, -80, 200, 260, (38, 58, 90))
corner_ornament(d, light=True)
logo_bar(d, "navy")

# Giant background text watermark
wf5bg = f(BOLD, 200)
d.text((-20, 160), "PRO", font=wf5bg, fill=(30, 48, 72))
d.text((-20, 350), "BATE", font=wf5bg, fill=(30, 48, 72))

y = 130
lf5 = f(SANSB, 26); lab5 = "CALIFORNIA LAW"
lw5 = d.textlength(lab5, font=lf5)
d.text(((W-lw5)/2, y), lab5, font=lf5, fill=GOLD)
y += 46; d.rectangle([PAD, y, W-PAD, y+2], fill=GOLD); y += 32

hf5 = f(BOLD, 62)
h5 = wrap("PROBATE FEES ARE BASED ON THE GROSS VALUE OF THE ESTATE.", hf5, d, W-PAD*2)
y = put_c(d, h5, hf5, WHITE, y, 1.2)

d.rectangle([PAD, y+14, W-PAD, y+17], fill=GOLD); y += 50

sf5 = f(ITAL, 42)
subs5 = ["Not the size of the mistake.", "Not just the $500 account."]
y = put_c(d, subs5, sf5, (180, 165, 145), y, 1.4)

d.rectangle([PAD, y+16, W-PAD, y+19], fill=GOLD); y += 50

wf5 = f(BOLD, 48)
w5 = wrap("If ANY significant asset sits outside your trust — real estate, accounts, property — probate is on the table.", wf5, d, W-PAD*2)
y = put_c(d, w5, wf5, GOLD, y, 1.3)

y += 32
ef5 = f(REG, 38)
extra = wrap("And probate in California means months of court process, public records, and fees that can reach 4–6% of your gross estate.", ef5, d, W-PAD*2)
put_c(d, extra, ef5, WHITE, y, 1.35)

footer(d, 5, "navy")
img.save(f"{OUT}/slide_05.png"); print("Slide 5 ✓")

# ══════════════════════════════════════════════════════════════
# SLIDE 6 — CTA
# ══════════════════════════════════════════════════════════════
img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
dots(d)
big_circle_bg(d, W//2, H//2+60, 460, (215,205,185))
corner_ornament(d)

d.rectangle([0, 0, W, 110], fill=NAVY)
logo_bar(d, "navy")

y = 128
hf6 = f(BOLD, 64)
h6 = wrap("THE REAL PROBLEM ISN'T THE $500.", hf6, d, W-PAD*2)
y = put_c(d, h6, hf6, NAVY, y, 1.18)

d.rectangle([PAD, y+10, W-PAD, y+13], fill=GOLD); y += 44

if6 = f(ITAL, 44)
i6 = "It’s what it reveals:"
iw6 = d.textlength(i6, font=if6)
d.text(((W-iw6)/2, y), i6, font=if6, fill=NAVY); y += 72

items6 = ["An incomplete plan.", "Unfunded assets.", "A system that fails your family\nwhen it matters most."]
rf6 = f(REG, 40)
df6 = f(BOLD, 32)
for item in items6:
    for i, line in enumerate(item.split("\n")):
        if i == 0:
            d.text((PAD+8, y+5), "◆", font=df6, fill=GOLD)
            d.text((PAD+52, y), line, font=rf6, fill=NAVY)
        else:
            d.text((PAD+52, y), line, font=rf6, fill=NAVY)
        y += 52
    y += 10

d.rectangle([PAD, y+10, W-PAD, y+13], fill=GOLD); y += 44

cf6 = f(BDIT, 44)
for line in ["It’s not the big things that break a plan.", "It’s the small ones that get overlooked."]:
    lw6 = d.textlength(line, font=cf6)
    d.text(((W-lw6)/2, y), line, font=cf6, fill=NAVY); y += 62

y += 28
btf = f(SANSB, 38)
cta = "Book a Free Consultation"
ctaw = d.textlength(cta, font=btf)
bx = (W - ctaw - 80) // 2
d.rounded_rectangle([bx, y, bx+ctaw+80, y+72], radius=8, fill=NAVY)
d.text((bx+40, y+18), cta, font=btf, fill=WHITE)

y += 96
sitef = f(SANSB, 30)
site = "mjtrust law.com"
sitew = d.textlength(site, font=sitef)
d.text(((W-sitew)/2, y), site, font=sitef, fill=GOLD)

footer(d, 6)
img.save(f"{OUT}/slide_06.png"); print("Slide 6 ✓")

print(f"\nDone — {OUT}/")
