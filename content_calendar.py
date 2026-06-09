from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                 Paragraph, Spacer, HRFlowable, PageBreak)
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

DAY_CONTENT = {
    5:  [("Podcast",      C_POD,  "Ep.1: Que pasa con tu herencia sin un plan", "ES")],
    6:  [("Historia",     C_HIST, "Apertura semanal + horarios de atencion",    "ES")],
    7:  [("Carrusel",     C_CARR, "Que es un Trust y por que lo necesitas en CA","ES")],
    8:  [("Hist. Review", C_HIST, "'Por fin tengo paz mental' - cliente",        "ES")],
    9:  [("Mito #1",      C_MITO, "Solo los ricos necesitan un trust",           "ES")],
    12: [("UGC Video",    C_UGC,  "Como protegi a mi familia con un trust",      "ES")],
    13: [("Historia",     C_HIST, "Apertura semanal + horarios de atencion",    "ES")],
    14: [("Carrusel",     C_CARR, "What happens without a will in California?",  "EN")],
    15: [("Hist. Review", C_HIST, "'They explained everything clearly' - client","EN")],
    16: [("Mito #2",      C_MITO, "A will is enough to avoid probate",           "EN")],
    19: [("Podcast",      C_POD,  "Ep.2: Propiedades en Mexico y EE.UU.",        "ES")],
    20: [("Historia",     C_HIST, "Apertura semanal + horarios de atencion",    "ES")],
    21: [("Carrusel",     C_CARR, "Los 5 documentos que toda familia necesita",  "ES")],
    22: [("Hist. Review", C_HIST, "'Nos ayudaron a proteger nuestra casa'",      "ES")],
    23: [("Mito #3",      C_MITO, "Mi esposo/a hereda todo automaticamente",     "ES")],
    26: [("UGC Video",    C_UGC,  "Real story: avoiding probate saved us months","EN")],
    27: [("Historia",     C_HIST, "Apertura semanal + horarios de atencion",    "ES")],
    28: [("Carrusel",     C_CARR, "Estate planning for blended families",        "EN")],
    29: [("Hist. Review", C_HIST, "'El proceso fue muy sencillo' - cliente",     "ES")],
    30: [("Mito #4",      C_MITO, "El trust es complicado y muy caro",           "ES")],
}

CELL_BG = {
    0: colors.HexColor("#edf7f0"),
    1: colors.HexColor("#fff8e6"),
    2: colors.HexColor("#edf7f0"),
    3: colors.HexColor("#f2ebf9"),
    6: colors.HexColor("#fdecea"),
}

