from PIL import Image, ImageDraw, ImageFont
import os

W, H  = 1080, 1350
NAVY  = (26, 46, 74)
CREAM = (240, 232, 218)
GOLD  = (190, 128, 38)
WHITE = (255, 255, 255)
GRAY  = (155, 142, 122)
PAD   = 88

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

def logo(draw):
    lf = f(SANSB, 28)
    label = "MJ   TRUST LAW"
    lw = draw.textlength(label, font=lf)
    x = (W - lw) / 2
    draw.text((x, 55), label, font=lf, fill=GOLD)
    draw.line([(x, 94), (x + lw, 94)], fill=GOLD, width=2)

def footer(draw, page_num):
    y = H - 54
    draw.line([(PAD, y - 16), (W - PAD, y - 16)], fill=GRAY, width=1)
    sf = f(SANS, 22)
    draw.text((PAD, y), "2026", font=sf, fill=GRAY)
    site = "MJTRUST LAW.COM"
    sw = draw.textlength(site, font=sf)
    draw.text(((W - sw) / 2, y), site, font=sf, fill=GRAY)
    pn = f"PG0{page_num}"
    pw = draw.textlength(pn, font=sf)
    draw.text((W - PAD - pw, y), pn, font=sf, fill=GRAY)

def divider(draw, y, color=GOLD):
    draw.line([(PAD, y), (W - PAD, y)], fill=color, width=1)
    return y

def base(): return Image.new("RGB", (W, H), CREAM)

OUT = "/home/user/Vuelta-rapida/carousel"
os.makedirs(OUT, exist_ok=True)

# ── SLIDE 1 — Hook
img = base(); d = ImageDraw.Draw(img)
logo(d)

# Top label
lf = f(SANS, 24); label = "ESTATE PLANNING ALERT"
lw = d.textlength(label, font=lf)
d.text(((W - lw) / 2, 122), label, font=lf, fill=GOLD)
divider(d, 155)

# Opening italic quote
y = 185
q = f(BDIT, 62)
lines = wrap('Most people think:', q, d, W - PAD * 2)
y = put(d, lines, q, NAVY, y, 1.2)

q2 = f(ITAL, 66)
quote_lines = ['"Worst case,', 'I forgot a small', 'account…', 'no big deal."']
for line in quote_lines:
    lw2 = d.textlength(line, font=q2)
    d.text(((W - lw2) / 2, y), line, font=q2, fill=NAVY)
    y += 74

y += 12
divider(d, y)
y += 30

bf = f(BOLD, 36)
sub = wrap("But in California, that tiny mistake can break your entire estate plan.", bf, d, W - PAD * 2)
y = put(d, sub, bf, GOLD, y, 1.35)

y += 20
af = f(ITAL, 30)
arr = "Swipe to see how  →"
aw = d.textlength(arr, font=af)
d.text(((W - aw) / 2, y), arr, font=af, fill=GRAY)

footer(d, 1)
img.save(f"{OUT}/slide_01.png"); print("Slide 1 done")

# ── SLIDE 2 — Setup
img = base(); d = ImageDraw.Draw(img)
logo(d)
divider(d, 150)
y = 178

hf = f(BOLD, 58)
h = wrap("LET'S SAY YOU HAVE A TRUST.", hf, d, W - PAD * 2)
y = put(d, h, hf, NAVY, y, 1.2)

y += 16; divider(d, y); y += 40

items = ["Your home is in it.", "Your beneficiaries are named.", "Everything looks perfect."]
cf = f(REG, 40)
for item in items:
    gf = f(BOLD, 38)
    d.text((PAD + 8, y + 2), "✓", font=gf, fill=GOLD)
    d.text((PAD + 56, y), item, font=cf, fill=NAVY)
    y += 70

y += 10; divider(d, y); y += 40

mf = f(BDIT, 56)
miss = "One thing gets missed…"
mw = d.textlength(miss, font=mf)
d.text(((W - mw) / 2, y), miss, font=mf, fill=NAVY)

footer(d, 2)
img.save(f"{OUT}/slide_02.png"); print("Slide 2 done")

# ── SLIDE 3 — The $500
img = base(); d = ImageDraw.Draw(img)
logo(d)

lf3 = f(SANS, 24); label3 = "THE OVERLOOKED ASSET"
lw3 = d.textlength(label3, font=lf3)
d.text(((W - lw3) / 2, 122), label3, font=lf3, fill=GOLD)
divider(d, 155)

bigf = f(BOLD, 118)
big = "$500"
bw = d.textlength(big, font=bigf)
d.text(((W - bw) / 2, 175), big, font=bigf, fill=NAVY)

sf3 = f(BDIT, 36)
sub3 = "A bank account still in your individual name."
sw3 = d.textlength(sub3, font=sf3)
d.text(((W - sw3) / 2, 325), sub3, font=sf3, fill=GOLD)

y = 380; divider(d, y); y += 36

bf3 = f(REG, 38)
body3 = ["On its own? Under California's small", "estate rules — no probate needed."]
y = put(d, body3, bf3, NAVY, y, 1.3)

y += 20; divider(d, y); y += 36

wf3 = f(BOLD, 44)
warn3 = wrap("But here's where it gets risky…", wf3, d, W - PAD * 2)
put(d, warn3, wf3, GOLD, y, 1.3)

