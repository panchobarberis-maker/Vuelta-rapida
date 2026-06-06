from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, textwrap

W, H = 1080, 1350
NAVY   = (26, 46, 74)
GOLD   = (194, 128, 26)
CREAM  = (245, 239, 230)
WHITE  = (255, 255, 255)
DARK   = (10, 18, 30)
GRAY   = (120, 120, 120)

IMG_DIR = "/home/user/Vuelta-rapida/mjtrust law/"
OUT_DIR = "/home/user/Vuelta-rapida/carousel-html/previews/"
os.makedirs(OUT_DIR, exist_ok=True)

SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS      = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF_B   = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF     = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
LIB_BOLD  = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
LIB       = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def wrap_text(draw, text, font_obj, max_width):
    words = text.split()
    lines = []
    line = ""
    for w in words:
        test = (line + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font_obj)
        if bbox[2] - bbox[0] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines

def centered_text(draw, text, font_obj, y, color, max_width=W):
    lines = wrap_text(draw, text, font_obj, max_width - 120)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_obj)
        x = (W - (bbox[2] - bbox[0])) // 2
        draw.text((x, y), line, fill=color, font=font_obj)
        y += (bbox[3] - bbox[1]) + 16
    return y

def load_img(filename):
    return Image.open(IMG_DIR + filename).convert("RGBA")

def gold_bar(img, y, h=4):
    draw = ImageDraw.Draw(img)
    draw.rectangle([(80, y), (W - 80, y + h)], fill=GOLD)

def page_indicator(img, current, total=6, dark=False):
    """Draw elegant progress bars + 'XX / 06' centered at bottom."""
    draw = ImageDraw.Draw(img)
    bar_w, bar_h, gap = 44, 3, 10
    total_w = total * bar_w + (total - 1) * gap
    x0 = (W - total_w) // 2
    y_bars = H - 72
    active_col  = GOLD
    inactive_col = (255, 255, 255, 71) if dark else (26, 46, 74, 46)
    for i in range(total):
        x = x0 + i * (bar_w + gap)
        col = active_col if i == current - 1 else inactive_col[:3]
        draw.rounded_rectangle([(x, y_bars), (x + bar_w, y_bars + bar_h)], radius=2, fill=col)
    f_num = font(LIB, 20)
    num_text = f"{current:02d} / {total:02d}"
    bbox = draw.textbbox((0, 0), num_text, font=f_num)
    tx = (W - (bbox[2] - bbox[0])) // 2
    num_col = (255, 255, 255, 122) if dark else (176, 152, 120)
    draw.text((tx, H - 52), num_text, fill=num_col if not dark else (200, 190, 175), font=f_num)
    if dark:
        draw.text((tx, H - 52), num_text, fill=(200, 190, 175), font=f_num)

