from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

NAVY = colors.HexColor("#1a2e4a")
MID_GRAY = colors.HexColor("#555555")
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

    name_style = ParagraphStyle("name", fontSize=26, textColor=NAVY, fontName="Helvetica-Bold",
                                spaceAfter=2, leading=30)
    title_style = ParagraphStyle("title", fontSize=11, textColor=MID_GRAY, fontName="Helvetica",
                                 spaceAfter=4, leading=14)
    contact_style = ParagraphStyle("contact", fontSize=9.5, textColor=MID_GRAY, fontName="Helvetica",
                                   spaceAfter=2, leading=13)
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
    summary_style = ParagraphStyle("summary", fontSize=9.5, textColor=colors.black, fontName="Helvetica",
                                   spaceAfter=10, leading=14)

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

    # Header
    story.append(Paragraph("FRANCISCO BARBERIS", name_style))
    story.append(Paragraph("Law Firm SEO &amp; Digital Marketing Specialist", title_style))
    story.append(Paragraph(
        'franciscobarberiss@gmail.com &nbsp;|&nbsp; '
        '<a href="https://drive.google.com/drive/u/3/folders/1os-ZbsK1CI9UUji8tLAUt1wGCrk-cbKC" '
        'color="#1a56db"><u>[ Click here to view Portfolio ]</u></a>',
        contact_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceAfter=8, spaceBefore=6))

    # Summary
    story.append(Paragraph(
        "Results-driven digital marketing and SEO specialist with 7+ years of experience driving measurable growth "
        "for law firms and e-commerce brands. Proven track record in legal SEO strategy, content marketing, local "
        "search optimization, and full-funnel digital marketing execution. Grew a law firm's organic traffic from "
        "zero to <b>9,000+ monthly visits</b> and elevated its Google Business Profile ranking to <b>top-ranked "
        "employment law firm in the region</b>. Adept at managing all aspects of digital marketing independently — "
        "from technical SEO audits and content strategy to paid media, email campaigns, and social media. "
        "Hands-on experience with AI-powered content automation tools and a strong foundation in legal terminology "
        "from a Law degree.",
        summary_style
    ))

    # Work Experience
    story.append(section_header("WORK EXPERIENCE"))
    story.append(Spacer(1, 6))

    jobs = [
        {
            "title": "Chief Marketing Officer — Lange Firm (Employment Law Firm) · Houston, TX",
            "date": "Nov 2024 – Present",
            "bullets": [
                "<b>Grew organic traffic from 0 to 9,000+ monthly visits</b> by building and executing a full content marketing and blog strategy from scratch, targeting high-intent legal keywords.",
                "<b>Elevated the firm to the top-ranked employment law firm in Sugar Land, TX</b> on Google Maps through a comprehensive GMB optimization and migration strategy.",
                "<b>Built the firm's Google review presence from the ground up</b>, implementing a structured review generation strategy that significantly increased local authority and credibility.",
                "Serve as the sole marketing professional for the firm, owning all digital marketing operations end-to-end: SEO, content, email, social media, paid ads, and video.",
                "Conduct technical SEO audits using Screaming Frog and Google Search Console, identifying and resolving site issues to improve crawlability and Core Web Vitals.",
                "Perform keyword research and competitive analysis using SEMrush/Ahrefs to inform content strategy and on-page optimization.",
                "Monitor and report on performance via Google Analytics (GA4) and Search Console, tracking KPIs and adjusting strategy accordingly.",
                "Implement <b>Answer Engine Optimization (AEO)</b> and <b>Generative Engine Optimization (GEO)</b> strategies — including FAQ schema markup, E-E-A-T signals, and question-based content formats — to maximize visibility in AI-generated results (Google AI Overviews, ChatGPT, Perplexity).",
                "Manage email marketing campaigns via Mailchimp, achieving an <b>18% open rate</b>.",
                "Oversee WordPress website: blog publishing, internal linking, metadata, and on-page SEO.",
                "Run Google Ads and Meta Ads campaigns to support lead generation alongside organic efforts.",
                "Produce and edit video content using CapCut and design assets in Canva for social media and firm promotion.",
                "Collaborate directly with attorneys to ensure all content aligns with legal accuracy and client acquisition goals.",
            ],
        },
        {
            "title": "Project Manager — Claura AI",
            "date": "Nov 2025 – Present",
            "bullets": [
                "Manage client onboarding and end-to-end project coordination for AI-powered content services.",
                "Automate content generation and scheduling workflows using Claude AI, HeyGen, Adloop, and Notion — producing high-volume assets including stories and Reels at scale.",
                "Serve as primary client contact, ensuring delivery timelines, quality standards, and campaign goals are consistently met.",
            ],
        },
        {
            "title": '"Bonacera" Mountain-Inspired Clothing Brand — Founder & Director',
            "date": "Jan 2022 – Present",
            "bullets": [
                "Built and scaled an e-commerce brand to <b>30,000+ social media followers and 2,500+ online sales</b>.",
                "Developed and executed full digital marketing strategy: content planning, social media, and brand identity.",
                "Ran Meta Ads campaigns, promotions, and product launches driving consistent revenue growth.",
                "Managed website operations, product listings, customer communication, and analytics tracking.",
            ],
        },
        {
            "title": "Contract Analyst — Roche Argentina & MetLife",
            "date": "2018 – 2022",
            "bullets": [],
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
        ("SEO & AEO", "On-Page SEO · Technical SEO · Local SEO · Answer Engine Optimization (AEO) · Generative Engine Optimization (GEO) · AI Search Optimization · Keyword Research · Backlink Building · Google Business Profile (GMB) · Schema Markup (FAQ, LegalService, Attorney) · Core Web Vitals · E-E-A-T · Featured Snippets · Topical Authority Building"),
        ("Analytics & Tools", "Google Analytics (GA4) · Google Search Console · SEMrush · Ahrefs · Screaming Frog · Google Ads"),
        ("Content & Marketing", "Content Marketing · Blog Writing · Legal Content Creation · Email Marketing (Mailchimp) · Social Media Management · Meta Ads (Facebook/Instagram) · Video Editing (CapCut) · Canva"),
        ("Platforms & Tech", "WordPress · Notion · Claude AI · HeyGen · Adloop"),
        ("Other", "Independent Work · Client Communication · Project Management · Reporting & KPI Tracking · Cross-team Collaboration"),
    ]

    for label, val in skill_sections:
        story.append(Paragraph(label, skills_label_style))
        story.append(Paragraph(val, skills_val_style))

    doc.build(story)
    print(f"PDF saved to {output_path}")

if __name__ == "__main__":
    build_cv("/home/user/Vuelta-rapida/Francisco_Barberis_CV.pdf")