footer(d, 3)
img.save(f"{OUT}/slide_03.png"); print("Slide 3 done")

# ── SLIDE 4 — Escalation
img = base(); d = ImageDraw.Draw(img)
logo(d)
divider(d, 150); y = 178

hf4 = f(BOLD, 48)
h4 = wrap("THAT ONE ACCOUNT IS OFTEN A SIGN OF A BIGGER ISSUE.", hf4, d, W - PAD * 2)
y = put(d, h4, hf4, NAVY, y, 1.2)

y += 16; divider(d, y); y += 36

if4 = f(ITAL, 38)
intro4 = "Something else may have been missed too."
iw4 = d.textlength(intro4, font=if4)
d.text(((W - iw4) / 2, y), intro4, font=if4, fill=NAVY)
y += 64

items4 = ["An old retirement account.", "A second property.", "An investment account you forgot to transfer."]
rf4 = f(REG, 36)
for item in items4:
    d.text((PAD + 8, y + 4), "◆", font=f(BOLD, 28), fill=GOLD)
    d.text((PAD + 50, y), item, font=rf4, fill=NAVY)
    y += 60

y += 12; divider(d, y); y += 36

kf4 = f(BOLD, 44)
k1 = "The $500 isn't the problem."
k2 = "What it REVEALS is."
k1w = d.textlength(k1, font=kf4)
k2w = d.textlength(k2, font=kf4)
d.text(((W - k1w) / 2, y), k1, font=kf4, fill=NAVY); y += 58
d.text(((W - k2w) / 2, y), k2, font=kf4, fill=GOLD)

footer(d, 4)
img.save(f"{OUT}/slide_04.png"); print("Slide 4 done")

# ── SLIDE 5 — Consequence
img = base(); d = ImageDraw.Draw(img)
logo(d)

lf5 = f(SANS, 24); label5 = "CALIFORNIA PROBATE LAW"
lw5 = d.textlength(label5, font=lf5)
d.text(((W - lw5) / 2, 122), label5, font=lf5, fill=GOLD)
divider(d, 155); y = 182

hf5 = f(BOLD, 52)
h5 = wrap("PROBATE FEES ARE BASED ON THE GROSS VALUE OF THE ESTATE.", hf5, d, W - PAD * 2)
y = put(d, h5, hf5, NAVY, y, 1.2)

y += 16; divider(d, y); y += 36

sf5 = f(ITAL, 36)
subs5 = ["Not the size of the mistake.", "Not just the $500 account."]
y = put(d, subs5, sf5, GRAY, y, 1.4)

y += 16; divider(d, y, GOLD); y += 36

wf5 = f(BOLD, 40)
w5 = wrap("If ANY significant asset is outside the trust — real estate, accounts, property — probate is now on the table.", wf5, d, W - PAD * 2)
put(d, w5, wf5, GOLD, y, 1.3)

footer(d, 5)
img.save(f"{OUT}/slide_05.png"); print("Slide 5 done")

# ── SLIDE 6 — CTA
img = base(); d = ImageDraw.Draw(img)
logo(d)
divider(d, 150); y = 178

hf6 = f(BOLD, 52)
h6 = wrap("THE REAL PROBLEM ISN'T THE $500.", hf6, d, W - PAD * 2)
y = put(d, h6, hf6, NAVY, y, 1.2)

y += 16; divider(d, y); y += 36

if6 = f(ITAL, 36)
intro6 = "It's what it reveals:"
iw6 = d.textlength(intro6, font=if6)
d.text(((W - iw6) / 2, y), intro6, font=if6, fill=NAVY)
y += 60

items6 = ["An incomplete plan.", "Unfunded assets.", "A system that fails your family when it matters most."]
rf6 = f(REG, 34)
for item in items6:
    d.text((PAD + 8, y + 4), "◆", font=f(BOLD, 28), fill=GOLD)
    lines_i = wrap(item, rf6, d, W - PAD * 2 - 50)
    for li in lines_i:
        d.text((PAD + 50, y), li, font=rf6, fill=NAVY)
        y += 48
    y += 8

y += 16; divider(d, y, GOLD); y += 36

cf6 = f(BDIT, 38)
c1 = "It's not the big things that break a plan."
c2 = "It's the small ones that get overlooked."
for line in [c1, c2]:
    lw6 = d.textlength(line, font=cf6)
    d.text(((W - lw6) / 2, y), line, font=cf6, fill=NAVY)
    y += 54

y += 20
btf = f(SANSB, 34)
cta = "Book a Free Consultation"
ctaw = d.textlength(cta, font=btf)
bx = (W - ctaw - 60) // 2
d.rounded_rectangle([bx, y, bx + ctaw + 60, y + 62], radius=6, fill=NAVY)
d.text((bx + 30, y + 14), cta, font=btf, fill=WHITE)

y += 80
sitef = f(SANS, 26)
site = "mjtrust law.com"
sitew = d.textlength(site, font=sitef)
d.text(((W - sitew) / 2, y), site, font=sitef, fill=GOLD)

footer(d, 6)
img.save(f"{OUT}/slide_06.png"); print("Slide 6 done")
print(f"\nAll slides saved to {OUT}/")
