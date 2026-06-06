from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import ParagraphStyle

NAVY     = colors.HexColor("#1a2e4a")
GOLD     = colors.HexColor("#C2801A")
CREAM    = colors.HexColor("#F0E8DC")
LAVENDER = colors.HexColor("#ece0f0")
LGRAY    = colors.HexColor("#f7f3ee")
GRAY     = colors.HexColor("#777777")
WHITE    = colors.white
RED      = colors.HexColor("#c0392b")
GREEN    = colors.HexColor("#1a7a4a")
PURP     = colors.HexColor("#6d3a7a")
BLUE     = colors.HexColor("#1a4a7a")
ORG      = colors.HexColor("#d35400")

FORMAT_COLORS = {
    "Carrusel":      colors.HexColor("#2e6da4"),
    "Reel":          colors.HexColor("#8e44ad"),
    "Post Estático": colors.HexColor("#27ae60"),
    "Podcast Clip":  colors.HexColor("#d35400"),
}
LANG_COLORS = {
    "ES":    GREEN,
    "EN":    BLUE,
    "ES/EN": PURP,
}
STORY_TYPE_COLORS = {
    "Oficina":   colors.HexColor("#1a7a4a"),
    "Review":    colors.HexColor("#c0392b"),
    "Educativa": colors.HexColor("#7d3c98"),
}
STORY_TYPE_LABELS = {
    "Oficina":   "Story: Oficina & Contacto",
    "Review":    "Story: Review de Cliente",
    "Educativa": "Story: Historia Educativa",
}


