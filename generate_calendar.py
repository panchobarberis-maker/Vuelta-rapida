from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

NAVY  = colors.HexColor("#1a2e4a")
GOLD  = colors.HexColor("#C2801A")
CREAM = colors.HexColor("#F0E8DC")
GRAY  = colors.HexColor("#777777")
LGRAY = colors.HexColor("#f7f3ee")
WHITE = colors.white
RED   = colors.HexColor("#c0392b")

def build(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            leftMargin=0.65*inch, rightMargin=0.65*inch,
                            topMargin=0.6*inch, bottomMargin=0.6*inch)

    h1    = ParagraphStyle("h1", fontSize=22, textColor=NAVY, fontName="Helvetica-Bold", spaceAfter=2, leading=26)
    h2    = ParagraphStyle("h2", fontSize=13, textColor=NAVY, fontName="Helvetica-Bold", spaceAfter=2, leading=16)
    sub   = ParagraphStyle("sub", fontSize=9, textColor=GRAY, fontName="Helvetica", spaceAfter=4, leading=12)
    body  = ParagraphStyle("body", fontSize=9.5, textColor=colors.black, fontName="Helvetica", spaceAfter=3, leading=13)
    bold  = ParagraphStyle("bold", fontSize=9.5, textColor=NAVY, fontName="Helvetica-Bold", spaceAfter=2, leading=13)
    italic= ParagraphStyle("italic", fontSize=9.5, textColor=GRAY, fontName="Helvetica-Oblique", spaceAfter=3, leading=13)
    small = ParagraphStyle("small", fontSize=8.5, textColor=GRAY, fontName="Helvetica", spaceAfter=2, leading=11)
    copy_s= ParagraphStyle("copy", fontSize=9, textColor=colors.black, fontName="Helvetica-Oblique", spaceAfter=3, leading=13, leftIndent=8)
    tag_s = ParagraphStyle("tag", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold", leading=11)
    week_s= ParagraphStyle("week", fontSize=11, textColor=WHITE, fontName="Helvetica-Bold", leading=14)

    def sec_hdr(text):
        t = Table([[Paragraph(text, week_s)]], colWidths=[doc.width])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),NAVY),
            ("TOPPADDING",(0,0),(-1,-1),7),
            ("BOTTOMPADDING",(0,0),(-1,-1),7),
            ("LEFTPADDING",(0,0),(-1,-1),10),
        ]))
        return t

    def tag(label, color):
        t = Table([[Paragraph(label, tag_s)]], colWidths=[1.2*inch])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),color),
            ("TOPPADDING",(0,0),(-1,-1),3),
            ("BOTTOMPADDING",(0,0),(-1,-1),3),
            ("LEFTPADDING",(0,0),(-1,-1),6),
        ]))
        return t

    FORMAT_COLORS = {
        "Carrusel":    colors.HexColor("#2e6da4"),
        "Reel":        colors.HexColor("#8e44ad"),
        "Post Estático": colors.HexColor("#27ae60"),
        "Podcast Clip":  colors.HexColor("#d35400"),
        "GIF / Motion":  colors.HexColor("#c0392b"),
    }
    LANG_COLORS = {
        "ES":    colors.HexColor("#1a7a4a"),
        "EN":    colors.HexColor("#1a4a7a"),
        "ES/EN": colors.HexColor("#6d3a7a"),
    }

    def post_block(date, title, format_type, lang, objective, why_format, visual, copy_text, special=None):
        elems = []
        # Header row
        hdr_cells = [
            Paragraph(f"<b>{date}</b>", ParagraphStyle("d", fontSize=9, textColor=GRAY, fontName="Helvetica-Bold", leading=12)),
            tag(format_type, FORMAT_COLORS.get(format_type, NAVY)),
            tag(lang, LANG_COLORS.get(lang, NAVY)),
        ]
        if special:
            hdr_cells.append(tag(special, colors.HexColor("#c0392b")))
        hdr_t = Table([hdr_cells], colWidths=[1.4*inch, 1.3*inch, 0.7*inch] + ([1.5*inch] if special else []))
        hdr_t.setStyle(TableStyle([
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LEFTPADDING",(0,0),(-1,-1),0),
            ("RIGHTPADDING",(0,0),(-1,-1),6),
            ("TOPPADDING",(0,0),(-1,-1),0),
            ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ]))
        elems.append(hdr_t)
        elems.append(Paragraph(title, h2))
        rows = [
            ["Objetivo", objective],
            ["Por qué este formato", why_format],
            ["Visual", visual],
        ]
        for lbl, val in rows:
            elems.append(Paragraph(lbl, bold))
            elems.append(Paragraph(val, body))
        elems.append(Paragraph("Copy", bold))
        for line in copy_text:
            elems.append(Paragraph(line, copy_s))
        elems.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#dddddd"), spaceAfter=10, spaceBefore=6))
        return elems

    story = []

    # Title
    story.append(Paragraph("CONTENT CALENDAR — MJ TRUST LAW", h1))
    story.append(Paragraph("June 2026  |  Instagram  |  4 posts/week  |  English & Spanish", sub))
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=10, spaceBefore=4))

    # Content Mix Legend
    mix = [
        ["Formato", "Descripción", "Frecuencia"],
        ["Carrusel", "Casos hipotéticos, Myths, Educación", "2x semana"],
        ["Reel / Video", "Abogada a cámara, Podcast clips", "1x semana"],
        ["Post Estático", "Contrast hooks, Stats, CTAs", "1x semana"],
    ]
    mix_t = Table(mix, colWidths=[1.4*inch, 3.5*inch, 1.5*inch])
    mix_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),
        ("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),9),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[LGRAY, WHITE]),
        ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#dddddd")),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),8),
    ]))
    story.append(mix_t)
    story.append(Spacer(1, 14))

    # ── WEEK 1 ──────────────────────────────────────────────────────
    story.append(sec_hdr("WEEK 1  —  June 1–7"))
    story.append(Spacer(1, 8))

    story += post_block(
        "Lunes 1 de junio", "\"Protegés tu contraseña. ¿Y tu herencia?\"",
        "Post Estático", "ES",
        "Generar conciencia con un hook de alto impacto. Parar el scroll.",
        "El contraste inmediato funciona mejor en post estático — texto grande sobre fondo limpio. Se lee en 2 segundos.",
        "Fondo crema. Texto navy gigante: \"Protegés tu contraseña. ¿Y tu herencia?\". Logo MJ Trust Law abajo. Mínimo, limpio.",
        [
            "Protegés tu contraseña. Tenés seguro de auto. Guardás tus contratos.",
            "¿Por qué tu familia no tiene un plan si algo te pasa?",
            "El estate planning no es para cuando seas viejo. Es para ahora.",
            "📩 Consulta gratuita en el link de la bio.",
            "#EstatePlanning #TrustLaw #SanDiego #FamiliasLatinas #MJTrustLaw",
        ]
    )

    story += post_block(
        "Miércoles 3 de junio", "Caso Hipotético: La cuenta olvidada de María",
        "Carrusel", "ES",
        "Educar con storytelling. Mostrar cómo un error pequeño puede romper un plan perfecto.",
        "El carrusel permite contar una historia slide a slide — genera curiosidad y retención. Ideal para casos complejos.",
        "6 slides. Fondo crema / navy. Slide 1: \"María tenía un trust perfecto. Hasta que olvidó una cosa.\" Slide final: CTA consulta.",
        [
            "Slide 1: María tenía un trust perfecto. Su casa, sus beneficiarios, todo en orden. Hasta que olvidó una cosa.",
            "Slide 2: Una cuenta bancaria de $800. A su nombre. Fuera del trust.",
            "Slide 3: Cuando María falleció, esa cuenta abrió la puerta al probate court.",
            "Slide 4: Y el probate en California se calcula sobre el valor BRUTO del estate. No solo los $800.",
            "Slide 5: Una cuenta pequeña puede exponer toda tu herencia. No por su valor, sino por lo que revela.",
            "Slide 6: ¿Tu trust está completo? Revisalo con nosotros. Consulta gratuita 👇",
            "#TrustPlanning #Probate #California #EstatePlanning #MJTrustLaw",
        ]
    )

    story += post_block(
        "Viernes 5 de junio", "Reel: ¿Qué es un trust y por qué tu familia lo necesita?",
        "Reel", "ES",
        "Posicionar a la abogada como experta. Educación básica en formato video para audiencia que no conoce el tema.",
        "La abogada a cámara genera confianza y cercanía. Para audiencia latina que necesita ver quién la asesora antes de confiar.",
        "Abogada a cámara, buena iluminación, fondo de oficina o neutro. Subtítulos en español. Duración: 45-60 segundos.",
        [
            "Caption: Un trust no es solo para millonarios. Es para cualquier familia que quiera proteger lo que construyó.",
            "En este video te explico qué es, cómo funciona y por qué en California es especialmente importante.",
            "¿Tenés preguntas? Escribime por DM o agendá una consulta gratuita en el link de la bio 👇",
            "#Trust #EstatePlanning #AbogadaLatina #SanDiego #California #MJTrustLaw",
        ]
    )

    story += post_block(
        "Domingo 7 de junio", "Mito #1: \"Con testamento es suficiente\"",
        "Carrusel", "EN",
        "Combatir la misconception más común. Audiencia que cree que ya tiene todo resuelto.",
        "Carrusel para desarrollar el argumento paso a paso. En inglés para alcanzar audiencia más amplia en Instagram.",
        "5 slides. Slide 1: \"MYTH: If you have a will, your family is protected.\" en rojo. Slide 2-4: Explicación. Slide 5: CTA.",
        [
            "Slide 1: MYTH: \"If I have a will, my family is protected.\"",
            "Slide 2: A will still goes through probate court in California. That means months of legal process and public records.",
            "Slide 3: A trust, on the other hand, transfers your assets directly to your family — no court, no delays.",
            "Slide 4: For families with real estate in California, a will alone can cost your heirs thousands in probate fees.",
            "Slide 5: The difference matters. Let's talk. Free consultation at the link in bio.",
            "#EstatePlanningMyths #Will #TrustVsWill #CaliforniaLaw #MJTrustLaw",
        ]
    )

    story.append(Spacer(1, 6))

    # ── WEEK 2 ──────────────────────────────────────────────────────
    story.append(sec_hdr("WEEK 2  —  June 8–14"))
    story.append(Spacer(1, 8))

    story += post_block(
        "Lunes 8 de junio", "\"Tenés seguro de auto pero no un trust\"",
        "Post Estático", "ES",
        "Contrast hook de alto impacto. Generar conciencia con fricción positiva.",
        "Post estático para máxima legibilidad del hook. Texto grande que para el scroll.",
        "Fondo crema oscuro. Dos columnas: izquierda \"LO QUE SÍ TENÉS\" con lista, derecha \"LO QUE LE FALTA A TU FAMILIA\" con lista. Paleta navy/gold.",
        [
            "Tenés seguro de auto ✓",
            "Tenés contraseña en el teléfono ✓",
            "Tenés seguro médico ✓",
            "¿Tenés un plan para proteger tu casa, tus cuentas y tu familia si algo te pasa? ✗",
            "El estate planning no es un lujo. Es la decisión más importante que podés tomar para los que querés.",
            "Link en bio para agendar tu consulta gratuita.",
            "#FamiliaProtegida #TrustLaw #EstatePlanning #SanDiego #MJTrustLaw",
        ]
    )

    story += post_block(
        "Miércoles 10 de junio", "Caso Hipotético: La familia con bienes en México y USA",
        "Carrusel", "ES",
        "Hablar directamente a la audiencia inmigrante con bienes en dos países — el caso más relevante para sus clientes.",
        "Carrusel para contar el caso en detalle. Tema complejo que necesita espacio para explicarse bien.",
        "6 slides. Slide 1: \"Roberto construyó toda su vida entre México y California. Nadie le dijo que eso complica todo.\"",
        [
            "Slide 1: Roberto trabajó 30 años. Tiene una casa en Tijuana y un departamento en Chula Vista. Nunca hizo estate planning.",
            "Slide 2: Cuando Roberto falleció, su familia enfrentó dos sistemas legales distintos. Dos procesos. Dos costos.",
            "Slide 3: En California, el departamento entró a probate court. En México, iniciaron un juicio sucesorio por separado.",
            "Slide 4: Lo que podría haberse resuelto en semanas tardó casi 3 años y costó más de $40,000.",
            "Slide 5: Si tenés bienes en México y en USA, tu estate plan tiene que contemplar los dos países.",
            "Slide 6: En MJ Trust Law entendemos tu situación porque la vivimos. Consultá gratis 👇",
            "#FamiliasInmigrantes #BienesBinacionales #TrustLaw #Mexico #California #MJTrustLaw",
        ]
    )

    story += post_block(
        "Viernes 12 de junio", "Podcast Clip: [Tema del episodio]",
        "Podcast Clip", "ES/EN",
        "Aprovechar contenido existente. Posicionar a la abogada como thought leader con prueba social externa.",
        "Clip de podcast genera autoridad inmediata — alguien más la invitó a hablar. Cero producción extra.",
        "Video vertical del podcast con subtítulos grandes en español. 30-45 segundos. Highlight el momento más impactante del episodio.",
        [
            "Caption: Cuando me preguntaron en el podcast cuál es el error más común que cometen las familias latinas con su estate plan, la respuesta fue clara.",
            "Mirá el clip. 👆",
            "Si esto te resuena, el link para agendar tu consulta gratuita está en la bio.",
            "#Podcast #EstatePlanning #AbogadaLatina #FamiliasLatinas #MJTrustLaw",
        ]
    )

    story += post_block(
        "Domingo 14 de junio", "3 activos que NO pasan por tu testamento",
        "Post Estático", "EN",
        "Educación de alto valor que sorprende. Genera saves y shares.",
        "Post estático de lista — fácil de guardar, alto valor informativo. En inglés para mayor alcance.",
        "Fondo navy. Texto blanco y dorado. Título: \"3 ASSETS THAT DON'T PASS THROUGH YOUR WILL\". Lista numerada con iconos.",
        [
            "Most people don't know this:",
            "1. Life insurance proceeds (go directly to your named beneficiary)",
            "2. Retirement accounts like 401(k) and IRA (same — beneficiary designation overrides your will)",
            "3. Joint tenancy property (passes automatically to the surviving owner)",
            "This means your will alone may not control where a big part of your estate goes.",
            "Estate planning is more than a document. It's a strategy. Let's build yours. 🔗 Link in bio.",
            "#EstatePlanning #Will #TrustPlanning #CaliforniaLaw #MJTrustLaw",
        ]
    )

    story.append(Spacer(1, 6))

    # ── WEEK 3 ──────────────────────────────────────────────────────
    story.append(sec_hdr("WEEK 3  —  June 15–21  |  🌍 Immigrant Heritage Month  |  👨 Father's Day"))
    story.append(Spacer(1, 8))

    story += post_block(
        "Lunes 15 de junio", "Reel: 3 errores comunes en estate planning",
        "Reel", "ES",
        "Educación rápida y accionable. Generar saves y shares.",
        "Formato de lista en video es altamente compartible. La abogada a cámara refuerza autoridad.",
        "Abogada a cámara. Formato rápido: 3 puntos en 60 segundos. Subtítulos. Texto en pantalla con cada error.",
        [
            "Caption: Estos son los 3 errores que veo repetirse una y otra vez en las familias que vienen a verme.",
            "El 1 es el más común. El 3 es el más caro.",
            "Si querés revisar si tu plan tiene alguno de estos problemas, agendá una consulta gratuita en el link de la bio 👇",
            "#EstatePlanning #TrustPlanning #Probate #AbogadaLatina #MJTrustLaw",
        ]
    )

    story += post_block(
        "Miércoles 18 de junio", "Mito #2: \"Estate planning es solo para ricos\"",
        "Carrusel", "ES",
        "Eliminar la barrera de entrada más grande para la audiencia latina de clase media.",
        "Carrusel para desmantelar el mito con argumentos sólidos. El tema requiere espacio para convencer.",
        "5 slides. Slide 1: \"MITO: El estate planning es para millonarios.\" Grande, en rojo. Resto: argumentos y datos.",
        [
            "Slide 1: MITO: El estate planning es solo para ricos.",
            "Slide 2: Si tenés una casa en California, tenés un estate. El valor promedio en San Diego supera los $800,000.",
            "Slide 3: Sin un trust, tu familia enfrenta el probate court. Los honorarios legales en California pueden ser del 4 al 6% del valor bruto.",
            "Slide 4: En una casa de $500,000, eso son hasta $30,000 en costos que tu familia podría evitar.",
            "Slide 5: Un trust no es un lujo. Es la decisión financiera más inteligente que podés tomar por tu familia.",
            "Slide 6: Consultá gratis y entendé qué necesitás. Link en bio 👇",
            "#EstatePlanningParaTodos #TrustLaw #FamiliasLatinas #SanDiego #MJTrustLaw",
        ]
    )

    story += post_block(
        "Viernes 19 de junio", "Immigrant Heritage Month: Familias con raíces en dos países",
        "Post Estático", "ES/EN",
        "Conectar emocionalmente con la audiencia inmigrante. Relevancia cultural máxima.",
        "Post estático emocional y directo. El texto bilingüe refleja la identidad de su audiencia.",
        "Fondo crema con bandera o elemento cultural sutil. Texto en español e inglés. Emotivo pero profesional.",
        [
            "ES: Construiste una vida entre dos países. Trabajaste duro para dejarle algo a tu familia.",
            "Proteger eso requiere un plan que entienda tu historia.",
            "EN: You built a life across two countries. Protecting that legacy requires a plan that understands both.",
            "EN: At MJ Trust Law, we do.",
            "🔗 Free consultation. Link in bio.",
            "#ImmigrantHeritageMonth #FamiliasLatinas #EstatePlanning #SanDiego #MJTrustLaw",
        ],
        special="Immigrant Heritage Month"
    )

    story += post_block(
        "Domingo 21 de junio", "Father's Day: El mejor regalo que le podés dejar a tu familia",
        "Reel", "ES",
        "Conexión emocional máxima. El estate planning como acto de amor hacia la familia.",
        "Reel emotivo en el día de mayor sensibilidad familiar del mes. La abogada a cámara hablando directo al corazón.",
        "Abogada a cámara, tono cálido y personal. Puede comenzar con \"Hoy es el día del padre...\" Fondo suave. 45-60 seg.",
        [
            "Hoy, el día del padre, quiero hablarle a todos los papás que están construyendo algo para sus hijos.",
            "El mejor regalo que le podés dejar a tu familia no se compra.",
            "Es saber que si algo te pasa, ellos van a estar protegidos. Sin cortes. Sin deudas. Sin años en tribunales.",
            "Ese es el regalo que un trust le da a tu familia.",
            "Si querés empezar, el primer paso es una conversación. Y es gratis. Link en bio 👇",
            "Feliz día del padre. 🤍",
            "#DiaDelPadre #FathersDay #EstatePlanning #TrustLaw #FamiliasLatinas #MJTrustLaw",
        ],
        special="Father's Day 🤍"
    )

    story.append(Spacer(1, 6))

    # ── WEEK 4 ──────────────────────────────────────────────────────
    story.append(sec_hdr("WEEK 4  —  June 22–28"))
    story.append(Spacer(1, 8))

    story += post_block(
        "Lunes 22 de junio", "\"Guardás los recibos del súper pero no tenés testamento\"",
        "Post Estático", "ES",
        "Contrast hook con humor sutil. Romper la procrastinación.",
        "Post estático de impacto rápido. El humor leve hace que sea compartible.",
        "Fondo crema. Dos columnas o texto grande centrado. Tipografía bold. Navy y gold.",
        [
            "Guardás los recibos del súper por si acaso. ✓",
            "Tenés carpeta con todos los papeles del auto. ✓",
            "Recordás la contraseña de una cuenta que no usás hace 3 años. ✓",
            "¿Tenés un plan legal para proteger tu casa y tu familia? ✗",
            "No hace falta esperar el momento perfecto. Hace falta empezar.",
            "Consultá gratis. Link en bio 👇",
            "#EstatePlanning #TrustLaw #Procrastinación #SanDiego #MJTrustLaw",
        ]
    )

    story += post_block(
        "Miércoles 24 de junio", "Podcast Clip: El momento más impactante del episodio",
        "Podcast Clip", "ES",
        "Prueba social y autoridad. Reutilizar contenido existente de alto valor.",
        "Segundo clip del mes — refuerza presencia de la abogada como figura de autoridad en el tema.",
        "Video vertical, subtítulos grandes y claros en español. El clip debe tener un momento de \"wow\" o dato sorprendente.",
        [
            "Esto es lo que le digo a cada familia que viene a verme sin un plan:",
            "[cita del podcast]",
            "Si querés escuchar el episodio completo, el link está en mi bio.",
            "Y si querés que hablemos de tu situación específica, la primera consulta es gratis 👇",
            "#Podcast #TrustLaw #EstatePlanning #AbogadaLatina #MJTrustLaw",
        ]
    )

    story += post_block(
        "Viernes 26 de junio", "Caso Hipotético: El dueño de negocio que esperó demasiado",
        "Carrusel", "EN",
        "Llegar a audiencia de pequeños empresarios latinos. Un segmento con alta necesidad y bajo awareness.",
        "Carrusel para desarrollar el caso con detalle. En inglés para alcanzar a business owners bilingües.",
        "6 slides. Slide 1: \"He had a business, a home, and a plan. The plan was: I'll do it next year.\" Paleta navy/gold.",
        [
            "Slide 1: Carlos had a business, a home, and a retirement account. His estate plan? \"I'll take care of it next year.\"",
            "Slide 2: He passed away unexpectedly at 58. No trust. No succession plan for the business.",
            "Slide 3: His family had to go through probate for the home. And the business? It couldn't operate while the estate was in court.",
            "Slide 4: What took Carlos a lifetime to build took less than 18 months to complicate beyond repair.",
            "Slide 5: Business owners need estate planning more than anyone. Your business IS your estate.",
            "Slide 6: Don't wait for next year. Free consultation at the link in bio.",
            "#BusinessOwner #EstatePlanning #TrustLaw #SmallBusiness #MJTrustLaw",
        ]
    )

    story += post_block(
        "Domingo 28 de junio", "Reel CTA: ¿Tenés dudas? La consulta es gratis",
        "Reel", "ES",
        "Cerrar el mes con un llamado a la acción directo. Convertir audiencia que ya sigue el contenido.",
        "Reel de cierre con la abogada a cámara. Tono cercano y sin presión. La consulta gratuita baja la barrera de entrada.",
        "Abogada a cámara, tono amigable. Puede hablar de las preguntas más frecuentes que recibe. 45-60 segundos.",
        [
            "La pregunta que más me hacen es: ¿Por dónde empiezo?",
            "La respuesta siempre es la misma: con una conversación.",
            "No necesitás saber nada de leyes. No necesitás tener todo claro. Solo necesitás querer proteger a tu familia.",
            "La primera consulta es gratis y sin compromiso. Podemos hablar de tu situación y entender juntos qué necesitás.",
            "El link para agendar está en mi bio. Te espero 👇",
            "#ConsultaGratis #EstatePlanning #TrustLaw #AbogadaLatina #SanDiego #MJTrustLaw",
        ]
    )

    doc.build(story)
    print(f"Calendar saved to {output_path}")

if __name__ == "__main__":
    build("/home/user/Vuelta-rapida/Content_Calendar_MJTrustLaw.pdf")
