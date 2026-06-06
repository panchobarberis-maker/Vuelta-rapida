from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

NAVY  = colors.HexColor("#1a2e4a")
GOLD  = colors.HexColor("#C2801A")
CREAM = colors.HexColor("#F0E8DC")
GRAY  = colors.HexColor("#555555")
RED   = colors.HexColor("#c0392b")
WHITE = colors.white

def build(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            leftMargin=0.75*inch, rightMargin=0.75*inch,
                            topMargin=0.7*inch, bottomMargin=0.9*inch)

    h1      = ParagraphStyle("h1",  fontSize=22, textColor=NAVY,  fontName="Helvetica-Bold", spaceAfter=2,  leading=26)
    h2      = ParagraphStyle("h2",  fontSize=13, textColor=NAVY,  fontName="Helvetica-Bold", spaceAfter=4,  leading=16)
    sub     = ParagraphStyle("sub", fontSize=10, textColor=GRAY,  fontName="Helvetica",       spaceAfter=2,  leading=13)
    label   = ParagraphStyle("lbl", fontSize=9.5,textColor=NAVY,  fontName="Helvetica-Bold", spaceAfter=1,  leading=13)
    body    = ParagraphStyle("bdy", fontSize=9.5,textColor=colors.black, fontName="Helvetica", spaceAfter=5, leading=14)
    email_p = ParagraphStyle("ep",  fontSize=10, textColor=colors.HexColor("#222222"),
                             fontName="Helvetica", spaceAfter=10, leading=15, leftIndent=6, rightIndent=6)
    subj_s  = ParagraphStyle("sbj", fontSize=11, textColor=NAVY,  fontName="Helvetica-Bold",
                             spaceAfter=4, leading=14, leftIndent=6)
    prev_s  = ParagraphStyle("prv", fontSize=9,  textColor=GRAY,  fontName="Helvetica-Oblique",
                             spaceAfter=8, leading=12, leftIndent=6)
    cta_s   = ParagraphStyle("cta", fontSize=11, textColor=WHITE, fontName="Helvetica-Bold",
                             leading=14, alignment=TA_CENTER)
    sec_s   = ParagraphStyle("sec", fontSize=10, textColor=WHITE, fontName="Helvetica-Bold",
                             leading=14, leftIndent=4)
    bullet  = ParagraphStyle("bul", fontSize=9.5,textColor=colors.black, fontName="Helvetica",
                             spaceAfter=3, leading=13, leftIndent=14)
    foot_s  = ParagraphStyle("ft",  fontSize=8.5,textColor=GRAY,  fontName="Helvetica",
                             leading=12, alignment=TA_CENTER)

    def sec_hdr(text):
        t = Table([[Paragraph(text, sec_s)]], colWidths=[doc.width])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),NAVY),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
            ("LEFTPADDING",(0,0),(-1,-1),8),
        ]))
        return t

    def email_box(paragraphs):
        t = Table([[p] for p in paragraphs], colWidths=[doc.width - 0.4*inch])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),CREAM),
            ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
            ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),
            ("BOX",(0,0),(-1,-1),1,colors.HexColor("#d0c0a8")),
        ]))
        return t

    def cta_button(text):
        t = Table([[Paragraph(text, cta_s)]], colWidths=[3*inch])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),NAVY),
            ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
            ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
        ]))
        wrap = Table([[t]], colWidths=[doc.width - 0.4*inch])
        wrap.setStyle(TableStyle([
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("BACKGROUND",(0,0),(-1,-1),CREAM),
            ("TOPPADDING",(0,0),(-1,-1),14),("BOTTOMPADDING",(0,0),(-1,-1),14),
            ("BOX",(0,0),(-1,-1),1,colors.HexColor("#d0c0a8")),
        ]))
        return wrap

    story = []

    # ── TÍTULO ────────────────────────────────────────────────────
    story.append(Paragraph("PROPUESTA DE EMAIL MARKETING", h1))
    story.append(Paragraph("Campaña de re-engagement para contactos sin convertir", sub))
    story.append(HRFlowable(width="100%", thickness=1.5, color=GOLD, spaceAfter=8, spaceBefore=4))
    story.append(Spacer(1, 4))

    # ── OBJETIVO ─────────────────────────────────────────────────
    story.append(sec_hdr("OBJETIVO DE LA CAMPAÑA"))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Contexto", label))
    story.append(Paragraph(
        "La firma cuenta con una lista de contactos que solicitaron información sobre servicios de estate planning "
        "pero no llegaron a contratar. Esta campaña busca retomar esa conversación de forma empática, sin presión, "
        "usando un caso hipotético concreto para mostrar el costo real de no actuar.", body))
    story.append(Paragraph("Intención detrás del mensaje", label))
    story.append(Paragraph(
        "No se trata de vender. Se trata de educar con un ejemplo relatable que el contacto pueda proyectar "
        "en su propia situación. El email construye autoridad y confianza antes de pedir la acción.", body))
    story.append(Spacer(1, 10))

    # ── DATOS DEL EMAIL ──────────────────────────────────────────
    story.append(sec_hdr("DATOS DEL EMAIL"))
    story.append(Spacer(1, 6))

    meta = [
        ("Asunto",        "El error más caro que cometen las familias en California"),
        ("Preview text",  "Una historia que se repite. Y que todavía están a tiempo de cambiar."),
        ("Idioma",        "Español"),
        ("Herramienta",   "Mailchimp"),
        ("Audiencia",     "Contactos que solicitaron información pero no contrataron"),
        ("Tono",          "Empático, educativo, sin presión"),
    ]
    meta_rows = [[Paragraph(k, label), Paragraph(v, body)] for k, v in meta]
    meta_t = Table(meta_rows, colWidths=[1.5*inch, doc.width - 1.5*inch])
    meta_t.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),4),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[WHITE, CREAM]),
        ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#dddddd")),
    ]))
    story.append(meta_t)
    story.append(Spacer(1, 14))

    # ── EMAIL COMPLETO ────────────────────────────────────────────
    story.append(sec_hdr("EMAIL"))
    story.append(Spacer(1, 6))

    email_content = [
        Paragraph("Asunto: <b>El error más caro que cometen las familias en California</b>", subj_s),
        Paragraph("Preview: Una historia que se repite. Y que todavía están a tiempo de cambiar.", prev_s),
        Paragraph(
            "Hay una conversación que tenemos seguido en nuestra oficina de Chula Vista. Alguien viene a preguntar "
            "sobre estate planning, se va con toda la información, y nos dice que lo piensa. Que lo habla con su "
            "pareja. Que lo hace el mes que viene.",
            email_p),
        Paragraph(
            "A veces vuelven. Y a veces nos enteramos de lo que pasó mientras esperaban.",
            email_p),
        Paragraph(
            "Hace unos meses atendimos a una familia de Chula Vista que vivió exactamente eso. Tenían una casa, "
            "una cuenta de retiro y la intención de armar su trust \"el año que viene\". Entonces pasó algo "
            "inesperado. Y sin un plan en lugar, su familia tuvo que iniciar un proceso de probate en California "
            "para poder acceder a lo que les correspondía.",
            email_p),
        Paragraph(
            "No fue rápido. No fue barato. Y fue exactamente lo que querían evitarle a las personas que más amaban.",
            email_p),
        Paragraph(
            "El probate en California no es solo un trámite. Para una propiedad valorada en <b>$700,000</b> en el "
            "área de San Diego, los honorarios legales obligatorios pueden superar los <b>$40,000</b>. Eso sin "
            "contar los meses de proceso, los documentos ni el desgaste emocional de manejarlo todo en el peor "
            "momento posible.",
            email_p),
        Paragraph(
            "Un trust bien estructurado hubiera evitado todo eso. El costo de armarlo es una fracción de lo que "
            "esa familia terminó pagando.",
            email_p),
        Paragraph(
            "No hace falta tener todo claro para dar el primer paso. En una consulta gratuita de 30 minutos "
            "revisamos tu situación, te explicamos qué necesitás y te damos un presupuesto concreto. Sin "
            "formularios largos. Sin compromisos. Solo una conversación.",
            email_p),
    ]
    story.append(email_box(email_content))
    story.append(Spacer(1, 8))
    story.append(cta_button("Agendá tu consulta gratuita"))
    story.append(Spacer(1, 14))

    # ── ESTRUCTURA VISUAL ─────────────────────────────────────────
    story.append(sec_hdr("ESTRUCTURA VISUAL EN MAILCHIMP"))
    story.append(Spacer(1, 6))
    visual_items = [
        "Header con logo MJ Trust Law sobre fondo crema",
        "Cuerpo en columna única, tipografía limpia e interlineado generoso",
        "Los valores $700,000 y $40,000 en negrita para capturar la atención al escanear",
        "Botón CTA en navy con texto blanco, centrado, tamaño generoso",
        "Separador dorado entre secciones para mantener la identidad visual de la firma",
        "Footer con dirección Chula Vista, teléfono y enlace de darse de baja (obligatorio Mailchimp)",
    ]
    for item in visual_items:
        story.append(Paragraph(f"• {item}", bullet))
    story.append(Spacer(1, 14))

    # ── ESTRATEGIA ────────────────────────────────────────────────
    story.append(sec_hdr("ESTRATEGIA E INTENCIÓN"))
    story.append(Spacer(1, 6))
    strategy_items = [
        ("Seguimiento comercial no invasivo",
         "El email no menciona que el contacto ya nos escribió. Funciona como contenido de valor para cualquier persona en la lista, sin hacer sentir al receptor que está siendo perseguido."),
        ("Caso hipotético como espejo",
         "El ejemplo de la familia de Chula Vista es lo suficientemente específico para ser creíble y lo suficientemente genérico para que cualquier lector se proyecte en él."),
        ("El número hace el trabajo",
         "$40,000 es el argumento más poderoso del email. No hace falta presionar: la matemática habla sola."),
        ("CTA de baja fricción",
         "La consulta gratuita elimina la barrera más grande. El botón no dice 'Contratanos' sino 'Hablemos'. Reduce la resistencia y aumenta los clics."),
        ("Próximo paso sugerido",
         "Si la respuesta es baja, esta campaña puede ser el primer email de una secuencia de tres: este email educativo, uno de testimonio, y uno de urgencia suave con fecha límite para la consulta gratuita."),
    ]
    for title_s, desc in strategy_items:
        story.append(Paragraph(title_s, label))
        story.append(Paragraph(desc, body))
    story.append(Spacer(1, 20))

    # ── FOOTER ───────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=10, spaceBefore=4))
    story.append(Paragraph("Realizado por <b>Francisco Barberis</b>", foot_s))
    story.append(Paragraph("MJ Trust Law", foot_s))

    doc.build(story)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    build("/home/user/Vuelta-rapida/Email_Marketing_Proposal_MJTrustLaw.pdf")