def build(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            leftMargin=0.6*inch, rightMargin=0.6*inch,
                            topMargin=0.6*inch, bottomMargin=0.6*inch)

    h1     = ParagraphStyle("h1",   fontSize=22, textColor=NAVY,  fontName="Helvetica-Bold",    spaceAfter=2,  leading=26)
    h2     = ParagraphStyle("h2",   fontSize=12, textColor=NAVY,  fontName="Helvetica-Bold",    spaceAfter=2,  leading=15)
    sub    = ParagraphStyle("sub",  fontSize=9,  textColor=GRAY,  fontName="Helvetica",          spaceAfter=4,  leading=12)
    body   = ParagraphStyle("body", fontSize=9.5,textColor=colors.black, fontName="Helvetica",  spaceAfter=3,  leading=13)
    bold   = ParagraphStyle("bold", fontSize=9.5,textColor=NAVY,  fontName="Helvetica-Bold",    spaceAfter=2,  leading=13)
    copy_s = ParagraphStyle("copy", fontSize=9,  textColor=colors.HexColor("#333333"),
                            fontName="Helvetica-Oblique", spaceAfter=2, leading=13, leftIndent=8)
    tag_s  = ParagraphStyle("tag",  fontSize=8,  textColor=WHITE, fontName="Helvetica-Bold",    leading=10)
    wk_s   = ParagraphStyle("wk",   fontSize=11, textColor=WHITE, fontName="Helvetica-Bold",    leading=14)
    cal_hdr= ParagraphStyle("calhdr",fontSize=8, textColor=WHITE, fontName="Helvetica-Bold",    leading=10, alignment=1)
    cal_day= ParagraphStyle("calday",fontSize=9, textColor=NAVY,  fontName="Helvetica-Bold",    leading=11, alignment=1)
    cal_emp= ParagraphStyle("calemp",fontSize=8, textColor=GRAY,  fontName="Helvetica",          leading=10, alignment=1)
    cal_ttl= ParagraphStyle("calttl",fontSize=7, textColor=NAVY,  fontName="Helvetica",          leading=9,  alignment=1)
    cal_sp = ParagraphStyle("calsp", fontSize=6.5,textColor=RED,  fontName="Helvetica-Bold",    leading=9,  alignment=1)

    def sec_hdr(text, bg=NAVY):
        t = Table([[Paragraph(text, wk_s)]], colWidths=[doc.width])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),bg),
            ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
            ("LEFTPADDING",(0,0),(-1,-1),10),
        ]))
        return t

    def tag(label, color, width=1.2*inch):
        t = Table([[Paragraph(label, tag_s)]], colWidths=[width])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),color),
            ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
            ("LEFTPADDING",(0,0),(-1,-1),6),
        ]))
        return t

    # ── POST DATA ─────────────────────────────────────────────────
    POST_DAYS = {
        1:  ("Contrast Hook",          "Post Estático", "ES"),
        3:  ("Caso: Cuenta olvidada",  "Carrusel",      "ES"),
        5:  ("Reel: ¿Qué es un trust?","Reel",          "ES"),
        7:  ("Mito #1: El testamento", "Carrusel",      "EN"),
        8:  ("Contrast Hook #2",       "Post Estático", "ES"),
        10: ("Caso: Bienes en 2 países","Carrusel",     "ES"),
        12: ("Podcast Clip #1",        "Podcast Clip",  "ES/EN"),
        14: ("3 activos sin testamento","Post Estático","EN"),
        15: ("Reel: 3 errores comunes","Reel",          "ES"),
        17: ("Mito #2: Solo para ricos","Carrusel",     "ES"),
        19: ("Immigrant Heritage Month","Post Estático","ES/EN"),
        21: ("Father's Day Reel",      "Reel",          "ES"),
        22: ("Contrast Hook #3",       "Post Estático", "ES"),
        24: ("Podcast Clip #2",        "Podcast Clip",  "ES"),
        26: ("Caso: Dueño de negocio", "Carrusel",      "EN"),
        28: ("Reel CTA: Consulta gratis","Reel",        "ES"),
    }
    SPECIAL = {19: "Juneteenth", 21: "Father's Day"}

    # ── STORY DATA ────────────────────────────────────────────────
    # 3 stories/week: Oficina (Mon), Review (Wed/Tue), Educativa (Fri/Thu)
    STORY_DAYS = {
        1:  ("Oficina",   "ES"),   # Mon W1
        3:  ("Review",    "ES"),   # Wed W1
        5:  ("Educativa", "ES"),   # Fri W1
        8:  ("Oficina",   "ES"),   # Mon W2
        10: ("Review",    "ES"),   # Wed W2
        11: ("Educativa", "ES"),   # Thu W2 (story-only)
        15: ("Oficina",   "ES"),   # Mon W3
        16: ("Review",    "ES"),   # Tue W3 (story-only)
        18: ("Educativa", "ES"),   # Thu W3 (story-only)
        22: ("Oficina",   "ES"),   # Mon W4
        24: ("Review",    "ES"),   # Wed W4
        26: ("Educativa", "ES"),   # Fri W4
    }
    story_only_days = [d for d in STORY_DAYS if d not in POST_DAYS]

    # ── CALENDAR GRID ──────────────────────────────────────────────
    days_row   = ["MON","TUE","WED","THU","FRI","SAT","SUN"]
    cal_col_w  = doc.width / 7
    cal_rows   = [[Paragraph(d, cal_hdr) for d in days_row]]
    week       = [None]*7

    for day in range(1, 31):
        dow     = (day - 1) % 7
        week[dow] = day
        if dow == 6 or day == 30:
            row = []
            for i in range(7):
                d = week[i]
                if d is None:
                    row.append(Paragraph("", cal_emp))
                elif d in POST_DAYS:
                    title, fmt, lang = POST_DAYS[d]
                    fc = FORMAT_COLORS.get(fmt, NAVY)
                    cell = [
                        Paragraph(str(d), cal_day),
                        Paragraph(title, cal_ttl),
                        Paragraph(fmt, ParagraphStyle("cf", fontSize=6.5, textColor=fc,
                                  fontName="Helvetica-Bold", leading=8, alignment=1)),
                    ]
                    if d in SPECIAL:
                        cell.append(Paragraph(SPECIAL[d], cal_sp))
                    if d in STORY_DAYS:
                        stype = STORY_DAYS[d][0]
                        sc    = STORY_TYPE_COLORS.get(stype, PURP)
                        cell.append(Paragraph(
                            "Story: " + stype,
                            ParagraphStyle("calsty", fontSize=6.5, textColor=sc,
                                           fontName="Helvetica-Bold", leading=9, alignment=1)
                        ))
                    row.append(cell)
                elif d in STORY_DAYS:
                    stype = STORY_DAYS[d][0]
                    sc    = STORY_TYPE_COLORS.get(stype, PURP)
                    row.append([
                        Paragraph(str(d), cal_day),
                        Paragraph(STORY_TYPE_LABELS[stype],
                                  ParagraphStyle("calsty2", fontSize=6.5, textColor=sc,
                                                 fontName="Helvetica-Bold", leading=8, alignment=1)),
                    ])
                else:
                    row.append(Paragraph(str(d), cal_emp))
            cal_rows.append(row)
            week = [None]*7

    cal_table = Table(cal_rows, colWidths=[cal_col_w]*7,
                      rowHeights=[0.28*inch] + [0.75*inch]*5)
    cal_style = TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),
        ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#cccccc")),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),4),
        ("RIGHTPADDING",(0,0),(-1,-1),4),
    ])
    for day in POST_DAYS:
        dow     = (day - 1) % 7
        row_idx = (day - 1) // 7 + 1
        cal_style.add("BACKGROUND",(dow,row_idx),(dow,row_idx),CREAM)
    for day in STORY_DAYS:  # all 12 story days get lavender, overrides CREAM on shared days
        dow     = (day - 1) % 7
        row_idx = (day - 1) // 7 + 1
        cal_style.add("BACKGROUND",(dow,row_idx),(dow,row_idx),LAVENDER)
    cal_table.setStyle(cal_style)

    STORY_TYPE_DESC = {
        "Oficina":   "Recordatorio semanal con ubicación, horarios y vías de contacto. Pin de ubicación animado, foto de la oficina o de la abogada. Sticker de link. Fondo crema, texto navy.",
        "Review":    "Historia mostrando una reseña de cliente. Quote en tipografía grande, estrellas doradas en la parte superior. Sin foto del cliente. Fondo crema cálido.",
        "Educativa": "Historia educativa semanal. El formato rota cada semana: quick fact de probate / encuesta interactiva / BTS de la consulta gratuita / pregunta frecuente respondida.",
    }

    # ── BLOCK BUILDERS ─────────────────────────────────────────────
    def post_block(date, title, format_type, lang, objective, why_format, visual, copy_lines, special=None):
        elems = []
        hdr_cells = [
            Paragraph(f"<b>{date}</b>", ParagraphStyle("d", fontSize=9, textColor=GRAY,
                      fontName="Helvetica-Bold", leading=12)),
            tag(format_type, FORMAT_COLORS.get(format_type, NAVY)),
            tag(lang, LANG_COLORS.get(lang, NAVY), 0.7*inch),
        ]
        if special:
            hdr_cells.append(tag(special, RED, 1.6*inch))
        hdr_t = Table([hdr_cells],
                      colWidths=[1.4*inch,1.3*inch,0.7*inch]+([1.6*inch] if special else []))
        hdr_t.setStyle(TableStyle([
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),6),
            ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ]))
        block = [hdr_t, Paragraph(title, h2)]
        for lbl, val in [("Objetivo", objective), ("Por qué este formato", why_format), ("Visual", visual)]:
            block.append(Paragraph(lbl, bold))
            block.append(Paragraph(val, body))
        block.append(HRFlowable(width="100%", thickness=0.5,
                     color=colors.HexColor("#dddddd"), spaceAfter=10, spaceBefore=6))
        elems.append(KeepTogether(block[:4]))
        elems += block[4:]
        return elems

    def story_block(date, story_type, title, lang, lines):
        elems = []
        st_color   = STORY_TYPE_COLORS.get(story_type, PURP)
        label_text = STORY_TYPE_LABELS.get(story_type, story_type)
        hdr_cells  = [
            Paragraph(f"<b>{date}</b>", ParagraphStyle("d", fontSize=9, textColor=GRAY,
                      fontName="Helvetica-Bold", leading=12)),
            tag(label_text, st_color, 1.7*inch),
            tag(lang, LANG_COLORS.get(lang, NAVY), 0.7*inch),
        ]
        hdr_t = Table([hdr_cells], colWidths=[1.4*inch, 1.7*inch, 0.7*inch])
        hdr_t.setStyle(TableStyle([
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),6),
            ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ]))
        desc = STORY_TYPE_DESC.get(story_type, "")
        block = [hdr_t, Paragraph(title, h2), Paragraph("Descripción", bold), Paragraph(desc, body)]
        block.append(HRFlowable(width="100%", thickness=0.5,
                     color=colors.HexColor("#e0d0f0"), spaceAfter=10, spaceBefore=6))
        elems.append(KeepTogether(block[:4]))
        elems += block[4:]
        return elems

    story = []

    # ── TITLE ──────────────────────────────────────────────────────
    story.append(Paragraph("CONTENT CALENDAR — MJ TRUST LAW", h1))
    story.append(Paragraph(
        "June 2026  |  Instagram  |  4 posts/week  +  3 stories/week  |  English & Spanish", sub))
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=10, spaceBefore=4))

    # ── CALENDAR VIEW ──────────────────────────────────────────────
    story.append(Paragraph("JUNE 2026 — OVERVIEW", ParagraphStyle("ov", fontSize=11,
                 textColor=NAVY, fontName="Helvetica-Bold", spaceAfter=6, leading=14)))
    story.append(cal_table)
    story.append(Spacer(1, 6))

    # Legend — feed formats
    legend_items = [[
        tag("Carrusel",      FORMAT_COLORS["Carrusel"],      1.0*inch),
        tag("Reel",          FORMAT_COLORS["Reel"],          0.75*inch),
        tag("Post Estático", FORMAT_COLORS["Post Estático"], 1.1*inch),
        tag("Podcast Clip",  FORMAT_COLORS["Podcast Clip"],  1.1*inch),
        tag("ES",            LANG_COLORS["ES"],              0.5*inch),
        tag("EN",            LANG_COLORS["EN"],              0.5*inch),
        tag("ES/EN",         LANG_COLORS["ES/EN"],           0.65*inch),
    ]]
    leg_t = Table(legend_items, colWidths=[1.0*inch,0.75*inch,1.1*inch,1.1*inch,0.5*inch,0.5*inch,0.65*inch])
    leg_t.setStyle(TableStyle([
        ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),4),
        ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),2),
    ]))
    story.append(leg_t)
    story.append(Spacer(1, 4))

    # Legend — story types
    story_legend_items = [[
        tag("Story: Oficina & Contacto", STORY_TYPE_COLORS["Oficina"],   1.9*inch),
        tag("Story: Review de Cliente",  STORY_TYPE_COLORS["Review"],    1.9*inch),
        tag("Story: Historia Educativa", STORY_TYPE_COLORS["Educativa"], 1.9*inch),
        Paragraph("Fondo lavanda = día con Story (con o sin post de feed) — 12 stories en total", ParagraphStyle(
            "ln", fontSize=7.5, textColor=GRAY, fontName="Helvetica-Oblique", leading=10)),
    ]]
    story_leg_t = Table(story_legend_items, colWidths=[1.9*inch, 1.9*inch, 1.9*inch, 2.5*inch])
    story_leg_t.setStyle(TableStyle([
        ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),4),
        ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    story.append(story_leg_t)
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=14))

    # ════════════════════════════════════════════════════════════════
    # FEED POSTS
    # ════════════════════════════════════════════════════════════════

    # ── WEEK 1 ─────────────────────────────────────────────────────
    story.append(sec_hdr("WEEK 1  —  June 1–7"))
    story.append(Spacer(1, 8))

    story += post_block(
        "Lunes 1 de junio",
        "\"Protegés tu contraseña. ¿Y tu herencia?\"",
        "Post Estático", "ES",
        "Parar el scroll con un contraste inmediato. Generar conciencia sin necesidad de que el usuario conozca el tema.",
        "El post estático con texto grande es el formato más efectivo para un contrast hook. Se lee en 2 segundos y genera saves.",
        "Fondo crema. Dos listas en columnas: izquierda 'LO QUE PROTEGÉS' (contraseña, auto, salud), derecha 'LO QUE OLVIDASTE' (herencia, casa, familia). Tipografía bold navy. Acento dorado.",
        [
            "Protegés tu contraseña. ✓",
            "Tenés seguro de auto. ✓",
            "Guardás todos tus papeles importantes. ✓",
            "¿Tu familia sabe qué pasa con tu casa en Chula Vista si algo te ocurre? ✗",
            "El estate planning no es para cuando seas viejo. Es para ahora.",
            "Primera consulta gratuita. Link en bio 👇",
            "#EstatePlanning #TrustLaw #ChulaVista #SanDiego #FamiliasLatinas #MJTrustLaw",
        ]
    )

    story += post_block(
        "Miércoles 3 de junio",
        "Caso: La cuenta que rompió el trust perfecto",
        "Carrusel", "ES",
        "Mostrar con un ejemplo concreto cómo un error pequeño puede tener consecuencias grandes. Generar urgencia sin alarmar.",
        "El carrusel construye tensión slide a slide — el lector hace swipe para saber qué pasó. Ideal para casos que necesitan contexto.",
        "6 slides. Fondo crema/navy alternado. Slide 1 hook fuerte. Slide 6 CTA. Números de slide visibles. Paleta MJ Trust Law.",
        [
            "Slide 1: Tenías un trust perfecto. Tu casa en Chula Vista adentro. Tus beneficiarios nombrados. Todo en orden. Hasta que olvidaste una cosa.",
            "Slide 2: Una cuenta bancaria de $500. A tu nombre. Fuera del trust.",
            "Slide 3: Esa cuenta sola, bajo las reglas de California, no hubiera necesitado probate. Pero abrió la puerta.",
            "Slide 4: En California, los honorarios de probate se calculan sobre el valor BRUTO del estate. No solo los $500.",
            "Slide 5: En una propiedad de $750,000 en Chula Vista, eso puede significar más de $45,000 en costos que tu familia no tenía que pagar.",
            "Slide 6: Una cuenta pequeña no es el problema. Es lo que revela. ¿Tu trust está completo? Hablemos. Primera consulta gratuita 👇",
            "#TrustPlanning #Probate #California #ChulaVista #EstatePlanning #MJTrustLaw",
        ]
    )

    story += post_block(
        "Viernes 5 de junio",
        "Reel: ¿Qué es un trust y por qué tu familia lo necesita?",
        "Reel", "ES",
        "Educar a audiencia nueva en el concepto básico. Posicionar a la abogada como figura de confianza.",
        "La abogada a cámara genera conexión personal. Para audiencia latina, ver quién las asesora es parte de la decisión.",
        "Abogada a cámara, buena iluminación. Subtítulos en español. 45-60 segundos. Fondo de oficina profesional o exterior de Chula Vista.",
        [
            "Un trust no es solo para millonarios.",
            "Si tenés una casa en San Diego, tenés un estate. Y en California, sin un trust, tu familia puede terminar en probate court.",
            "En este video te explico qué es un trust, cómo funciona y por qué es la herramienta más importante para proteger lo que construiste.",
            "¿Tenés preguntas? Escribime por DM o agendá una consulta gratuita en el link de la bio 👇",
            "#Trust #EstatePlanning #AbogadaLatina #ChulaVista #California #MJTrustLaw",
        ]
    )

    story += post_block(
        "Domingo 7 de junio",
        "Mito #1: \"Con testamento es suficiente\"",
        "Carrusel", "EN",
        "Desmentir la misconception más común. Llegar a audiencia bilingüe que cree que ya tiene todo resuelto.",
        "Carrusel para desarrollar el argumento con datos. En inglés para ampliar alcance en Instagram.",
        "5 slides. Slide 1: 'MYTH' en rojo grande. Slides 2-4: argumento con datos de California. Slide 5: CTA.",
        [
            "Slide 1: MYTH: \"If I have a will, my family is protected.\"",
            "Slide 2: A will still goes through probate court in California. That means months of legal process — and public records anyone can access.",
            "Slide 3: A trust transfers your assets directly to your family. No court. No delays. No unnecessary fees.",
            "Slide 4: For a home worth $700,000 in Chula Vista, probate fees can reach $42,000. A trust can eliminate that entirely.",
            "Slide 5: The difference between a will and a trust is not just paperwork. It's what your family goes through when you're gone. Let's talk. Free consultation at the link in bio.",
            "#EstatePlanningMyths #WillVsTrust #CaliforniaLaw #ChulaVista #MJTrustLaw",
        ]
    )

    story.append(Spacer(1, 4))

    # ── WEEK 2 ─────────────────────────────────────────────────────
    story.append(sec_hdr("WEEK 2  —  June 8–14"))
    story.append(Spacer(1, 8))

    story += post_block(
        "Lunes 8 de junio",
        "\"Tenés seguro de auto pero no un trust\"",
        "Post Estático", "ES",
        "Segundo contrast hook del mes. Mantener el formato de alto engagement con un ángulo diferente.",
        "Post estático con lista visual. Fácil de guardar y compartir. Genera conversación en comentarios.",
        "Dos columnas. Izquierda: 'LO QUE PROTEGÉS' con lista. Derecha: 'LO QUE LE FALTA A TU FAMILIA' con lista. Fondo crema, acento navy/gold.",
        [
            "Tenés seguro de auto. ✓",
            "Tenés seguro médico. ✓",
            "Tenés seguro de hogar para tu casa en San Diego. ✓",
            "¿Tenés un plan legal para que tu familia no pierda todo eso si algo te pasa? ✗",
            "El estate planning es el seguro que nadie te habla pero que más importa.",
            "Consultá gratis. Link en bio 👇",
            "#FamiliaProtegida #TrustLaw #EstatePlanning #SanDiego #ChulaVista #MJTrustLaw",
        ]
    )

    story += post_block(
        "Miércoles 10 de junio",
        "Caso: Bienes en México y en California",
        "Carrusel", "ES",
        "Hablar directamente al cliente inmigrante con propiedades en dos países — el perfil exacto de su audiencia en Chula Vista.",
        "Caso hipotético sin nombre — el lector se proyecta en la situación. Carrusel para desarrollar la complejidad del tema.",
        "6 slides. Slide 1 impacto: 'Tenés una casa en Chula Vista y algo en México. ¿Sabés qué pasa con todo eso si faltás?'. Slide final CTA.",
        [
            "Slide 1: Tenés una casa en Chula Vista. Y una propiedad en Tijuana que heredaste de tus padres. ¿Sabés qué pasa con todo eso si algo te ocurre?",
            "Slide 2: Sin un plan, tu familia enfrenta dos sistemas legales distintos al mismo tiempo. California por un lado. México por el otro.",
            "Slide 3: Dos procesos. Dos tribunales. Dos sets de honorarios. Lo que podría resolverse en meses puede tardar años.",
            "Slide 4: Y mientras tanto, ¿quién vive en la casa? ¿Quién paga los impuestos? ¿Quién toma las decisiones?",
            "Slide 5: Un estate plan binacional no es más caro. Es más inteligente. Y en la frontera San Diego-Tijuana, es más necesario que en cualquier otro lugar.",
            "Slide 6: En MJ Trust Law entendemos tu historia porque es la historia de nuestras familias también. Hablemos. Consulta gratuita 👇",
            "#FamiliasInmigrantes #BienesBinacionales #TijuanaSanDiego #ChulaVista #EstatePlanning #MJTrustLaw",
        ]
    )

    story += post_block(
        "Viernes 12 de junio",
        "Podcast Clip: [Momento más impactante del episodio]",
        "Podcast Clip", "ES/EN",
        "Aprovechar contenido existente de alto valor. Prueba social — alguien más invitó a la abogada a hablar.",
        "Los clips de podcast generan autoridad inmediata. Cero producción adicional sobre contenido que ya existe.",
        "Video vertical 9:16. Subtítulos grandes en español. 30-45 segundos. Highlight del momento más sorprendente o emotivo del episodio.",
        [
            "Cuando me preguntaron en el podcast cuál es el error más común que cometen las familias de San Diego con su estate plan, la respuesta fue una sola.",
            "Mirá el clip. 👆",
            "Si esto te resuena, el link para tu consulta gratuita está en la bio.",
            "#Podcast #EstatePlanning #AbogadaLatina #SanDiego #MJTrustLaw",
        ]
    )

    story += post_block(
        "Domingo 14 de junio",
        "3 activos que NO pasan por tu testamento",
        "Post Estático", "EN",
        "Contenido educativo de alto valor. Genera saves masivos — las personas guardan esto para releerlo.",
        "Lista numerada en post estático — fácil de leer, fácil de guardar. En inglés para mayor alcance.",
        "Fondo navy. Texto blanco y dorado. Título grande: '3 ASSETS THAT DON'T PASS THROUGH YOUR WILL'. Lista numerada con íconos.",
        [
            "Most people don't know this — and it changes everything:",
            "1. Life insurance proceeds go directly to your named beneficiary. Your will doesn't touch them.",
            "2. Retirement accounts (401k, IRA) — beneficiary designation overrides your will entirely.",
            "3. Joint tenancy property passes automatically to the surviving owner.",
            "This means a big part of your estate may go somewhere you didn't intend — without you knowing.",
            "Estate planning isn't just a document. It's a complete strategy. Free consultation at the link in bio. 🔗",
            "#EstatePlanning #Will #TrustPlanning #CaliforniaLaw #MJTrustLaw",
        ]
    )

    story.append(Spacer(1, 4))

    # ── WEEK 3 ─────────────────────────────────────────────────────
    story.append(sec_hdr("WEEK 3  —  June 15–21  |  Immigrant Heritage Month  |  Father's Day"))
    story.append(Spacer(1, 8))

    story += post_block(
        "Lunes 15 de junio",
        "Reel: 3 errores comunes en estate planning",
        "Reel", "ES",
        "Educación rápida y accionable. Alto potencial de shares — la gente manda esto a familiares.",
        "Formato de lista en video es altamente compartible. La abogada a cámara refuerza que esto viene de experiencia real.",
        "Abogada a cámara. Texto en pantalla con cada error mientras habla. Subtítulos. 60 segundos máximo.",
        [
            "Estos son los 3 errores que veo repetirse en las familias de Chula Vista y San Diego que vienen a verme.",
            "El primero es el más común. El tercero es el más caro.",
            "Si querés saber si tu plan tiene alguno de estos problemas, el link para una revisión gratuita está en la bio 👇",
            "#EstatePlanning #TrustPlanning #Probate #AbogadaLatina #ChulaVista #MJTrustLaw",
        ]
    )

    story += post_block(
        "Miércoles 17 de junio",
        "Mito #2: \"El estate planning es solo para ricos\"",
        "Carrusel", "ES",
        "Eliminar la barrera de entrada más grande. La audiencia latina clase media no se identifica como 'cliente de estate planning'.",
        "Carrusel para desmantelar el mito con datos reales de San Diego. El precio del mercado inmobiliario local hace el argumento solo.",
        "5 slides. Slide 1: 'MITO' en rojo. Datos reales de precios en Chula Vista/San Diego. Slide final: CTA accesible.",
        [
            "Slide 1: MITO: El estate planning es solo para millonarios.",
            "Slide 2: Si tenés una casa en Chula Vista, tenés un estate. El valor promedio de una propiedad en el área supera los $700,000.",
            "Slide 3: Sin un trust, tu familia puede enfrentar honorarios de probate de hasta el 5% del valor bruto. En una casa de $700,000 eso son $35,000.",
            "Slide 4: Un trust bien estructurado puede eliminar ese costo por completo — y proteger a tu familia de meses de proceso legal.",
            "Slide 5: El estate planning no es un lujo. Es la decisión financiera más inteligente para cualquier familia con una casa en California. Hablemos. Link en bio 👇",
            "#EstatePlanningParaTodos #TrustLaw #ChulaVista #FamiliasLatinas #California #MJTrustLaw",
        ]
    )

    story += post_block(
        "Viernes 19 de junio",
        "Immigrant Heritage Month: Familias con raíces en dos países",
        "Post Estático", "ES/EN",
        "Conexión emocional y cultural con la audiencia inmigrante. El post más personal del mes.",
        "Post estático emocional — el texto bilingüe refleja la identidad dual de sus clientes. Simple, directo, poderoso.",
        "Fondo crema cálido. Texto en español e inglés, intercalado. Tipografía elegante. Sin imágenes complejas — las palabras son el diseño.",
        [
            "Construiste una vida entre dos países.",
            "Cruzaste una frontera para darle más a tu familia.",
            "Trabajaste para tener una casa. Para dejar algo.",
            "You built something worth protecting.",
            "Protecting it requires a plan that understands your story — not just your assets.",
            "At MJ Trust Law, we do. 🔗 Free consultation. Link in bio.",
            "#ImmigrantHeritageMonth #FamiliasLatinas #SanDiego #ChulaVista #EstatePlanning #MJTrustLaw",
        ],
        special="Immigrant Heritage Month"
    )

    story += post_block(
        "Domingo 21 de junio",
        "Father's Day: El mejor regalo que le podés dejar a tu familia",
        "Reel", "ES",
        "Máxima conexión emocional del mes. Estate planning como acto de amor paternal.",
        "Reel emotivo de la abogada en el día de mayor sensibilidad familiar. El tono personal genera compartidos masivos.",
        "Abogada a cámara. Tono cálido, íntimo. Puede estar sentada, ropa más casual. Iluminación suave. 45-60 segundos.",
        [
            "Hoy, el día del padre, quiero hablarle a todos los que están construyendo algo para sus hijos.",
            "El mejor regalo que le podés dejar a tu familia no se compra.",
            "Es saber que si algo te pasa, ellos van a estar protegidos. Sin cortes. Sin deudas. Sin años en tribunales.",
            "Eso es lo que un trust le da a tu familia.",
            "Si querés empezar, el primer paso es una conversación. Y es gratis. Link en bio 👇",
            "Feliz día del padre. 🤍",
            "#DiaDelPadre #FathersDay #EstatePlanning #TrustLaw #FamiliasLatinas #ChulaVista #MJTrustLaw",
        ],
        special="Father's Day 🤍"
    )

    story.append(Spacer(1, 4))

    # ── WEEK 4 ─────────────────────────────────────────────────────
    story.append(sec_hdr("WEEK 4  —  June 22–28"))
    story.append(Spacer(1, 8))

    story += post_block(
        "Lunes 22 de junio",
        "\"Guardás los recibos del súper pero no tenés un trust\"",
        "Post Estático", "ES",
        "Tercer contrast hook del mes. Mantener el formato con humor sutil — romper la procrastinación.",
        "Post estático de impacto rápido. El humor leve aumenta los shares y comentarios.",
        "Texto grande centrado. Fondo crema. Bold navy. Estructura de lista con checkmarks y X.",
        [
            "Guardás los recibos del súper por si acaso. ✓",
            "Tenés una carpeta con todos los papeles del auto. ✓",
            "Recordás la contraseña de una cuenta que no usás hace 3 años. ✓",
            "¿Tenés un trust para proteger tu casa en San Diego? ✗",
            "No hace falta esperar el momento perfecto. Hace falta empezar.",
            "Consultá gratis. Link en bio 👇",
            "#EstatePlanning #TrustLaw #Procrastinacion #ChulaVista #MJTrustLaw",
        ]
    )

    story += post_block(
        "Miércoles 24 de junio",
        "Podcast Clip #2: [Dato o momento sorprendente]",
        "Podcast Clip", "ES",
        "Segundo clip del mes — refuerza presencia de la abogada como thought leader con prueba social externa.",
        "Reutilizar contenido existente de alto valor. Posiciona a la abogada por encima de la competencia local.",
        "Video vertical 9:16. Subtítulos grandes. El clip debe tener un insight práctico o estadística que sorprenda.",
        [
            "Esto es lo que les digo a las familias de Chula Vista que vienen sin ningún plan:",
            "[cita del podcast]",
            "Si querés escuchar el episodio completo, el link está en mi bio.",
            "Y si querés que hablemos de tu situación, la primera consulta es gratis 👇",
            "#Podcast #TrustLaw #EstatePlanning #AbogadaLatina #MJTrustLaw",
        ]
    )

    story += post_block(
        "Viernes 26 de junio",
        "Caso: El dueño de negocio que esperó demasiado",
        "Carrusel", "EN",
        "Llegar a pequeños empresarios latinos de San Diego — segmento con alta necesidad y bajo awareness del tema.",
        "Caso hipotético en inglés para llegar a business owners bilingües. Carrusel para desarrollar las consecuencias en detalle.",
        "6 slides. Fondo navy en slides de impacto, crema en slides de datos. Slide 1 hook fuerte sin nombre.",
        [
            "Slide 1: You have a business in San Diego. A home. A retirement account. Your estate plan? \"I'll take care of it next year.\"",
            "Slide 2: Then something unexpected happens. No trust. No succession plan. No instructions.",
            "Slide 3: Your family has to go through probate for the home. And your business? It can't operate while your estate sits in court.",
            "Slide 4: Your employees don't know what happens. Your clients don't know who to call. What you spent years building starts to unravel.",
            "Slide 5: Business owners need estate planning more than anyone. Your business IS your estate.",
            "Slide 6: Don't wait for next year. It never comes. Free consultation at the link in bio.",
            "#BusinessOwner #EstatePlanning #TrustLaw #SanDiego #SmallBusiness #MJTrustLaw",
        ]
    )

    story += post_block(
        "Domingo 28 de junio",
        "Reel CTA: La consulta es gratis. ¿Qué esperás?",
        "Reel", "ES",
        "Cerrar el mes convirtiendo audiencia que ya siguió el contenido. La consulta gratuita elimina la última barrera.",
        "Reel directo de la abogada con tono cercano. El mes de contenido ya construyó la confianza — este post cierra.",
        "Abogada a cámara, tono amigable y sin presión. Puede responder las 3 preguntas más frecuentes que recibe. 45-60 seg.",
        [
            "La pregunta que más me hacen es: ¿por dónde empiezo?",
            "La respuesta siempre es la misma: con una conversación.",
            "No necesitás saber nada de leyes. No necesitás tener todo claro.",
            "Solo necesitás querer proteger a tu familia.",
            "Atiendo familias en Chula Vista, San Diego y toda el área. Y la primera consulta es gratis y sin compromiso.",
            "El link para agendar está en mi bio. Te espero 👇",
            "#ConsultaGratis #EstatePlanning #TrustLaw #AbogadaLatina #ChulaVista #SanDiego #MJTrustLaw",
        ]
    )

    # ════════════════════════════════════════════════════════════════
    # INSTAGRAM STORIES
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=GOLD, spaceAfter=14, spaceBefore=4))
    story.append(sec_hdr("INSTAGRAM STORIES — JUNE 2026", PURP))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "3 stories por semana: Oficina & Contacto (lunes) · Review de Cliente (miércoles/martes) · Historia Educativa (viernes/jueves)",
        ParagraphStyle("stsubb", fontSize=9, textColor=PURP, fontName="Helvetica-Oblique",
                       spaceAfter=10, leading=12)))

    # ── STORIES WEEK 1 ─────────────────────────────────────────────
    story.append(sec_hdr("STORIES — WEEK 1  (June 1–7)", colors.HexColor("#7d3c98")))
    story.append(Spacer(1, 8))

    story += story_block(
        "Lunes 1 de junio",
        "Oficina",
        "Así nos encontrás esta semana",
        "ES",
        [
            "📍 Chula Vista, CA — atendemos toda el área de San Diego",
            "🕐 Lunes a viernes, 9am a 6pm",
            "💻 Consultas en persona o por videollamada — sin moverse de tu casa",
            "Primera consulta: GRATUITA y sin compromiso",
            "👇 Agendá en el link de la bio",
            "Tip de diseño: pin de ubicación animado, foto de la oficina o de la abogada. Fondo crema, texto navy. Sticker de link.",
        ]
    )

    story += story_block(
        "Miércoles 3 de junio",
        "Review",
        "Lo que dicen nuestras clientes",
        "ES",
        [
            "★★★★★",
            "'No entendía nada sobre trusts y me daba vergüenza preguntar. La abogada me explicó todo en español, sin apurarme, hasta que me fui con todo claro. Hoy tengo un plan de estate planning completo para mi familia.'",
            "Cliente, Chula Vista",
            "",
            "¿Conocés a alguien que necesite escuchar esto? Compartí esta historia 👇",
            "Tip de diseño: fondo crema cálido, tipografía grande para la quote, estrellas doradas en la parte superior. Sin foto del cliente.",
        ]
    )

    story += story_block(
        "Viernes 5 de junio",
        "Educativa",
        "Quick Fact: ¿Cuánto cuesta el probate en California?",
        "ES",
        [
            "En California, los honorarios de probate se calculan sobre el valor BRUTO del estate.",
            "Casa en Chula Vista valorada en $750,000:",
            "Honorarios de probate: hasta $46,000",
            "Con un trust: $0",
            "¿Tu familia debería pagar eso?",
            "Primera consulta gratuita. DM o link en bio 👇",
            "Tip de diseño: slide tipo infographic. Número grande '$46,000' en rojo. Texto bold. Paleta navy y crema.",
        ]
    )

    # ── STORIES WEEK 2 ─────────────────────────────────────────────
    story.append(sec_hdr("STORIES — WEEK 2  (June 8–14)", colors.HexColor("#7d3c98")))
    story.append(Spacer(1, 8))

    story += story_block(
        "Lunes 8 de junio",
        "Oficina",
        "¿Cuándo es el mejor momento para empezar tu estate plan?",
        "ES",
        [
            "La respuesta es siempre la misma: antes de necesitarlo.",
            "Esta semana tenemos disponibilidad para consultas en Chula Vista y por videollamada.",
            "📍 Chula Vista, CA",
            "🕐 Lunes a viernes, 9am a 6pm",
            "Primera consulta: GRATUITA",
            "Agendá en el link de la bio 👇",
            "Tip de diseño: fondo crema. Texto en dos bloques. Ícono de calendario o reloj como elemento decorativo.",
        ]
    )

    story += story_block(
        "Miércoles 10 de junio",
        "Review",
        "De boca de nuestros clientes",
        "ES",
        [
            "★★★★★",
            "'Tenía una casa en San Diego y una propiedad en México que heredé de mis padres. No sabía que podía planear los dos al mismo tiempo. MJ Trust Law me ayudó a estructurar todo sin complicaciones.'",
            "Cliente, San Diego",
            "",
            "Si tenés bienes en dos países, hay un plan para vos. Link en bio 👇",
            "Tip de diseño: igual que review anterior. Consistencia visual semana a semana genera reconocimiento de marca.",
        ]
    )

    story += story_block(
        "Jueves 11 de junio",
        "Educativa",
        "Encuesta: ¿Ya tenés un plan de estate planning?",
        "ES",
        [
            "Pregunta del día:",
            "[Poll: Sí, tengo un trust / Tengo testamento / Todavía no]",
            "",
            "No importa tu respuesta — siempre hay un próximo paso.",
            "Si elegiste 'Todavía no': DM para hablar sin compromiso 👇",
            "Tip de diseño: usar la función de encuesta nativa de Instagram Stories. Fondo navy o crema según marca. El resultado de la encuesta se puede resharedear al día siguiente como segundo slide.",
        ]
    )

    # ── STORIES WEEK 3 ─────────────────────────────────────────────
    story.append(sec_hdr("STORIES — WEEK 3  (June 15–21)", colors.HexColor("#7d3c98")))
    story.append(Spacer(1, 8))

    story += story_block(
        "Lunes 15 de junio",
        "Oficina",
        "Immigrant Heritage Month: Estamos aquí para vos",
        "ES",
        [
            "Este mes celebramos a las familias que construyeron algo nuevo en este país.",
            "En MJ Trust Law atendemos familias inmigrantes que quieren proteger lo que trabajaron para tener.",
            "📍 Chula Vista, CA — a minutos de la frontera",
            "🕐 Lunes a viernes, 9am a 6pm",
            "Hablamos español. Primera consulta gratis.",
            "Link en bio 👇",
            "Tip de diseño: tono más cálido y emocional esta semana. Podés usar colores del Immigrant Heritage Month o simplemente mantener la paleta de marca con copy más personal.",
        ]
    )

    story += story_block(
        "Martes 16 de junio",
        "Review",
        "Lo que cambia cuando actuás a tiempo",
        "ES",
        [
            "★★★★★",
            "'Mi esposo y yo siempre postergábamos esto porque pensábamos que era para gente mayor o millonaria. Hoy tenemos un trust, un plan médico de emergencia y todo en orden. El proceso fue más fácil de lo que esperábamos.'",
            "Cliente, National City",
            "",
            "No esperés a que sea urgente. Link en bio 👇",
            "Tip de diseño: quote larga — podés dividirla en 2 slides consecutivos para que se lea bien en mobile.",
        ]
    )

    story += story_block(
        "Jueves 18 de junio",
        "Educativa",
        "¿Qué pasa en tu primera consulta con MJ Trust Law?",
        "ES",
        [
            "¿No sabés qué esperar? Así funciona:",
            "✓ 30 a 45 minutos, en persona o por videollamada",
            "✓ Revisamos tu situación sin juzgar ni apurar",
            "✓ Te explicamos qué documentos necesitás y por qué",
            "✓ Te damos un presupuesto claro, sin letra chica",
            "✓ Sin compromiso — si no te convence, sin problema",
            "Agendá en el link de la bio 👇",
            "Tip de diseño: checklist visual con tildas verdes. Fondo crema. Ideal para convertir a quienes tienen dudas sobre el proceso.",
        ]
    )

    # ── STORIES WEEK 4 ─────────────────────────────────────────────
    story.append(sec_hdr("STORIES — WEEK 4  (June 22–28)", colors.HexColor("#7d3c98")))
    story.append(Spacer(1, 8))

    story += story_block(
        "Lunes 22 de junio",
        "Oficina",
        "Última semana de junio — ¿Todavía no agendaste?",
        "ES",
        [
            "Junio casi termina.",
            "Si lo venías postergando, esta semana es la señal.",
            "📍 Chula Vista, CA",
            "🕐 Lunes a viernes, 9am a 6pm",
            "Primera consulta: GRATUITA y sin compromiso",
            "Quedan lugares esta semana. Agendá en el link de la bio 👇",
            "Tip de diseño: agregar un elemento de urgencia sutil — podés usar un contador de días del mes o simplemente el copy. No exagerar la urgencia, mantener el tono empático de la marca.",
        ]
    )

    story += story_block(
        "Miércoles 24 de junio",
        "Review",
        "Una llamada que cambió todo",
        "ES",
        [
            "★★★★★",
            "'Soy dueño de un negocio pequeño en Chula Vista. Nunca había pensado en estate planning porque creía que era para otra gente. Una llamada de 30 minutos cambió todo lo que pensaba sobre el tema.'",
            "Cliente, Chula Vista",
            "",
            "Tu negocio también es parte de tu estate. Hablemos. Link en bio 👇",
            "Tip de diseño: podés usar esta review para hacer un puente con el carrusel del caso del dueño de negocio del día 26.",
        ]
    )

    story += story_block(
        "Viernes 26 de junio",
        "Educativa",
        "Pregunta frecuente: ¿Necesito ser ciudadano para tener un trust?",
        "ES",
        [
            "No.",
            "Cualquier persona con bienes en California puede tener un estate plan, independientemente de su estatus migratorio.",
            "Residentes permanentes, visas de trabajo, DACA, y más — todos tienen activos que proteger y derechos legales que usar.",
            "¿Tenés más preguntas? DM o link en bio 👇",
            "Tip de diseño: pregunta grande al inicio en formato bold. Respuesta directa debajo. Fondo navy con texto blanco para mayor contraste e impacto visual.",
        ]
    )

    doc.build(story)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    build("/home/user/Vuelta-rapida/Content_Calendar_MJTrustLaw.pdf")