# ── DETAILED CONTENT ────────────────────────────────────────────────────────
# (date_label, format, color, title, description)
DETAIL = [
    # HISTORIAS LUNES
    ("Lunes (repetido)", "Historia - Horarios", C_HIST,
     "Apertura semanal + horarios",
     "Historia fija cada lunes: plantilla con los horarios de atencion y un saludo breve. "
     "Objetivo: que los seguidores sepan cuando pueden llamar o escribir. Simple, util, consistente."),

    # HISTORIAS MIERCOLES
    ("Mie 8 Jul", "Historia - Review", C_HIST,
     "'Por fin tengo paz mental'",
     "Una clienta comparte en sus propias palabras como se sentia antes (angustia, no saber que pasaria con su casa) "
     "y como se siente ahora. Sin nombres completos. Solo la emocion real. Termina con: Nosotros tambien podemos ayudarte."),

    ("Mie 15 Jul", "Historia - Review", C_HIST,
     "'They explained everything clearly'",
     "Cliente anglohablante. Menciona que nunca entendia el tema legal hasta que MJ Trust Law le explico paso a paso. "
     "Refuerza el mensaje de que el estudio es accesible y bilingue."),

    ("Mie 22 Jul", "Historia - Review", C_HIST,
     "'Nos ayudaron a proteger nuestra casa'",
     "Pareja latina que tenia una casa en Chula Vista. Temian que si uno de los dos fallecia, el otro perderia la propiedad. "
     "MJ Trust Law les armo el trust. Ahora estan tranquilos. Historia breve, emocional, cercana."),

    ("Mie 29 Jul", "Historia - Review", C_HIST,
     "'El proceso fue muy sencillo'",
     "Desmiente el mito de que armar un trust es complicado. El cliente cuenta que en pocas reuniones ya tenia todo listo. "
     "Ideal para terminar el mes y dejar ganas de contactar."),

    # CARRUSELES
    ("Mar 7 Jul", "Carrusel", C_CARR,
     "Que es un Trust y por que lo necesitas",
     "CASO: Maria tiene una casa en Chula Vista, dos hijos y un negocio pequeno. "
     "Nunca armo un trust porque penso que era para ricos. Cuando fallecio, sus hijos tardaron 18 meses "
     "en resolver el tema en los tribunales y gastaron miles de dolares. "
     "El carrusel explica que es un trust, para que sirve y como hubiera cambiado la historia de Maria. "
     "Sin jerga legal. Lenguaje de barrio."),

    ("Mar 14 Jul", "Carrusel", C_CARR,
     "What happens without a will in California?",
     "CASE: John and Carmen owned a home together. When John passed away, Carmen assumed the house was automatically hers. "
     "California probate court said otherwise. The process took over a year. "
     "Slides walk through what 'intestate succession' actually means in plain English, "
     "using their story as the thread. No legal terms without explanation."),

    ("Mar 21 Jul", "Carrusel", C_CARR,
     "Los 5 documentos que toda familia necesita",
     "CASO: La familia Lopez cree que con el seguro de vida alcanza. "
     "El carrusel revela los 5 documentos clave: trust, testamento, poder notarial, directiva medica y beneficiarios actualizados. "
     "Cada slide = 1 documento. Explicado con una situacion real de que pasa si no lo tenes. "
     "Formato de lista practica, accionable, sin texto largo."),

    ("Mar 28 Jul", "Carrusel", C_CARR,
     "Estate planning for blended families",
     "CASE: Carlos has 3 kids from a first marriage. His new wife Diana has 2. "
     "They never updated their estate plan after the wedding. "
     "Slides show the 4 most common problems blended families face and how a trust solves each one. "
     "Tone: empathetic, non-judgmental, practical."),

    # MITOS Y VERDADES
    ("Jue 9 Jul", "Mito y Verdad", C_MITO,
     "Solo los ricos necesitan un trust",
     "MITO: Si no soy millonario no necesito planificacion patrimonial. "
     "VERDAD: En California, si tu casa vale mas de $184,500 y no esta en un trust, "
     "tus herederos van a probate de todas formas. El trust no es lujo, es proteccion basica para cualquier familia."),

    ("Jue 16 Jul", "Mito y Verdad", C_MITO,
     "A will is enough to avoid probate",
     "MYTH: I have a will, so my family is protected. "
     "TRUTH: A will does NOT avoid probate in California. It is a document that goes THROUGH probate court. "
     "Only a properly funded trust keeps your estate out of court. "
     "Most people don't know this until it's too late."),

    ("Jue 23 Jul", "Mito y Verdad", C_MITO,
     "Mi esposo/a hereda todo automaticamente",
     "MITO: Si fallezco, mi pareja recibe todo sin problemas. "
     "VERDAD: Depende de como estan titulados los bienes. Si hay hijos de una relacion anterior, "
     "cuentas individuales o propiedades sin retitular, el proceso puede ser muy complicado. "
     "Muchas familias descubren esto cuando ya es demasiado tarde."),

    ("Jue 30 Jul", "Mito y Verdad", C_MITO,
     "El trust es complicado y muy caro",
     "MITO: Armar un trust lleva meses y cuesta una fortuna. "
     "VERDAD: El proceso es mas sencillo de lo que parece y cuesta una fraccion de lo que costaria el probate. "
     "En California, los honorarios de probate pueden llegar al 4-6% del valor bruto del patrimonio. "
     "Un trust se hace una vez y te protege para siempre."),

    # UGC
    ("Dom 12 Jul", "UGC Video", C_UGC,
     "Como protegi a mi familia con un trust",
     "Video autentico de un cliente (puede ser grabado en casa, sin produccion). "
     "Cuenta su historia: el momento en que se dio cuenta de que necesitaba un trust, "
     "como fue el proceso con MJ Trust Law y como se siente ahora. "
     "Valor: la gente cree mas en personas reales que en anuncios. Subtitulado en espanol."),

    ("Dom 26 Jul", "UGC Video", C_UGC,
     "Real story: avoiding probate saved us months",
     "English-language client video. Family shares how having a trust in place "
     "meant zero court involvement when a parent passed. "
     "Focus on the emotional relief, not the legal details. "
     "Value: speaks directly to the fear of the unknown that most families have."),

    # PODCASTS
    ("Dom 5 Jul", "Podcast", C_POD,
     "Ep.1: Que pasa con tu herencia sin un plan",
     "Primer episodio. Tono conversacional, no academico. "
     "Escenario de apertura: 'Imaginemos que mañana algo te pasa. Quien se queda con tu casa? Tu auto? Tu negocio?' "
     "Recorre los escenarios mas comunes: sin testamento, con testamento pero sin trust, con trust mal hecho. "
     "Cierre con llamado a consulta gratuita. Duracion recomendada: 12-18 minutos."),

    ("Dom 19 Jul", "Podcast", C_POD,
     "Ep.2: Propiedades en Mexico y EE.UU.",
     "Tema muy relevante para la comunidad latina de Chula Vista. "
     "Que pasa con una propiedad en Mexico si el dueno vive en EE.UU. y fallece? "
     "Hay que hacer dos procesos sucesorios distintos? Se puede incluir en un trust americano? "
     "Entrevista o dialogo con preguntas reales que llegan al estudio. "
     "Valor: nadie habla de esto en espanol para esta comunidad especifica."),
]


