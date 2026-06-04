from PIL import Image, ImageDraw, ImageFont
import os, textwrap

W, H = 1080, 1350
NAVY   = (26, 46, 74)
CREAM  = (245, 239, 230)
GOLD   = (194, 130, 40)
WHITE  = (255, 255, 255)
LGRAY  = (180, 170, 155)

BOLD   = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REG    = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SERIF  = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"
SERIF_R= "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"

def fnt(path, size):
    return ImageFont.truetype(path, size)

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

def draw_text_block(draw, lines, font, color, x, y, align="center", page_w=W, line_spacing=1.3):
    for line in lines:
        lw = draw.textlength(line, font=font)
        lh = font.size
        if align == "center":
            draw.text(((page_w - lw) / 2, y), line, font=font, fill=color)
        else:
            draw.text((x, y), line, font=font, fill=color)
        y += int(lh * line_spacing)
    return y

def logo(draw, bg):
    text_color = GOLD if bg == NAVY else GOLD
    f = fnt(BOLD, 32)
    label = "MJ  TRUST LAW"
    lw = draw.textlength(label, font=f)
    x = (W - lw) / 2
    draw.text((x, 60), label, font=f, fill=text_color)
    draw.line([(x, 102), (x + lw, 102)], fill=GOLD, width=2)

def footer(draw, bg, page_num):
    y = H - 52
    draw.line([(60, y - 14), (W - 60, y - 14)], fill=LGRAY if bg==CREAM else (80,100,130), width=1)
    fc = LGRAY if bg == CREAM else (120, 140, 170)
    f = fnt(REG, 22)
    draw.text((60, y), "2026", font=f, fill=fc)
    site = "MJTRUST LAW.COM"
    sw = draw.textlength(site, font=f)
    draw.text(((W - sw) / 2, y), site, font=f, fill=fc)
    pn = f"PG0{page_num}"
    pw = draw.textlength(pn, font=f)
    draw.text((W - 60 - pw, y), pn, font=f, fill=fc)

def new(bg): return Image.new("RGB", (W, H), bg)

OUT = "/home/user/Vuelta-rapida/carousel"
os.makedirs(OUT, exist_ok=True)
PAD = 90

# ── SLIDE 1 ── Hook / Navy
img = new(NAVY); d = ImageDraw.Draw(img)
logo(d, NAVY)

# Gold top label
label = "ESTATE PLANNING MISTAKE"
lf = fnt(BOLD, 26)
lw = d.textlength(label, font=lf)
d.text(((W-lw)/2, 155), label, font=lf, fill=GOLD)
d.line([(PAD, 192),(W-PAD, 192)], fill=GOLD, width=1)

# Big serif quote
q1 = fnt(SERIF, 68)
q2 = fnt(SERIF, 62)
lines1 = ["Most people think:", '"Worst case,', 'I forgot a small', 'account…', 'no big deal."']
y = 225
for i, line in enumerate(lines1):
    lw2 = d.textlength(line, font=q1)
    d.text(((W-lw2)/2, y), line, font=q1, fill=WHITE)
    y += 82

# Gold subtext
d.line([(PAD, y+18),(W-PAD, y+18)], fill=GOLD, width=1)
y += 38
sub = fnt(BOLD, 34)
sub_lines = wrap("But in California, that tiny mistake can break your entire estate plan.", sub, d, W - PAD*2)
y = draw_text_block(d, sub_lines, sub, GOLD, PAD, y, line_spacing=1.4)

# CTA arrow
y += 30
cf = fnt(REG, 30)
cw = d.textlength("Swipe to see how  →", font=cf)
d.text(((W-cw)/2, y), "Swipe to see how  →", font=cf, fill=LGRAY)

footer(d, NAVY, 1)
img.save(f"{OUT}/slide_01.png")
print("Slide 1 done")

# ── SLIDE 2 ── Setup / Cream
img = new(CREAM); d = ImageDraw.Draw(img)
logo(d, CREAM)

hf = fnt(BOLD, 54)
h_lines = wrap("LET'S SAY YOU HAVE A TRUST.", hf, d, W - PAD*2)
y = 170
y = draw_text_block(d, h_lines, hf, NAVY, PAD, y, line_spacing=1.25)

d.line([(PAD, y+20),(W-PAD, y+20)], fill=GOLD, width=1)
y += 50

