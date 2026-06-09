from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import PageBreak

OUT = "/home/user/Vuelta-rapida/content_calendar.pdf"

NAVY  = colors.HexColor("#1a2e4a")
GOLD  = colors.HexColor("#C2801A")
CREAM = colors.HexColor("#F5EFE6")
LIGHT = colors.HexColor("#faf7f2")
WHITE = colors.white
GRAY  = colors.HexColor("#888888")
DARK  = colors.HexColor("#333333")

FORMAT_COLORS = {
    "Historia":        colors.HexColor("#e8f4f8"),
    "Carrusel":        colors.HexColor("#fff8e6"),
    "Mitos y Verdades":colors.HexColor("#f0ede8"),
    "Podcast":         colors.HexColor("#e6ede6"),
    "UGC Video":       colors.HexColor("#f0e6ee"),
}
FORMAT_ACCENT = {
    "Historia":        colors.HexColor("#2980b9"),
    "Carrusel":        GOLD,
    "Mitos y Verdades":NAVY,
    "Podcast":         colors.HexColor("#27ae60"),
    "UGC Video":       colors.HexColor("#8e44ad"),
}

weeks = [
    {
        "num": 1,
        "posts": [
            ("Lunes",   "Historia",         "ES", "Apertura semanal + horarios de atencion"),
            ("Martes",  "Carrusel",         "ES", "Que es un Trust y por que necesitas uno en California"),
            ("Jueves",  "Mitos y Verdades", "ES", "MITO: Solo los ricos necesitan un trust"),
            ("Domingo", "Podcast",          "ES", "Episodio 1: Que pasa con tu herencia si no tienes un plan"),
        ]
    },
    {
        "num": 2,
        "posts": [
            ("Lunes",   "Historia",         "ES", "Apertura semanal + horarios de atencion"),
            ("Martes",  "Carrusel",         "EN", "What happens if you die without a will in California?"),
            ("Jueves",  "Mitos y Verdades", "EN", "MYTH: A will is enough to avoid probate"),
            ("Domingo", "UGC Video",        "ES", "Cliente comparte: como un trust protejo a su familia"),
        ]
    },
    {
        "num": 3,
        "posts": [
            ("Lunes",   "Historia",         "ES", "Apertura semanal + horarios de atencion"),
            ("Martes",  "Carrusel",         "ES", "Los 5 documentos que toda familia necesita tener"),
            ("Jueves",  "Mitos y Verdades", "ES", "MITO: Mi esposo/a hereda todo automaticamente"),
            ("Domingo", "Podcast",          "ES", "Episodio 2: Propiedades en Mexico y EE.UU. que debes saber"),
        ]
    },
    {
        "num": 4,
        "posts": [
            ("Lunes",   "Historia",         "ES", "Apertura semanal + horarios de atencion"),
            ("Martes",  "Carrusel",         "EN", "Estate planning for blended families"),
            ("Jueves",  "Mitos y Verdades", "ES", "MITO: El trust es complicado y muy caro"),
            ("Domingo", "UGC Video",        "EN", "Real story: avoiding probate saved us months and thousands"),
        ]
    },
    {
        "num": 5,
        "posts": [
            ("Lunes",   "Historia",         "ES", "Apertura semanal + horarios de atencion"),
            ("Martes",  "Carrusel",         "ES", "Como proteger a tus hijos menores con un trust"),
            ("Jueves",  "Mitos y Verdades", "ES", "MITO: Ya tengo seguro de vida, no necesito mas nada"),
            ("Domingo", "Podcast",          "EN", "Episode 3: Power of Attorney - what it is and when you need it"),
        ]
    },
    {
        "num": 6,
        "posts": [
            ("Lunes",   "Historia",         "ES", "Apertura semanal + horarios de atencion"),
            ("Martes",  "Carrusel",         "ES", "Probate en California: cuanto tiempo y cuanto cuesta"),
            ("Jueves",  "Mitos y Verdades", "EN", "MYTH: I'm too young to think about estate planning"),
            ("Domingo", "UGC Video",        "ES", "Testimonio: como organizamos la herencia de mi papa"),
        ]
    },
]

