from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import ParagraphStyle

NAVY  = colors.HexColor("#1a2e4a")
GOLD  = colors.HexColor("#C2801A")
CREAM = colors.HexColor("#F0E8DC")
LGRAY = colors.HexColor("#f7f3ee")
GRAY  = colors.HexColor("#777777")
WHITE = colors.white
RED   = colors.HexColor("#c0392b")
GREEN = colors.HexColor("#1a7a4a")
PURP  = colors.HexColor("#6d3a7a")
BLUE  = colors.HexColor("#1a4a7a")
ORG   = colors.HexColor("#d35400")

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

def build(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            leftMargin=0.6*inch, rightMargin=0.6*inch,
                            topMargin=0.6*inch, bottomMargin=0.6*inch)

    h1    = ParagraphStyle("h1", fontSize=22, textColor=NAVY, fontName="Helvetica-Bold", spaceAfter=2, leading=26)
    h2    = ParagraphStyle("h2", fontSize=12, textColor=NAVY, fontName="Helvetica-Bold", spaceAfter=2, leading=15)
    sub   = ParagraphStyle("sub", fontSize=9, textColor=GRAY, fontName="Helvetica", spaceAfter=4, leading=12)
    body  = ParagraphStyle("body", fontSize=9.5, textColor=colors.black, fontName="Helvetica", spaceAfter=3, leading=13)
    bold  = ParagraphStyle("bold", fontSize=9.5, textColor=NAVY, fontName="Helvetica-Bold", spaceAfter=2, leading=13)
    copy_s= ParagraphStyle("copy", fontSize=9, textColor=colors.HexColor("#333333"), fontName="Helvetica-Oblique", spaceAfter=2, leading=13, leftIndent=8)
    tag_s = ParagraphStyle("tag", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold", leading=10)
    wk_s  = ParagraphStyle("wk", fontSize=11, textColor=WHITE, fontName="Helvetica-Bold", leading=14)
    cal_hdr= ParagraphStyle("calhdr", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold", leading=10, alignment=1)
    cal_day= ParagraphStyle("calday", fontSize=9, textColor=NAVY, fontName="Helvetica-Bold", leading=11, alignment=1)
    cal_emp= ParagraphStyle("calemp", fontSize=8, textColor=GRAY, fontName="Helvetica", leading=10, alignment=1)
    cal_ttl= ParagraphStyle("calttl", fontSize=7, textColor=NAVY, fontName="Helvetica", leading=9, alignment=1)
    cal_sp = ParagraphStyle("calsp", fontSize=6.5, textColor=RED, fontName="Helvetica-Bold", leading=9, alignment=1)

    def sec_hdr(text):
        t = Table([[Paragraph(text, wk_s)]], colWidths=[doc.width])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),NAVY),
            ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
            ("LEFTPADDING",(0,0),(-1,-1),10),
        ]))
        return t

    def tag(label, color):
        t = Table([[Paragraph(label, tag_s)]], colWidths=[1.2*inch])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),color),
            ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
            ("LEFTPADDING",(0,0),(-1,-1),6),
        ]))
        return t

    # ── CALENDAR GRID ──────────────────────────────────────────────
    # June 2026: starts Monday June 1
    # Posts: Mon, Wed, Fri, Sun
    POST_DAYS = {
        1:  ("Contrast Hook", "Post Estático", "ES"),
        3:  ("Caso: Cuenta olvidada", "Carrusel", "ES"),
        5:  ("Reel: ¿Qué es un trust?", "Reel", "ES"),
        7:  ("Mito #1: El testamento", "Carrusel", "EN"),
        8:  ("Contrast Hook #2", "Post Estático", "ES"),
        10: ("Caso: Bienes en 2 países", "Carrusel", "ES"),
        12: ("Podcast Clip #1", "Podcast Clip", "ES/EN"),
        14: ("3 activos sin testamento", "Post Estático", "EN"),
        15: ("Reel: 3 errores comunes", "Reel", "ES"),
        17: ("Mito #2: Solo para ricos", "Carrusel", "ES"),
        19: ("Immigrant Heritage Month", "Post Estático", "ES/EN"),
        21: ("Father's Day Reel", "Reel", "ES"),
        22: ("Contrast Hook #3", "Post Estático", "ES"),
        24: ("Podcast Clip #2", "Podcast Clip", "ES"),
        26: ("Caso: Dueño de negocio", "Carrusel", "EN"),
        28: ("Reel CTA: Consulta gratis", "Reel", "ES"),
    }
    SPECIAL = {19: "Juneteenth", 21: "Father's Day"}

    # June 2026: Mon=1, so weekday of June 1 = 0 (Mon)
    days_row = ["MON","TUE","WED","THU","FRI","SAT","SUN"]
    cal_col_w = doc.width / 7

    # Build calendar rows
    cal_rows = [[Paragraph(d, cal_hdr) for d in days_row]]
    # June has 30 days, starts Monday
    week = [None]*7
    for day in range(1, 31):
        dow = (day - 1) % 7  # 0=Mon
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
                    cell_content = [
                        Paragraph(str(d), cal_day),
                        Paragraph(title, cal_ttl),
                        Paragraph(fmt, ParagraphStyle("cf", fontSize=6.5, textColor=fc,
                                  fontName="Helvetica-Bold", leading=8, alignment=1)),
                    ]
                    if d in SPECIAL:
                        cell_content.append(Paragraph(SPECIAL[d], cal_sp))
                    row.append(cell_content)
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
    # Highlight post days
    for day in POST_DAYS:
        dow = (day - 1) % 7
        row_idx = (day - 1) // 7 + 1
        cal_style.add("BACKGROUND",(dow,row_idx),(dow,row_idx),colors.HexColor("#f0e8dc"))
    cal_table.setStyle(cal_style)

    def post_block(date, title, format_type, lang, objective, why_format, visual, copy_lines, special=None):
        elems = []
        hdr_cells = [
            Paragraph(f"<b>{date}</b>", ParagraphStyle("d", fontSize=9, textColor=GRAY,
                      fontName="Helvetica-Bold", leading=12)),
            tag(format_type, FORMAT_COLORS.get(format_type, NAVY)),
            tag(lang, LANG_COLORS.get(lang, NAVY)),
        ]
        if special:
            hdr_cells.append(tag(special, RED))
        hdr_t = Table([hdr_cells], colWidths=[1.4*inch,1.3*inch,0.7*inch]+([1.6*inch] if special else []))
        hdr_t.setStyle(TableStyle([
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LEFTPADDING",(0,0),(-1,-1),0),
            ("RIGHTPADDING",(0,0),(-1,-1),6),
            ("TOPPADDING",(0,0),(-1,-1),0),
            ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ]))
        block = [hdr_t, Paragraph(title, h2)]
        for lbl, val in [("Objetivo", objective), ("Por qué este formato", why_format), ("Visual", visual)]:
            block.append(Paragraph(lbl, bold))
            block.append(Paragraph(val, body))
        block.append(Paragraph("Copy", bold))
        for line in copy_lines:
            block.append(Paragraph(line, copy_s))
        block.append(HRFlowable(width="100%", thickness=0.5,
                     color=colors.HexColor("#dddddd"), spaceAfter=10, spaceBefore=6))
        elems.append(KeepTogether(block[:4]))
        elems += block[4:]
        return elems

    story = []

    # ── TITLE ──────────────────────────────────────────────────────
    story.append(Paragraph("CONTENT CALENDAR — MJ TRUST LAW", h1))
    story.append(Paragraph("June 2026  |  Instagram  |  4 posts/week  |  English & Spanish", sub))
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=10, spaceBefore=4))

    # ── CALENDAR VIEW ──────────────────────────────────────────────
    story.append(Paragraph("JUNE 2026 — OVERVIEW", ParagraphStyle("ov", fontSize=11,
                 textColor=NAVY, fontName="Helvetica-Bold", spaceAfter=6, leading=14)))
    story.append(cal_table)
    story.append(Spacer(1, 6))

    # Legend
    legend_items = [
        [tag("Carrusel", FORMAT_COLORS["Carrusel"]),
         tag("Reel", FORMAT_COLORS["Reel"]),
         tag("Post Estático", FORMAT_COLORS["Post Estático"]),
         tag("Podcast Clip", FORMAT_COLORS["Podcast Clip"]),
         tag("ES", LANG_COLORS["ES"]),
         tag("EN", LANG_COLORS["EN"]),
         tag("ES/EN", LANG_COLORS["ES/EN"])],
    ]
    leg_t = Table(legend_items, colWidths=[1.0*inch]*7)
    leg_t.setStyle(TableStyle([
        ("LEFTPADDING",(0,0),(-1,-1),0),
        ("RIGHTPADDING",(0,0),(-1,-1),4),
        ("TOPPADDING",(0,0),(-1,-1),0),
        ("BOTTOMPADDING",(0,0),(-1,-1),0),
    ]))
    story.append(leg_t)
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=14))

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
            "1. Life insurance proceeds → go directly to your named beneficiary. Your will doesn't touch them.",
            "2. Retirement accounts (401k, IRA) → same. Beneficiary designation overrides your will entirely.",
            "3. Joint tenancy property → passes automatically to the surviving owner.",
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

    doc.build(story)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    build("/home/user/Vuelta-rapida/Content_Calendar_MJTrustLaw.pdf")
