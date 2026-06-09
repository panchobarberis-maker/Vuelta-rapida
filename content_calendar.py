from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                 Paragraph, Spacer, HRFlowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import calendar as cal

OUT = "/home/user/Vuelta-rapida/content_calendar.pdf"

NAVY  = colors.HexColor("#1a2e4a")
GOLD  = colors.HexColor("#C2801A")
CREAM = colors.HexColor("#F5EFE6")
WHITE = colors.white
GRAY  = colors.HexColor("#999999")
LGRAY = colors.HexColor("#f9f9f9")
LCREAM= colors.HexColor("#fdf9f4")

C_HIST = colors.HexColor("#27ae60")
C_CARR = colors.HexColor("#C2801A")
C_MITO = colors.HexColor("#8e44ad")
C_POD  = colors.HexColor("#2980b9")
C_UGC  = colors.HexColor("#e74c3c")

YEAR, MONTH = 2026, 7
MONTH_LABEL = "JULIO 2026"

# {day: [(short_label, color, description, "ES"|"EN")]}
DAY_CONTENT = {
    # week 1 — Sun Jul 5
    5:  [("Podcast",      C_POD,  "Ep.1: Que pasa con tu herencia sin un plan", "ES")],
    6:  [("Historia",     C_HIST, "Apertura semanal + horarios de atencion",    "ES")],
    7:  [("Carrusel",     C_CARR, "Que es un Trust y por que lo necesitas en CA","ES")],
    8:  [("Hist. Review", C_HIST, "'Por fin tengo paz mental' - cliente",        "ES")],
    9:  [("Mito #1",      C_MITO, "Solo los ricos necesitan un trust",           "ES")],
    # week 2
    12: [("UGC Video",    C_UGC,  "Como protegi a mi familia con un trust",      "ES")],
    13: [("Historia",     C_HIST, "Apertura semanal + horarios de atencion",    "ES")],
    14: [("Carrusel",     C_CARR, "What happens without a will in California?",  "EN")],
    15: [("Hist. Review", C_HIST, "'They explained everything clearly' - client","EN")],
    16: [("Mito #2",      C_MITO, "A will is enough to avoid probate",           "EN")],
    # week 3
    19: [("Podcast",      C_POD,  "Ep.2: Propiedades en Mexico y EE.UU.",        "ES")],
    20: [("Historia",     C_HIST, "Apertura semanal + horarios de atencion",    "ES")],
    21: [("Carrusel",     C_CARR, "Los 5 documentos que toda familia necesita",  "ES")],
    22: [("Hist. Review", C_HIST, "'Nos ayudaron a proteger nuestra casa'",      "ES")],
    23: [("Mito #3",      C_MITO, "Mi esposo/a hereda todo automaticamente",     "ES")],
    # week 4
    26: [("UGC Video",    C_UGC,  "Real story: avoiding probate saved us months","EN")],
    27: [("Historia",     C_HIST, "Apertura semanal + horarios de atencion",    "ES")],
    28: [("Carrusel",     C_CARR, "Estate planning for blended families",        "EN")],
    29: [("Hist. Review", C_HIST, "'El proceso fue muy sencillo' - cliente",     "ES")],
    30: [("Mito #4",      C_MITO, "El trust es complicado y muy caro",           "ES")],
}

CELL_BG = {
    0: colors.HexColor("#edf7f0"),  # Mon - Historia
    1: colors.HexColor("#fff8e6"),  # Tue - Carrusel
    2: colors.HexColor("#edf7f0"),  # Wed - Historia Review
    3: colors.HexColor("#f2ebf9"),  # Thu - Mitos
    6: colors.HexColor("#fdecea"),  # Sun - Podcast/UGC
}

def make_para(text, fname, fsize, color, leading=None, align=TA_LEFT, space_after=0):
    opts = dict(fontName=fname, fontSize=fsize, textColor=color,
                alignment=align, spaceAfter=space_after)
    if leading:
        opts["leading"] = leading
    return ParagraphStyle("_", **opts)