# ── SLIDE 1: Split layout - cream left + attorney photo right ─────────────────
def slide1():
    img = Image.new("RGBA", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Right panel: attorney photo — cover crop (no stretch), right 60%
    try:
        photo = load_img("10.webp")
        pw = int(W * 0.72)
        orig_w, orig_h = photo.size
        scale = max(pw / orig_w, H / orig_h)
        new_w = int(orig_w * scale)
        new_h = int(orig_h * scale)
        photo = photo.resize((new_w, new_h), Image.LANCZOS)
        cx = int((new_w - pw) * 0.35)  # 35% desde la izquierda — cara centrada visible
        region = photo.crop((cx, 0, cx + pw, H))
        x_off = W - pw
        img.paste(region, (x_off, 0), region)
    except Exception as e:
        print(f"Slide 1 photo error: {e}")

    # Cream gradient: sólido hasta 36% del panel, desaparece al 78%
    panel_w = int(W * 0.72)
    blend_start = int(panel_w * 0.36)   # 36% del panel = ~20% del slide
    blend_end   = int(panel_w * 0.78)   # 78% del panel = ~56% del slide
    cream_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for x in range(blend_end):
        if x <= blend_start:
            a = 255
        else:
            t = (x - blend_start) / (blend_end - blend_start)
            a = int(255 * (1 - t))
        for y in range(H):
            cream_overlay.putpixel((x, y), CREAM + (a,))
    img = Image.alpha_composite(img, cream_overlay)

    draw = ImageDraw.Draw(img)

    # Left panel content
    lw = int(W * 0.50)

    # Logo
    try:
        logo = Image.open(IMG_DIR + "logo.jpg").convert("RGBA")
        logo_w = 220
        logo_h = int(logo.size[1] * (logo_w / logo.size[0]))
        logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
        img.paste(logo, (80, 80), logo if logo.mode == 'RGBA' else None)
    except:
        f = font(SANS_BOLD, 28)
        draw.text((80, 80), "MJ TRUST LAW", fill=NAVY, font=f)

    # Gold line
    draw.rectangle([(80, 220), (lw - 40, 224)], fill=GOLD)

    # Tag
    f_tag = font(LIB, 22)
    draw.text((80, 244), "ESTATE PLANNING", fill=GOLD, font=f_tag)

    # Main headline
    f_h = font(SERIF_B, 62)
    y = 300
    lines = ["Proteger", "lo que", "construiste", "es posible."]
    for line in lines:
        draw.text((80, y), line, fill=NAVY, font=f_h)
        y += 74

    # Subheading
    f_sub = font(LIB, 28)
    y += 20
    sub_lines = wrap_text(draw, "Planes de estate planning para familias en California.", f_sub, lw - 100)
    for line in sub_lines:
        draw.text((80, y), line, fill=GRAY, font=f_sub)
        y += 38

    img = img.convert("RGB")
    page_indicator(img, 1, dark=False)
    img.save(OUT_DIR + "slide1.jpg", quality=90)
    print("Slide 1 saved")

# ── SLIDE 2: Cream design - big typography ────────────────────────────────────
def slide2():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Large decorative circles
    for cx, cy, r in [(820, 180, 260), (900, 1200, 320), (160, 900, 180)]:
        draw.ellipse([(cx-r, cy-r), (cx+r, cy+r)], outline=GOLD + (0,), width=2)
    # dot grid (subtle)
    for x in range(80, W-80, 44):
        for y in range(80, H-80, 44):
            draw.ellipse([(x-1, y-1), (x+1, y+1)], fill=(194, 128, 26, 40))

    # Gold accent top
    draw.rectangle([(80, 80), (200, 84)], fill=GOLD)

    # Tag
    f_tag = font(LIB, 22)
    draw.text((80, 102), "SITUACIÓN REAL", fill=GOLD, font=f_tag)

    # Big quote text
    f_big = font(SERIF_B, 88)
    y = 320
    for line in ["Tenían", "todo en", "orden."]:
        bbox = draw.textbbox((0,0), line, font=f_big)
        draw.text((80, y), line, fill=NAVY, font=f_big)
        y += 102

    # Underline
    draw.rectangle([(80, y + 10), (420, y + 16)], fill=GOLD)
    y += 50

    # Body text
    f_body = font(LIB, 32)
    body = "Una casa. Una cuenta de retiro. La intención de armar su trust el año que viene."
    body_lines = wrap_text(draw, body, f_body, W - 160)
    for line in body_lines:
        draw.text((80, y), line, fill=(60, 60, 60), font=f_body)
        y += 46

    y += 20
    f_bold = font(LIB_BOLD, 32)
    draw.text((80, y), "Entonces pasó algo inesperado.", fill=NAVY, font=f_bold)

    page_indicator(img, 2, dark=False)
    img.save(OUT_DIR + "slide2.jpg", quality=90)
    print("Slide 2 saved")

# ── SLIDE 3: Hispanic family photo with overlay ───────────────────────────────
def slide3():
    try:
        photo = load_img("depositphotos_2348091-stock-photo-hispanic-family-portrait-in-the.jpg")
    except:
        photo = Image.new("RGBA", (W, H), (100, 80, 60, 255))

    pw, ph = photo.size
    scale = max(W/pw, H/ph)
    new_w, new_h = int(pw * scale), int(ph * scale)
    photo = photo.resize((new_w, new_h), Image.LANCZOS)
    x_off = (new_w - W) // 2
    y_off = (new_h - H) // 2
    photo = photo.crop((x_off, y_off, x_off + W, y_off + H))

    img = photo.copy()

    # Warm gradient overlay: cream top -> transparent middle -> dark bottom
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        if y < H * 0.35:
            alpha = int(200 * (1 - y / (H * 0.35)))
            r, g, b = 245, 235, 215
        elif y > H * 0.55:
            t = (y - H * 0.55) / (H * 0.45)
            alpha = int(210 * t)
            r, g, b = 10, 18, 30
        else:
            alpha = 0
            r, g, b = 0, 0, 0
        for x in range(W):
            overlay.putpixel((x, y), (r, g, b, alpha))
    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)

    # Top content
    f_tag = font(LIB, 24)
    draw.text((80, 90), "LO QUE NO PLANEARON", fill=GOLD, font=f_tag)
    draw.rectangle([(80, 122), (340, 126)], fill=GOLD)

    # Bottom content
    f_h = font(SERIF_B, 72)
    y = H - 480
    for line in ["Y sin un plan,"]:
        bbox = draw.textbbox((0, 0), line, font=f_h)
        draw.text((80, y), line, fill=WHITE, font=f_h)
        y += 86
    f_h2 = font(SERIF_B, 68)
    for line in ["la familia tuvo", "que esperar."]:
        draw.text((80, y), line, fill=WHITE, font=f_h2)
        y += 80

    y += 16
    f_body = font(LIB, 30)
    body_lines = wrap_text(draw, "Probate en California: meses de proceso y miles en honorarios.", f_body, W - 160)
    for line in body_lines:
        draw.text((80, y), line, fill=(220, 210, 195), font=f_body)
        y += 44

    img = img.convert("RGB")
    page_indicator(img, 3, dark=True)
    img.save(OUT_DIR + "slide3.jpg", quality=90)
    print("Slide 3 saved")

