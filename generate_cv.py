from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus.flowables import AnchorFlowable

NAVY = colors.HexColor("#1a2e4a")
LIGHT_GRAY = colors.HexColor("#f5f5f5")
MID_GRAY = colors.HexColor("#666666")
LINK_COLOR = colors.HexColor("#1a56db")

def build_cv(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    )

    styles = getSampleStyleSheet()

    name_style = ParagraphStyle("name", fontSize=26, textColor=NAVY, fontName="Helvetica-Bold",
                                spaceAfter=2, leading=30)
    title_style = ParagraphStyle("title", fontSize=11, textColor=MID_GRAY, fontName="Helvetica",
                                 spaceAfter=4, leading=14, letterSpacing=1.5)
    contact_style = ParagraphStyle("contact", fontSize=9, textColor=MID_GRAY, fontName="Helvetica",
                                   spaceAfter=2, leading=12)
    section_style = ParagraphStyle("section", fontSize=10, textColor=colors.white, fontName="Helvetica-Bold",
                                   spaceAfter=0, leading=14, leftIndent=4)
    job_title_style = ParagraphStyle("job_title", fontSize=11, textColor=NAVY, fontName="Helvetica-Bold",
                                     spaceAfter=1, leading=14)
    job_date_style = ParagraphStyle("job_date", fontSize=9, textColor=MID_GRAY, fontName="Helvetica-Oblique",
                                    spaceAfter=4, leading=12)
    bullet_style = ParagraphStyle("bullet", fontSize=9.5, textColor=colors.black, fontName="Helvetica",
                                  spaceAfter=2, leading=13, leftIndent=12, bulletIndent=2)
    skills_label_style = ParagraphStyle("skills_label", fontSize=9.5, textColor=NAVY, fontName="Helvetica-Bold",
                                        spaceAfter=2, leading=13)
    skills_val_style = ParagraphStyle("skills_val", fontSize=9.5, textColor=colors.black, fontName="Helvetica",
                                      spaceAfter=6, leading=13)
    edu_style = ParagraphStyle("edu", fontSize=10, textColor=NAVY, fontName="Helvetica-Bold",
                               spaceAfter=1, leading=13)
    edu_sub_style = ParagraphStyle("edu_sub", fontSize=9.5, textColor=MID_GRAY, fontName="Helvetica",
                                   spaceAfter=0, leading=12)

    def section_header(text):
        table = Table([[Paragraph(text, section_style)]], colWidths=[doc.width])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), NAVY),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ]))
        return table

    story = []

    # Header block
    story.append(Paragraph("FRANCISCO BARBERIS", name_style))
    story.append(Paragraph("LAW FIRM SEO SPECIALIST", title_style))
    story.append(Paragraph(
        'franciscobarberiss@gmail.com &nbsp;|&nbsp; +54 29444 538946 &nbsp;|&nbsp; '
        '<a href="https://drive.google.com/drive/u/3/folders/1os-ZbsK1CI9UUji8tLAUt1wGCrk-cbKC" '
        'color="#1a56db">Portfolio</a>',
        contact_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceAfter=8, spaceBefore=6))

    # Summary
    summary_text = (
        "Marketing professional with 7+ years of hands-on experience driving digital growth for e-commerce brands "
        "and law firms. Skilled in legal SEO strategy, content planning, keyword research, link acquisition, technical "
        "optimization, and local visibility initiatives for attorneys. Proven success improving organic traffic and lead "
        "generation through high-quality legal content, on-page optimization, and GMB/local SEO improvements. Founder "
        "of a successful mountain-inspired clothing brand with 2,500+ online sales and 30K followers, with additional "
        "expertise in paid ads, email marketing, brand management, and cross-team collaboration."
    )
    summary_style = ParagraphStyle("summary", fontSize=9.5, textColor=colors.black, fontName="Helvetica",
                                   spaceAfter=10, leading=14)
    story.append(Paragraph(summary_text, summary_style))

    # Work Experience
    story.append(section_header("WORK EXPERIENCE"))
    story.append(Spacer(1, 6))

    jobs = [
        {
            "title": "Chief Marketing Officer — Lange Firm (Employment Law Firm)",
            "date": "Nov 2024 – Present",
            "bullets": [
                "Coordinated digital marketing initiatives including content creation and scheduling, email campaigns, website updates, and Google Business Profile optimization.",
                "Managed SEO and website improvements by overseeing blog publishing, internal linking, metadata updates, and performance tracking.",
                "Conducted backlink outreach, reporting, and competitor monitoring.",
                "Collaborated with attorneys and internal stakeholders to align marketing content with firm messaging and client needs.",
                "Managed email marketing campaigns via Mailchimp, achieving an 18% open rate.",
                "Produced and edited video content using CapCut for social media and firm promotion.",
            ],
        },
        {
            "title": "Project Manager — Claura AI",
            "date": "Nov 2025 – Present",
            "bullets": [
                "Managed client onboarding and end-to-end project coordination for AI-powered content services.",
                "Automated content generation and scheduling workflows for clients using Claude AI, HeyGen, Adloop, and Notion — producing assets ranging from stories to Reels.",
                "Served as primary client contact, ensuring delivery timelines and content quality standards were met.",
            ],
        },
        {
            "title": 'Director — "Bonacera" Mountain-Inspired Clothing Brand',
            "date": "Jan 2022 – Present",
            "bullets": [
                "Built and scaled a mountain-inspired e-commerce brand to 30,000+ social media followers and 2,500+ online sales.",
                "Managed social media content planning, posting schedules, and brand messaging.",
                "Coordinated and executed Meta Ads campaigns, promotions, and product launches.",
                "Oversaw website updates, product listings, customer communication, and analytics tracking.",
            ],
        },
        {
            "title": "Contract Development Analyst — MetLife Chile & Uruguay",
            "date": "2021 – 2022",
            "bullets": [
                "Drafted and negotiated contracts and amendments with vendors.",
                "Streamlined contract processes and implemented workflow improvements.",
                "Managed procurement operations via ARIBA and produced daily reports.",
            ],
        },
        {
            "title": "Business Support & Contract Analyst — Roche Argentina",
            "date": "2018 – 2022",
            "bullets": [
                "Joined as intern and advanced to main contract touchpoint owner for the Diagnostics division.",
                "Drafted and negotiated contracts with clients and provided legal advice on contract matters.",
                "Led Agiloft implementation for contract lifecycle management.",
                "Managed commercial procurement in SAP and produced monthly performance reports.",
            ],
        },
    ]

    for job in jobs:
        story.append(Paragraph(job["title"], job_title_style))
        story.append(Paragraph(job["date"], job_date_style))
        for b in job["bullets"]:
            story.append(Paragraph(f"• {b}", bullet_style))
        story.append(Spacer(1, 8))

    # Education
    story.append(section_header("EDUCATION"))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Law Degree", edu_style))
    story.append(Paragraph("University of Buenos Aires (UBA)", edu_sub_style))
    story.append(Spacer(1, 10))

    # Skills
    story.append(section_header("SKILLS"))
    story.append(Spacer(1, 6))

    skill_sections = [
        ("SEO & Content", "On-Page Optimization · Backlink Building · Technical SEO · Keyword Research · Blog & Legal Content Creation · Google Business Profile Optimization · Local SEO"),
        ("Digital Marketing", "Email Marketing (Mailchimp) · Paid Ads (Meta/Facebook) · Social Media Management · Website Content Management · Reporting & Performance Tracking"),
        ("Tools & Technology", "Claude AI · HeyGen · Adloop · Notion · CapCut · SAP · ARIBA · Agiloft"),
        ("Other", "Project Management · Client Onboarding · Cross-team Collaboration · Brand Management"),
    ]

    for label, val in skill_sections:
        story.append(Paragraph(label, skills_label_style))
        story.append(Paragraph(val, skills_val_style))

    doc.build(story)
    print(f"PDF saved to {output_path}")

if __name__ == "__main__":
    build_cv("/home/user/Vuelta-rapida/Francisco_Barberis_CV.pdf")
