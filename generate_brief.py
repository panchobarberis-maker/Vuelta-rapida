from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

NAVY = colors.HexColor("#1a2e4a")
BLUE_LIGHT = colors.HexColor("#e8f0fe")
MID_GRAY = colors.HexColor("#555555")
GREEN = colors.HexColor("#1a7a4a")

def build_brief(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            leftMargin=0.75*inch, rightMargin=0.75*inch,
                            topMargin=0.7*inch, bottomMargin=0.7*inch)

    h1 = ParagraphStyle("h1", fontSize=22, textColor=NAVY, fontName="Helvetica-Bold", spaceAfter=4, leading=26)
    subtitle = ParagraphStyle("sub", fontSize=10, textColor=MID_GRAY, fontName="Helvetica", spaceAfter=2, leading=13)
    section = ParagraphStyle("section", fontSize=11, textColor=colors.white, fontName="Helvetica-Bold",
                             spaceAfter=0, leading=14, leftIndent=4)
    label = ParagraphStyle("label", fontSize=9.5, textColor=NAVY, fontName="Helvetica-Bold",
                           spaceAfter=1, leading=13)
    body = ParagraphStyle("body", fontSize=9.5, textColor=colors.black, fontName="Helvetica",
                          spaceAfter=5, leading=13)
    bullet = ParagraphStyle("bullet", fontSize=9.5, textColor=colors.black, fontName="Helvetica",
                            spaceAfter=2, leading=13, leftIndent=12)
    note = ParagraphStyle("note", fontSize=9, textColor=MID_GRAY, fontName="Helvetica-Oblique",
                          spaceAfter=2, leading=12, leftIndent=8)
    kw_tag = ParagraphStyle("kw", fontSize=9.5, textColor=GREEN, fontName="Helvetica-Bold",
                            spaceAfter=3, leading=13)

    def sec_header(text):
        t = Table([[Paragraph(text, section)]], colWidths=[doc.width])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0),(-1,-1), NAVY),
            ("TOPPADDING", (0,0),(-1,-1), 5),
            ("BOTTOMPADDING", (0,0),(-1,-1), 5),
            ("LEFTPADDING", (0,0),(-1,-1), 8),
        ]))
        return t

    def info_row(lbl, val):
        return [
            Paragraph(lbl, label),
            Paragraph(val, body),
        ]

    story = []

    # Title
    story.append(Paragraph("CONTENT BRIEF", h1))
    story.append(Paragraph("Employment Lawyer in Houston", ParagraphStyle("t2", fontSize=16, textColor=NAVY,
                           fontName="Helvetica-Bold", spaceAfter=4, leading=20)))
    story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceAfter=6, spaceBefore=4))

    story.append(Spacer(1, 6))

    # Keywords
    story.append(sec_header("KEYWORD STRATEGY"))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Primary Keyword", label))
    story.append(Paragraph("employment lawyer Houston &nbsp;&nbsp;|&nbsp;&nbsp; Est. volume: 1,300/mo &nbsp;&nbsp;|&nbsp;&nbsp; Difficulty: Medium-High", kw_tag))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Secondary Keywords", label))
    secondary = [
        "employment attorney Houston",
        "wrongful termination lawyer Houston",
        "workplace discrimination attorney Houston",
        "Houston employment law firm",
        "labor lawyer Houston TX",
        "sue my employer in Houston",
    ]
    for kw in secondary:
        story.append(Paragraph(f"• {kw}", bullet))
    story.append(Spacer(1, 4))

    story.append(Paragraph("LSI / Semantic Terms to Include Naturally", label))
    lsi = ["at-will employment Texas", "EEOC complaint", "workplace rights", "unpaid wages attorney",
           "retaliation at work", "employment law consultation", "Texas Workforce Commission"]
    story.append(Paragraph("  ·  ".join(lsi), body))
    story.append(Spacer(1, 10))

    # Search intent
    story.append(sec_header("SEARCH INTENT & TARGET AUDIENCE"))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Intent", label))
    story.append(Paragraph(
        "<b>Commercial / Transactional</b> — The user is an employee in Houston who believes their workplace rights "
        "have been violated and is actively looking to consult with or hire an employment lawyer.",
        body))
    story.append(Paragraph("Who is reading this?", label))
    audience = [
        "Employees who were recently fired and suspect it was illegal (wrongful termination)",
        "Workers experiencing discrimination based on race, gender, age, or disability",
        "Employees facing sexual harassment in the workplace",
        "Workers who haven't received proper wages or overtime",
        "Employees who were retaliated against for filing a complaint",
    ]
    for a in audience:
        story.append(Paragraph(f"• {a}", bullet))
    story.append(Spacer(1, 10))

    # Article structure
    story.append(sec_header("RECOMMENDED ARTICLE STRUCTURE"))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Target Length: 1,500 – 2,000 words", note))
    story.append(Spacer(1, 4))

    structure = [
        ("H1", "Employment Lawyer in Houston | Lange Firm"),
        ("Intro (100 words)", "Answer directly: what an employment lawyer does and when you need one. Include primary keyword in first sentence."),
        ("H2", "What Does an Employment Lawyer Do?"),
        ("H2", "When Should You Hire an Employment Lawyer in Houston?"),
        ("H3", "Wrongful Termination"),
        ("H3", "Workplace Discrimination"),
        ("H3", "Sexual Harassment"),
        ("H3", "Unpaid Wages & Overtime"),
        ("H3", "Retaliation"),
        ("H2", "Why Choose Lange Firm for Your Employment Law Case in Houston?"),
        ("H2", "How Much Does an Employment Lawyer Cost in Houston?"),
        ("H2", "How to Get Started — Free Consultation"),
        ("H2", "Frequently Asked Questions"),
        ("H3", "What is employment law?"),
        ("H3", "How long do I have to file an employment claim in Texas?"),
        ("H3", "Can I sue my employer in Houston?"),
        ("H3", "What is the statute of limitations for employment cases in Texas?"),
    ]

    struct_table = Table(
        [[Paragraph(tag, ParagraphStyle("tag", fontSize=8.5, textColor=colors.white, fontName="Helvetica-Bold", leading=12)),
          Paragraph(title, ParagraphStyle("stitle", fontSize=9.5, textColor=colors.black, fontName="Helvetica", leading=13))]
         for tag, title in structure],
        colWidths=[0.85*inch, doc.width - 0.85*inch]
    )
    struct_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(0,-1), NAVY),
        ("BACKGROUND", (1,0),(1,-1), colors.white),
        ("ROWBACKGROUNDS", (1,0),(1,-1), [colors.white, BLUE_LIGHT]),
        ("TOPPADDING", (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
        ("LEFTPADDING", (0,0),(-1,-1), 6),
        ("GRID", (0,0),(-1,-1), 0.5, colors.HexColor("#d0d0d0")),
        ("VALIGN", (0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(struct_table)
    story.append(Spacer(1, 10))

    # On-page SEO
    story.append(sec_header("ON-PAGE SEO & METADATA"))
    story.append(Spacer(1, 6))
    on_page = [
        ("Meta Title", "Employment Lawyer Houston | Lange Firm | Free Consultation"),
        ("Meta Description", "Facing workplace injustice in Houston? Lange Firm's employment lawyers fight for your rights. Wrongful termination, discrimination & harassment. Call today."),
        ("Slug", "/employment-lawyer-houston"),
        ("Word Count", "1,500 – 2,000 words"),
        ("Primary KW in", "H1, first 100 words, at least 2 H2s, meta title, meta description, image alt text"),
    ]
    for lbl, val in on_page:
        story.append(Paragraph(lbl, label))
        story.append(Paragraph(val, body))
    story.append(Spacer(1, 10))

    # Linking
    story.append(sec_header("INTERNAL & EXTERNAL LINKS"))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Internal Links to Include", label))
    internal = ["/wrongful-termination-lawyer-houston", "/workplace-discrimination-attorney",
                "/sexual-harassment-lawyer-houston", "/unpaid-wages-attorney", "/contact"]
    for l in internal:
        story.append(Paragraph(f"• {l}", bullet))
    story.append(Spacer(1, 4))
    story.append(Paragraph("External Authority Links", label))
    external = ["eeoc.gov — EEOC complaint process", "twc.texas.gov — Texas Workforce Commission",
                "texasbar.com — State Bar of Texas"]
    for l in external:
        story.append(Paragraph(f"• {l}", bullet))
    story.append(Spacer(1, 10))

    # AEO / Schema
    story.append(sec_header("AEO / AI SEARCH OPTIMIZATION"))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Schema Markup Required", label))
    schemas = ["FAQ Schema — apply to all H3 questions in the FAQ section",
               "LegalService Schema — firm name, practice area, location, hours",
               "LocalBusiness Schema — address, phone, service area (Houston, Sugar Land, TX)"]
    for s in schemas:
        story.append(Paragraph(f"• {s}", bullet))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Content Formatting for AI Readability", label))
    aeo_notes = [
        "First paragraph must directly answer: 'What is an employment lawyer and do I need one?' in 2-3 sentences",
        "Keep paragraphs to 3-4 sentences max",
        "Use question-format H2s and H3s where possible — AI tools pull these as answers",
        "Include a dedicated FAQ section (minimum 4 questions with concise answers under 60 words each)",
        "Add E-E-A-T signals: attorney bar admission, years of experience, Houston-specific case references",
    ]
    for n in aeo_notes:
        story.append(Paragraph(f"• {n}", bullet))
    story.append(Spacer(1, 10))

    # CTA & notes
    story.append(sec_header("CTA & EDITORIAL NOTES"))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Primary CTA", label))
    story.append(Paragraph('"Schedule a free consultation with Lange Firm today" → link to /contact. Include inline CTA mid-article and again at the end.', body))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Editorial Notes", label))
    notes = [
        "Write for the client, not the attorney — avoid jargon, use plain language",
        "Reference Houston and Sugar Land naturally throughout (local SEO signal)",
        "Do NOT make specific legal promises or guarantees — flag for attorney review before publishing",
        "Tone: empathetic and authoritative — the reader is likely stressed and scared",
    ]
    for n in notes:
        story.append(Paragraph(f"• {n}", bullet))

    doc.build(story)
    print(f"Brief saved to {output_path}")

if __name__ == "__main__":
    build_brief("/home/user/Vuelta-rapida/Content_Brief_Employment_Lawyer_Houston.pdf")