# ── SLIDE 4: Cream - $45,000 as visual element ───────────────────────────────
def slide4():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Gold corner brackets
    bw, bl = 60, 4  # bracket width, line thickness
    pad = 70
    for (x1, y1, x2, y2) in [(pad, pad, pad+bw, pad+bw), (W-pad-bw, pad, W-pad, pad+bw),
                               (pad, H-pad-bw, pad+bw, H-pad), (W-pad-bw, H-pad-bw, W-pad, H-pad)]:
        # top-left
        if x1 == pad and y1 == pad:
            draw.rectangle([(x1, y1), (x1+bw, y1+bl)], fill=GOLD)
            draw.rectangle([(x1, y1), (x1+bl, y1+bw)], fill=GOLD)
        elif x1 == W-pad-bw and y1 == pad:
            draw.rectangle([(x1, y1), (x2, y1+bl)], fill=GOLD)
            draw.rectangle([(x2-bl, y1), (x2, y2)], fill=GOLD)
        elif y1 == H-pad-bw:
            if x1 == pad:
                draw.rectangle([(x1, y2-bl), (x1+bw, y2)], fill=GOLD)
                draw.rectangle([(x1, y1), (x1+bl, y2)], fill=GOLD)
            else:
                draw.rectangle([(x1, y2-bl), (x2, y2)], fill=GOLD)
                draw.rectangle([(x2-bl, y1), (x2, y2)], fill=GOLD)

    # Tag
    f_tag = font(LIB, 24)
    draw.text((80, 130), "EL COSTO REAL", fill=GOLD, font=f_tag)
    draw.rectangle([(80, 162), (280, 166)], fill=GOLD)

    # Huge number as design element
    f_huge = font(SERIF_B, 180)
    num_text = "$45,000"
    bbox = draw.textbbox((0, 0), num_text, font=f_huge)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw.text((x, 220), num_text, fill=NAVY, font=f_huge)

    # Subtitle under number
    f_sub = font(LIB, 28)
    sub = "en honorarios de probate"
    bbox = draw.textbbox((0, 0), sub, font=f_sub)
    draw.text(((W - (bbox[2]-bbox[0])) // 2, 430), sub, fill=GRAY, font=f_sub)

    # Gold divider
    draw.rectangle([(W//2 - 120, 490), (W//2 + 120, 494)], fill=GOLD)

    # Body
    f_body = font(LIB, 32)
    y = 530
    lines = [
        "Para una propiedad de $700,000 en",
        "el área de San Diego, los honorarios",
        "legales obligatorios pueden superar",
        "esa cifra.",
    ]
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=f_body)
        draw.text(((W - (bbox[2]-bbox[0])) // 2, y), line, fill=(60, 60, 60), font=f_body)
        y += 46

    # Bold kicker
    y += 30
    f_bold = font(LIB_BOLD, 34)
    kicker = "Un trust evita todo eso."
    bbox = draw.textbbox((0, 0), kicker, font=f_bold)
    draw.text(((W - (bbox[2]-bbox[0])) // 2, y), kicker, fill=NAVY, font=f_bold)

    # Dots
    for i, filled in enumerate([False, True, False, False, False]):
        cx = W//2 + (i - 2) * 28
    page_indicator(img, 4, dark=False)
    img.save(OUT_DIR + "slide4.jpg", quality=90)
    print("Slide 4 saved")

# ── SLIDE 5: Cream - quote design ────────────────────────────────────────────
def slide5():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Inner frame border
    pad = 55
    draw.rectangle([(pad, pad), (W-pad, H-pad)], outline=GOLD, width=2)

    # Dot grid accent (top-right corner area)
    for x in range(W - 300, W - 80, 36):
        for y in range(90, 320, 36):
            draw.ellipse([(x-1, y-1), (x+1, y+1)], fill=(*GOLD, 60))

    # Big decorative quote marks
    f_quote = font(SERIF_B, 240)
    draw.text((90, 60), "“", fill=(*GOLD, 30), font=f_quote)
    # Use a simple approach - draw giant quote marks
    f_q = font(SERIF_B, 220)
    draw.text((80, 40), '"', fill=(194, 128, 26), font=f_q)

    # Section tag
    f_tag = font(LIB, 22)
    draw.text((110, 330), "LA SOLUCIÓN", fill=GOLD, font=f_tag)
    draw.rectangle([(110, 360), (310, 364)], fill=GOLD)

    # Quote text
    f_h = font(SERIF_B, 54)
    y = 400
    lines = ["No hace falta tener", "todo claro para dar", "el primer paso."]
    for line in lines:
        draw.text((110, y), line, fill=NAVY, font=f_h)
        y += 68

    # Gold line
    draw.rectangle([(110, y + 10), (450, y + 14)], fill=GOLD)
    y += 50

    # Body
    f_body = font(LIB, 30)
    body = "En una consulta gratuita de 30 minutos revisamos tu situación y te damos un presupuesto concreto."
    body_lines = wrap_text(draw, body, f_body, W - 220)
    for line in body_lines:
        draw.text((110, y), line, fill=(70, 70, 70), font=f_body)
        y += 46

    # Author attribution style
    y += 20
    f_attr = font(LIB_BOLD, 26)
    draw.text((110, y), "MJ Trust Law — Chula Vista, CA", fill=GOLD, font=f_attr)

    page_indicator(img, 5, dark=False)
    img.save(OUT_DIR + "slide5.jpg", quality=90)
    print("Slide 5 saved")

# ── SLIDE 6: Attorney photo + dark overlay + CTA ─────────────────────────────
def slide6():
    try:
        photo = load_img("10.webp")
    except:
        photo = Image.new("RGBA", (W, H), (40, 60, 80, 255))

    orig_w, orig_h = photo.size
    # Cover crop maintaining aspect ratio, anchor top for face
    scale = max(W / orig_w, H / orig_h)
    new_w, new_h = int(orig_w * scale), int(orig_h * scale)
    photo = photo.resize((new_w, new_h), Image.LANCZOS)
    x_off = (new_w - W) // 2
    y_off = 0  # top anchor keeps face in frame
    photo = photo.crop((x_off, y_off, x_off + W, y_off + H))

    img = photo.copy()

    # Dark gradient overlay top and bottom
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        if y < H * 0.5:
            t = 1 - (y / (H * 0.5))
            alpha = int(180 * t)
        else:
            t = (y - H * 0.5) / (H * 0.5)
            alpha = int(220 * t)
        r, g, b = DARK
        for x in range(W):
            overlay.putpixel((x, y), (r, g, b, alpha))
    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)

    # Logo top
    try:
        logo = Image.open(IMG_DIR + "logo.jpg").convert("RGBA")
        # Make logo visible on dark: apply white tint
        logo_w = 200
        logo_h = int(logo.size[1] * (logo_w / logo.size[0]))
        logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
        x_logo = (W - logo_w) // 2
        img.paste(logo, (x_logo, 70), logo if logo.mode == 'RGBA' else None)
    except:
        f_logo = font(SANS_BOLD, 30)
        bbox = draw.textbbox((0,0), "MJ TRUST LAW", font=f_logo)
        draw.text(((W-(bbox[2]-bbox[0]))//2, 80), "MJ TRUST LAW", fill=WHITE, font=f_logo)

    # CTA block - centered bottom
    y = H - 560

    f_tag = font(LIB, 24)
    tag = "PRIMER PASO SIN COSTO"
    bbox = draw.textbbox((0, 0), tag, font=f_tag)
    draw.text(((W-(bbox[2]-bbox[0]))//2, y), tag, fill=GOLD, font=f_tag)
    y += 40
    draw.rectangle([(W//2-100, y), (W//2+100, y+3)], fill=GOLD)
    y += 24

    f_h = font(SERIF_B, 66)
    for line in ["Consultá gratis.", "Sin formularios,", "sin compromiso."]:
        bbox = draw.textbbox((0, 0), line, font=f_h)
        draw.text(((W-(bbox[2]-bbox[0]))//2, y), line, fill=WHITE, font=f_h)
        y += 78

    y += 20
    # CTA button
    btn_w, btn_h = 680, 86
    bx = (W - btn_w) // 2
    draw.rectangle([(bx, y), (bx + btn_w, y + btn_h)], fill=GOLD)
    f_btn = font(LIB_BOLD, 30)
    btn_text = "Agendar consulta gratuita"
    bbox = draw.textbbox((0, 0), btn_text, font=f_btn)
    tx = bx + (btn_w - (bbox[2]-bbox[0])) // 2
    ty = y + (btn_h - (bbox[3]-bbox[1])) // 2
    draw.text((tx, ty), btn_text, fill=DARK, font=f_btn)

    y += btn_h + 28
    f_contact = font(LIB, 26)
    contact = "mjtrust.law  |  Chula Vista, CA"
    bbox = draw.textbbox((0, 0), contact, font=f_contact)
    draw.text(((W-(bbox[2]-bbox[0]))//2, y), contact, fill=(200, 190, 175), font=f_contact)

    img = img.convert("RGB")
    page_indicator(img, 6, dark=True)
    img.save(OUT_DIR + "slide6.jpg", quality=90)
    print("Slide 6 saved")


slide1()
slide2()
slide3()
slide4()
slide5()
slide6()
print("All slides rendered.")