def build_pdf():
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        rightMargin=1.8*cm,
        leftMargin=1.8*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=22,
                                  textColor=WHITE, alignment=TA_CENTER, spaceAfter=4)
    sub_style   = ParagraphStyle("sub",   fontName="Helvetica",      fontSize=10,
                                  textColor=CREAM,  alignment=TA_CENTER)
    week_style  = ParagraphStyle("week",  fontName="Helvetica-Bold", fontSize=13,
                                  textColor=NAVY,   spaceBefore=14, spaceAfter=6)
    cell_fmt    = ParagraphStyle("cfmt",  fontName="Helvetica-Bold", fontSize=8,
                                  textColor=WHITE)
    cell_day    = ParagraphStyle("cday",  fontName="Helvetica-Bold", fontSize=9,
                                  textColor=DARK)
    cell_topic  = ParagraphStyle("ctopic",fontName="Helvetica",      fontSize=8,
                                  textColor=DARK,   leading=11)
    cell_lang   = ParagraphStyle("clang", fontName="Helvetica-Bold", fontSize=7,
                                  textColor=GRAY)
    note_style  = ParagraphStyle("note",  fontName="Helvetica-Oblique", fontSize=8,
                                  textColor=GRAY,   spaceBefore=4)

    elements = []

    # ── HEADER BANNER ─────────────────────────────────────────────────────────
    header_data = [[
        Paragraph("MJ TRUST LAW", title_style),
        Paragraph("Content Calendar · Instagram", sub_style),
        Paragraph("70% ES &nbsp; · &nbsp; 30% EN", sub_style),
    ]]
    header_table = Table(header_data, colWidths=[6*cm, 7*cm, 4.5*cm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,-1), NAVY),
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0),(-1,-1), 14),
        ("BOTTOMPADDING",(0,0),(-1,-1), 14),
        ("LEFTPADDING", (0,0),(0,-1),  16),
        ("ROUNDEDCORNERS", [6]),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.3*cm))

    # ── GOLD STRIPE ───────────────────────────────────────────────────────────
    elements.append(HRFlowable(width="100%", thickness=3, color=GOLD, spaceAfter=10))

    # ── LEGEND ────────────────────────────────────────────────────────────────
    legend_items = []
    for fmt, bg in FORMAT_COLORS.items():
        acc = FORMAT_ACCENT[fmt]
        pill = Table([[Paragraph(fmt, ParagraphStyle("lp", fontName="Helvetica-Bold",
                                                      fontSize=7, textColor=WHITE))]],
                     colWidths=[2.6*cm])
        pill.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(-1,-1), acc),
            ("TOPPADDING",   (0,0),(-1,-1), 3),
            ("BOTTOMPADDING",(0,0),(-1,-1), 3),
            ("LEFTPADDING",  (0,0),(-1,-1), 6),
            ("ROUNDEDCORNERS",[4]),
        ]))
        legend_items.append(pill)

    legend_table = Table([legend_items], colWidths=[3.3*cm]*5)
    legend_table.setStyle(TableStyle([
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0),(-1,-1), 0),
        ("RIGHTPADDING",(0,0),(-1,-1), 4),
    ]))
    elements.append(legend_table)
    elements.append(Spacer(1, 0.4*cm))

    # ── COLUMN HEADERS ────────────────────────────────────────────────────────
    col_w = [1.8*cm, 2.8*cm, 1.0*cm, 11.2*cm]
    hdr_style = ParagraphStyle("hdr", fontName="Helvetica-Bold", fontSize=8,
                                textColor=WHITE, alignment=TA_CENTER)
    col_headers = [
        [Paragraph("DIA",     hdr_style),
         Paragraph("FORMATO", hdr_style),
         Paragraph("ID",      hdr_style),
         Paragraph("CONTENIDO", hdr_style)]
    ]
    hdr_tbl = Table(col_headers, colWidths=col_w)
    hdr_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), NAVY),
        ("TOPPADDING",   (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING",  (0,0),(-1,-1), 6),
    ]))
    elements.append(hdr_tbl)

    # ── WEEKS ─────────────────────────────────────────────────────────────────
    for week in weeks:
        elements.append(
            Paragraph(f"SEMANA {week['num']}", week_style)
        )

        rows = []
        row_styles = []
        ri = 0
        for (day, fmt, lang, topic) in week["posts"]:
            bg  = FORMAT_COLORS[fmt]
            acc = FORMAT_ACCENT[fmt]

            fmt_cell = Table(
                [[Paragraph(fmt, ParagraphStyle("fp", fontName="Helvetica-Bold",
                                                 fontSize=7.5, textColor=WHITE))]],
                colWidths=[2.6*cm]
            )
            fmt_cell.setStyle(TableStyle([
                ("BACKGROUND",   (0,0),(-1,-1), acc),
                ("TOPPADDING",   (0,0),(-1,-1), 4),
                ("BOTTOMPADDING",(0,0),(-1,-1), 4),
                ("LEFTPADDING",  (0,0),(-1,-1), 5),
                ("ROUNDEDCORNERS",[3]),
            ]))

            lang_hex = "#C2801A" if lang == "ES" else "#2980b9"
            lang_cell = Paragraph(
                f"<font color='{lang_hex}'><b>{lang}</b></font>",
                ParagraphStyle("lc", fontName="Helvetica-Bold", fontSize=8, alignment=TA_CENTER)
            )

            rows.append([
                Paragraph(day,   cell_day),
                fmt_cell,
                lang_cell,
                Paragraph(topic, cell_topic),
            ])

            row_styles += [
                ("BACKGROUND",   (0, ri), (-1, ri), bg),
                ("TOPPADDING",   (0, ri), (-1, ri), 7),
                ("BOTTOMPADDING",(0, ri), (-1, ri), 7),
                ("LEFTPADDING",  (0, ri), (-1, ri), 6),
                ("LINEBELOW",    (0, ri), (-1, ri), 0.5, colors.HexColor("#e0d8cc")),
                ("VALIGN",       (0, ri), (-1, ri), "MIDDLE"),
            ]
            ri += 1

        tbl = Table(rows, colWidths=col_w)
        tbl.setStyle(TableStyle(row_styles + [
            ("BOX", (0,0),(-1,-1), 0.5, colors.HexColor("#d0c8bc")),
        ]))
        elements.append(tbl)
        elements.append(Spacer(1, 0.15*cm))

    # ── FOOTER NOTES ──────────────────────────────────────────────────────────
    elements.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceBefore=14, spaceAfter=6))
    notes = [
        "Lunes: plantilla fija de horarios, cambia solo el mensaje semanal.",
        "Domingos: Podcast y UGC Video se alternan semana a semana.",
        "Distribucion de idioma: 70% Espanol / 30% Ingles.",
        "Chula Vista · Estate Planning · MJ Trust Law",
    ]
    for n in notes:
        elements.append(Paragraph(n, note_style))

    doc.build(elements)
    print(f"PDF generado: {OUT}")

build_pdf()