items = ["Your home is in it.", "Your beneficiaries are named.", "Everything looks perfect."]
cf2 = fnt(REG, 38)
for item in items:
    check_f = fnt(BOLD, 38)
    d.text((PAD + 10, y), "✓", font=check_f, fill=GOLD)
    d.text((PAD + 55, y), item, font=cf2, fill=NAVY)
    y += 68

d.line([(PAD, y+15),(W-PAD, y+15)], fill=GOLD, width=1)
y += 50

miss_f = fnt(SERIF, 52)
miss = "One thing gets missed…"
mw = d.textlength(miss, font=miss_f)
d.text(((W-mw)/2, y), miss, font=miss_f, fill=NAVY)

footer(d, CREAM, 2)
img.save(f"{OUT}/slide_02.png")
print("Slide 2 done")

# ── SLIDE 3 ── Problem / Navy
img = new(NAVY); d = ImageDraw.Draw(img)
logo(d, NAVY)

label2 = "THE OVERLOOKED ASSET"
lf2 = fnt(BOLD, 26)
lw2 = d.textlength(label2, font=lf2)
d.text(((W-lw2)/2, 155), label2, font=lf2, fill=GOLD)
d.line([(PAD, 192),(W-PAD, 192)], fill=GOLD, width=1)

big_f = fnt(BOLD, 110)
big = "$ 500"
bw = d.textlength(big, font=big_f)
d.text(((W-bw)/2, 215), big, font=big_f, fill=WHITE)

sub2 = fnt(BOLD, 34)
acc = "A bank account still in your individual name."
aw = d.textlength(acc, font=sub2)
d.text(((W-aw)/2, 355), acc, font=sub2, fill=GOLD)

d.line([(PAD, 415),(W-PAD, 415)], fill=(60,85,120), width=1)

body_f = fnt(REG, 36)
b1 = "On its own? Under California's small"
b2 = "estate rules — no probate needed."
for i, line in enumerate([b1, b2]):
    lw3 = d.textlength(line, font=body_f)
    d.text(((W-lw3)/2, 440 + i*52), line, font=body_f, fill=WHITE)

d.line([(PAD, 560),(W-PAD, 560)], fill=GOLD, width=2)

warn_f = fnt(BOLD, 40)
warn_lines = wrap("But here's where it gets risky…", warn_f, d, W - PAD*2)
y = 590
y = draw_text_block(d, warn_lines, warn_f, GOLD, PAD, y, line_spacing=1.3)

footer(d, NAVY, 3)
img.save(f"{OUT}/slide_03.png")
print("Slide 3 done")

# ── SLIDE 4 ── Escalation / Cream
img = new(CREAM); d = ImageDraw.Draw(img)
logo(d, CREAM)

hf4 = fnt(BOLD, 46)
h4 = wrap("THAT ONE ACCOUNT IS OFTEN A SIGN OF A BIGGER ISSUE.", hf4, d, W - PAD*2)
y = 165
y = draw_text_block(d, h4, hf4, NAVY, PAD, y, line_spacing=1.2)

d.line([(PAD, y+15),(W-PAD, y+15)], fill=GOLD, width=1)
y += 45

intro_f = fnt(SERIF_R, 36)
intro = "Something else may have been missed too."
iw = d.textlength(intro, font=intro_f)
d.text(((W-iw)/2, y), intro, font=intro_f, fill=NAVY)
y += 65

items4 = ["An old retirement account.", "A second property.", "An investment account you forgot to transfer."]
bf4 = fnt(REG, 36)
for item in items4:
    iw2 = d.textlength("◆", font=fnt(BOLD, 30))
    d.text((PAD + 10, y + 4), "◆", font=fnt(BOLD, 30), fill=GOLD)
    d.text((PAD + 50, y), item, font=bf4, fill=NAVY)
    y += 62

d.line([(PAD, y+15),(W-PAD, y+15)], fill=GOLD, width=2)
y += 40

key_f = fnt(BOLD, 42)
k1 = "The $500 isn't the problem."
k2 = "What it REVEALS is."
for i, line in enumerate([k1, k2]):
    lw4 = d.textlength(line, font=key_f)
    col = NAVY if i == 0 else GOLD
    d.text(((W-lw4)/2, y + i*60), line, font=key_f, fill=col)