def make_st(fname, fsize, color, align=TA_LEFT, leading=None, space_after=0, space_before=0):
    opts = dict(fontName=fname, fontSize=fsize, textColor=color,
                alignment=align, spaceAfter=space_after, spaceBefore=space_before)
    if leading:
        opts["leading"] = leading
    return ParagraphStyle("_", **opts)


def section_header(label, col):
    return Table(
        [[Paragraph(label, make_st("Helvetica-Bold", 10, WHITE, TA_LEFT))]],
        colWidths=[25*cm]
    )


def build_pdf():
    pw, ph = landscape(A4)
    doc = SimpleDocTemplate(OUT, pagesize=landscape(A4),
                            leftMargin=1.1*cm, rightMargin=1.1*cm,
                            topMargin=0.9*cm, bottomMargin=0.9*cm)
    elements = []

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 1: CALENDAR GRID
    # ────────────────────────────────────────────────────────────────────────
    title_st = make_st("Helvetica-Bold", 20, NAVY, space_after=2)
    sub_st   = make_st("Helvetica",       9, GRAY, space_after=2)
    ov_st    = make_st("Helvetica-Bold", 11, NAVY, leading=14, space_after=5)

    elements.append(Paragraph("CONTENT CALENDAR — MJ TRUST LAW", title_st))
    elements.append(Paragraph(
        f"{MONTH_LABEL} | Instagram | 4 posts/week + 3 stories/week | English &amp; Spanish",
        sub_st))
    elements.append(HRFlowable(width="100%", thickness=2.5, color=GOLD, spaceAfter=6))
    elements.append(Paragraph(f"{MONTH_LABEL} — OVERVIEW", ov_st))

    first_wd, num_days = cal.monthrange(YEAR, MONTH)
    avail_w  = pw - 2.2*cm
    col_w    = avail_w / 7
    col_widths = [col_w] * 7

    DAY_NAMES = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    hdr_st = make_st("Helvetica-Bold", 9, WHITE, TA_CENTER)
    header_row = [Paragraph(d, hdr_st) for d in DAY_NAMES]

    cells = [None] * first_wd + list(range(1, num_days + 1))
    while len(cells) % 7:
        cells.append(None)
    num_rows = len(cells) // 7

    date_st = make_st("Helvetica-Bold", 11, NAVY, leading=14, space_after=2)
    lbl_st  = make_st("Helvetica-Bold",  7, WHITE, leading=9, space_after=1)
    cont_st = make_st("Helvetica",        7, colors.HexColor("#333333"), leading=9, space_after=3)
    lang_es = make_st("Helvetica-Bold",   7, GOLD,  leading=9)
    lang_en = make_st("Helvetica-Bold",   7, colors.HexColor("#2980b9"), leading=9)

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
                lbl_tbl = Table([[Paragraph(label, lbl_st)]], colWidths=[col_w - 0.7*cm])
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

    # Legend
    elements.append(Spacer(1, 0.25*cm))
    legend = [
        ("Historia (Lun + Mie)",           C_HIST),
        ("Carrusel (Mar)",                  C_CARR),
        ("Mitos y Verdades (Jue)",          C_MITO),
        ("Podcast (Dom - semanas 1 y 3)",   C_POD),
        ("UGC Video (Dom - semanas 2 y 4)", C_UGC),
    ]
    leg_row = []
    for label, col in legend:
        p = Table([[Paragraph(label, make_st("Helvetica-Bold", 6.5, WHITE))]],
                  colWidths=[4.2*cm])
        p.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), col),
            ("TOPPADDING",    (0,0),(-1,-1), 3),
            ("BOTTOMPADDING", (0,0),(-1,-1), 3),
            ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ]))
        leg_row.append(p)
    leg_tbl = Table([leg_row], colWidths=[4.5*cm]*5)
    leg_tbl.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                                  ("LEFTPADDING",(0,0),(-1,-1),0),
                                  ("RIGHTPADDING",(0,0),(-1,-1),5)]))
    elements.append(leg_tbl)

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 2: CONTENT DETAIL
    # ────────────────────────────────────────────────────────────────────────
    elements.append(PageBreak())

    pg2_title = make_st("Helvetica-Bold", 18, NAVY, space_after=2)
    pg2_sub   = make_st("Helvetica",       9, GRAY, space_after=0)
    elements.append(Paragraph("DESARROLLO DE CONTENIDO — JULIO 2026", pg2_title))
    elements.append(Paragraph("Descripcion de cada post: que se publica, por que y como enfocarlo", pg2_sub))
    elements.append(HRFlowable(width="100%", thickness=2.5, color=GOLD, spaceAfter=10))

    # Group detail items by format
    groups = {
        "Historia": ("HISTORIAS",  C_HIST, []),
        "Carrusel": ("CARRUSELES", C_CARR, []),
        "Mito y Verdad": ("MITOS Y VERDADES", C_MITO, []),
        "UGC Video": ("UGC VIDEO", C_UGC, []),
        "Podcast":   ("PODCAST",   C_POD, []),
    }
    order = ["Historia", "Carrusel", "Mito y Verdad", "UGC Video", "Podcast"]
    for item in DETAIL:
        date_lbl, fmt, col, title, desc = item
        for key in groups:
            if fmt.startswith(key.split()[0]):
                groups[key][2].append(item)
                break

    # 2-column layout for detail
    avail_w2 = pw - 2.2*cm
    left_w  = 3.5*cm
    right_w = avail_w2 - left_w - 0.4*cm

    sec_hdr_st  = make_st("Helvetica-Bold", 9, WHITE, leading=12)
    date_lbl_st = make_st("Helvetica-Bold", 8, GRAY,  leading=11)
    card_ttl_st = make_st("Helvetica-Bold", 9, NAVY,  leading=12, space_after=2)
    card_dsc_st = make_st("Helvetica",      8, colors.HexColor("#444444"), leading=11)

    for key in order:
        label, col, items = groups[key]
        if not items:
            continue

        # Section header bar
        hdr_tbl = Table(
            [[Paragraph(label, sec_hdr_st)]],
            colWidths=[avail_w2]
        )
        hdr_tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), col),
            ("TOPPADDING",    (0,0),(-1,-1), 5),
            ("BOTTOMPADDING", (0,0),(-1,-1), 5),
            ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ]))
        elements.append(hdr_tbl)
        elements.append(Spacer(1, 0.1*cm))

        # Cards: 2 per row
        cards_per_row = 2
        card_w = (avail_w2 - (cards_per_row - 1) * 0.3*cm) / cards_per_row

        row_cards = []
        for i, (date_lbl, fmt, c, title, desc) in enumerate(items):
            card_inner = Table([
                [Paragraph(date_lbl.upper(), date_lbl_st)],
                [Paragraph(title, card_ttl_st)],
                [Paragraph(desc,  card_dsc_st)],
            ], colWidths=[card_w - 0.5*cm])
            card_inner.setStyle(TableStyle([
                ("VALIGN",        (0,0),(-1,-1), "TOP"),
                ("TOPPADDING",    (0,0),(-1,-1), 0),
                ("BOTTOMPADDING", (0,0),(-1,-1), 2),
                ("LEFTPADDING",   (0,0),(-1,-1), 0),
                ("RIGHTPADDING",  (0,0),(-1,-1), 0),
            ]))

            card = Table([[card_inner]], colWidths=[card_w])
            card.setStyle(TableStyle([
                ("BACKGROUND",    (0,0),(-1,-1), colors.HexColor("#fafafa")),
                ("BOX",           (0,0),(-1,-1), 0.5, colors.HexColor("#e0dbd4")),
                ("LEFTBORDER",    (0,0),(0,-1), 3, col),
                ("TOPPADDING",    (0,0),(-1,-1), 8),
                ("BOTTOMPADDING", (0,0),(-1,-1), 8),
                ("LEFTPADDING",   (0,0),(-1,-1), 8),
                ("RIGHTPADDING",  (0,0),(-1,-1), 8),
            ]))
            # accent left border via background trick
            accent = Table([[""],[""]], colWidths=[3], rowHeights=[None, None])
            accent.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),col)]))

            row_cards.append(card)
            if len(row_cards) == cards_per_row:
                row_tbl = Table([row_cards], colWidths=[card_w + 0.15*cm] * cards_per_row)
                row_tbl.setStyle(TableStyle([
                    ("VALIGN",      (0,0),(-1,-1), "TOP"),
                    ("LEFTPADDING", (0,0),(-1,-1), 0),
                    ("RIGHTPADDING",(0,0),(-1,-1), 3),
                ]))
                elements.append(row_tbl)
                elements.append(Spacer(1, 0.15*cm))
                row_cards = []

        if row_cards:
            # pad to full row
            while len(row_cards) < cards_per_row:
                row_cards.append("")
            row_tbl = Table([row_cards], colWidths=[card_w + 0.15*cm] * cards_per_row)
            row_tbl.setStyle(TableStyle([
                ("VALIGN",      (0,0),(-1,-1), "TOP"),
                ("LEFTPADDING", (0,0),(-1,-1), 0),
                ("RIGHTPADDING",(0,0),(-1,-1), 3),
            ]))
            elements.append(row_tbl)

        elements.append(Spacer(1, 0.25*cm))

    doc.build(elements)
    print(f"PDF generado: {OUT}")

build_pdf()