def build_pdf():
    pw, ph = landscape(A4)
    doc = SimpleDocTemplate(OUT, pagesize=landscape(A4),
                            leftMargin=1.1*cm, rightMargin=1.1*cm,
                            topMargin=0.9*cm, bottomMargin=0.9*cm)
    elements = []

    # ── TITLE ──────────────────────────────────────────────────────────────────
    title_st = make_para("", "Helvetica-Bold", 20, NAVY, space_after=2)
    sub_st   = make_para("", "Helvetica",       9, GRAY, space_after=2)
    ov_st    = make_para("", "Helvetica-Bold", 11, NAVY, leading=14, space_after=5)

    elements.append(Paragraph("CONTENT CALENDAR — MJ TRUST LAW", title_st))
    elements.append(Paragraph(
        f"{MONTH_LABEL} | Instagram | 4 posts/week + 3 stories/week | "
        "English &amp; Spanish", sub_st))
    elements.append(HRFlowable(width="100%", thickness=2.5, color=GOLD, spaceAfter=6))
    elements.append(Paragraph(f"{MONTH_LABEL} — OVERVIEW", ov_st))

    # ── CALENDAR GRID ─────────────────────────────────────────────────────────
    first_wd, num_days = cal.monthrange(YEAR, MONTH)

    avail_w  = pw - 2.2*cm
    col_w    = avail_w / 7
    col_widths = [col_w] * 7

    DAY_NAMES = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    hdr_st = make_para("", "Helvetica-Bold", 9, WHITE, align=TA_CENTER)
    header_row = [Paragraph(d, hdr_st) for d in DAY_NAMES]

    # flatten days
    cells = [None] * first_wd + list(range(1, num_days + 1))
    while len(cells) % 7:
        cells.append(None)
    num_rows = len(cells) // 7

    date_st  = make_para("", "Helvetica-Bold", 11, NAVY, leading=14, space_after=2)
    lbl_st   = make_para("", "Helvetica-Bold",  7, WHITE, leading=9, space_after=1)
    cont_st  = make_para("", "Helvetica",        7, colors.HexColor("#333333"), leading=9, space_after=3)
    lang_es  = make_para("", "Helvetica-Bold",   7, GOLD,  leading=9)
    lang_en  = make_para("", "Helvetica-Bold",   7, colors.HexColor("#2980b9"), leading=9)

    grid = [header_row]
    for ri in range(num_rows):
        row = []
        for ci in range(7):
            day = cells[ri * 7 + ci]
            if not day:
                row.append("")
                continue
            items = DAY_CONTENT.get(day, [])
            paras = [Paragraph(str(day), date_st)]
            for label, col, text, lang in items:
                # label as small colored pill via nested table
                lbl_tbl = Table(
                    [[Paragraph(label, lbl_st)]],
                    colWidths=[col_w - 0.7*cm]
                )
                lbl_tbl.setStyle(TableStyle([
                    ("BACKGROUND",    (0,0),(-1,-1), col),
                    ("TOPPADDING",    (0,0),(-1,-1), 2),
                    ("BOTTOMPADDING", (0,0),(-1,-1), 2),
                    ("LEFTPADDING",   (0,0),(-1,-1), 4),
                    ("RIGHTPADDING",  (0,0),(-1,-1), 2),
                ]))
                paras.append(lbl_tbl)
                paras.append(Paragraph(text, cont_st))
                paras.append(Paragraph(lang, lang_es if lang == "ES" else lang_en))
            row.append(paras)
        grid.append(row)

    tbl = Table(grid, colWidths=col_widths)

    ts = [
        ("BACKGROUND",    (0,0), (6,0), NAVY),
        ("TOPPADDING",    (0,0), (6,0), 7),
        ("BOTTOMPADDING", (0,0), (6,0), 7),
        ("ALIGN",         (0,0), (6,0), "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",    (0,1), (-1,-1), 5),
        ("BOTTOMPADDING", (0,1), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("RIGHTPADDING",  (0,0), (-1,-1), 3),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#d0ccc5")),
        ("BACKGROUND",    (5,1), (5, num_rows), LGRAY),
        ("BACKGROUND",    (6,1), (6, num_rows), LCREAM),
    ]

    for ri in range(num_rows):
        for ci in range(7):
            day = cells[ri * 7 + ci]
            if day and day in DAY_CONTENT:
                bg = CELL_BG.get(ci, WHITE)
                ts.append(("BACKGROUND", (ci, ri+1), (ci, ri+1), bg))

    tbl.setStyle(TableStyle(ts))
    elements.append(tbl)

    # ── LEGEND ────────────────────────────────────────────────────────────────
    elements.append(Spacer(1, 0.25*cm))
    legend = [
        ("Historia (Lun + Mie)",      C_HIST),
        ("Carrusel (Mar)",             C_CARR),
        ("Mitos y Verdades (Jue)",     C_MITO),
        ("Podcast (Dom - semanas 1,3)", C_POD),
        ("UGC Video (Dom - semanas 2,4)", C_UGC),
    ]
    leg_row = []
    for label, col in legend:
        p = Table([[Paragraph(label,
                              ParagraphStyle("_", fontName="Helvetica-Bold",
                                             fontSize=6.5, textColor=WHITE))]],
                  colWidths=[4.2*cm])
        p.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), col),
            ("TOPPADDING",    (0,0),(-1,-1), 3),
            ("BOTTOMPADDING", (0,0),(-1,-1), 3),
            ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ]))
        leg_row.append(p)

    leg_tbl = Table([leg_row], colWidths=[4.5*cm]*5)
    leg_tbl.setStyle(TableStyle([
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0),(-1,-1), 0),
        ("RIGHTPADDING",(0,0),(-1,-1), 5),
    ]))
    elements.append(leg_tbl)

    doc.build(elements)
    print(f"PDF generado: {OUT}")

build_pdf()