footer(d, CREAM, 4)
img.save(f"{OUT}/slide_04.png")
print("Slide 4 done")

# ── SLIDE 5 ── Consequence / Navy
img = new(NAVY); d = ImageDraw.Draw(img)
logo(d, NAVY)

label5 = "CALIFORNIA PROBATE LAW"
lf5 = fnt(BOLD, 26)
lw5 = d.textlength(label5, font=lf5)
d.text(((W-lw5)/2, 155), label5, font=lf5, fill=GOLD)
d.line([(PAD, 192),(W-PAD, 192)], fill=GOLD, width=1)

hf5 = fnt(BOLD, 52)
h5 = wrap("PROBATE FEES ARE BASED ON THE GROSS VALUE OF THE ESTATE.", hf5, d, W - PAD*2)
y = 220
y = draw_text_block(d, h5, hf5, WHITE, PAD, y, line_spacing=1.2)

d.line([(PAD, y+15),(W-PAD, y+15)], fill=(60,85,120), width=1)
y += 40

sub5_f = fnt(REG, 36)
subs = ["Not the size of the mistake.", "Not just the $500 account."]
for line in subs:
    lw6 = d.textlength(line, font=sub5_f)
    d.text(((W-lw6)/2, y), line, font=sub5_f, fill=LGRAY)
    y += 55

d.line([(PAD, y+10),(W-PAD, y+10)], fill=GOLD, width=2)
y += 35

warn5_f = fnt(BOLD, 40)
w5 = wrap("If ANY significant asset is outside the trust — real estate, accounts, property — probate is now on the table.", warn5_f, d, W - PAD*2)
y = draw_text_block(d, w5, warn5_f, GOLD, PAD, y, line_spacing=1.3)

footer(d, NAVY, 5)
img.save(f"{OUT}/slide_05.png")
print("Slide 5 done")

# ── SLIDE 6 ── CTA / Cream
img = new(CREAM); d = ImageDraw.Draw(img)
logo(d, CREAM)

hf6 = fnt(BOLD, 52)
h6 = wrap("THE REAL PROBLEM ISN'T THE $500.", hf6, d, W - PAD*2)
y = 168
y = draw_text_block(d, h6, hf6, NAVY, PAD, y, line_spacing=1.2)

d.line([(PAD, y+15),(W-PAD, y+15)], fill=GOLD, width=1)
y += 42

intro6 = fnt(SERIF_R, 36)
iline = "It's what it reveals:"
ilw = d.textlength(iline, font=intro6)
d.text(((W-ilw)/2, y), iline, font=intro6, fill=NAVY)
y += 62

items6 = ["An incomplete plan.", "Unfunded assets.", "A system that fails your family when it matters most."]
bf6 = fnt(REG, 34)
for item in items6:
    d.text((PAD + 10, y + 4), "◆", font=fnt(BOLD, 28), fill=GOLD)
    lines_item = wrap(item, bf6, d, W - PAD*2 - 50)
    for li in lines_item:
        d.text((PAD + 50, y), li, font=bf6, fill=NAVY)
        y += 50
    y += 8

d.line([(PAD, y+10),(W-PAD, y+10)], fill=GOLD, width=2)
y += 35

close_f = fnt(SERIF, 38)
c1 = "It's not the big things that break a plan."
c2 = "It's the small ones that get overlooked."
for i, line in enumerate([c1, c2]):
    clw = d.textlength(line, font=close_f)
    d.text(((W-clw)/2, y + i*56), line, font=close_f, fill=NAVY)
y += 130

cta_f = fnt(BOLD, 36)
cta = "📅  Book a Free Consultation"
ctaw = d.textlength(cta, font=cta_f)
# CTA button
btn_x = (W - ctaw - 60) // 2
btn_y = y
d.rounded_rectangle([btn_x, btn_y, btn_x + ctaw + 60, btn_y + 64], radius=8, fill=NAVY)
d.text((btn_x + 30, btn_y + 14), cta, font=cta_f, fill=WHITE)

y += 85
site_f = fnt(REG, 28)
site = "mjtrust law.com"
sw = d.textlength(site, font=site_f)
d.text(((W-sw)/2, y), site, font=site_f, fill=GOLD)

footer(d, CREAM, 6)
img.save(f"{OUT}/slide_06.png")
print("Slide 6 done")
print(f"\nAll slides saved to {OUT}/")
