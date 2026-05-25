import os
import json
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")
PDF_PATH = os.path.join(BASE_DIR, "Manik_Chaudhary_Test_Lead_V1.pdf")

# =========================================================================
# PDF-ONLY HARDCODED CONTENT CONFIGURATIONS (Exposed here for easy updates)
# =========================================================================

# 1. Custom Professional Title (overrides hero.title from JSON in the PDF only)
OVERRIDE_TITLE = "Lead QA | AI-Assisted Test Automation Expert"

# 2. Custom Intro Summary Paragraph (overrides the 1st summary paragraph from JSON in the PDF only)
OVERRIDE_SUMMARY = (
    "Passionate Lead QA specializing in building enterprise-grade test automation frameworks and pioneering "
    "AI-assisted testing solutions. Experienced in leveraging machine learning and artificial intelligence to power "
    "intelligent test case generation, self-healing selectors, and predictive analytics that drive autonomous "
    "continuous testing."
)

# 3. PDF-Only Certifications (hardcoded directly in the PDF certifications section)
PDF_ONLY_CERTIFICATIONS = [
    {
        "title": "SAFe 5.0 Practitioner",
        "issuer": "Scaled Agile"
    }
]







def clean_html_tags(text):
    """
    Ensure only valid ReportLab HTML tags are used.
    ReportLab supports <b>, <i>, <u>, <font>, <strong>, <em> etc.
    We convert <strong> to <b> just in case.
    """
    if not text:
        return ""
    text = text.replace("<strong>", "<b>").replace("</strong>", "</b>")
    text = text.replace("<em>", "<i>").replace("</em>", "</i>")
    return text

def draw_line(color=colors.HexColor("#CBD5E0"), thickness=1, space_after=6):
    """
    Draws a clean, robust horizontal line using a ReportLab Table.
    """
    t = Table([['']], colWidths=[540], rowHeights=[thickness])
    t.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, -1), thickness, color),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    return t



def build_pdf():
    # Load JSON data
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Document Setup - 0.5 inch margins (36 pt)
    # Printable area: Width = 612 - 72 = 540 pt, Height = 792 - 72 = 720 pt
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=24,
        bottomMargin=24
    )

    story = []

    # Color Palette
    primary_color = colors.HexColor("#1A365D")  # Slate/Navy
    accent_color = colors.HexColor("#2B6CB0")   # Accent Blue
    text_color = colors.HexColor("#2D3748")     # Charcoal Text
    light_bg = colors.HexColor("#F7FAFC")       # Off-white / light grey
    border_color = colors.HexColor("#E2E8F0")   # Border grey

    # Setup Custom Styles
    styles = getSampleStyleSheet()

    # Modify existing styles to avoid conflicts
    title_style = ParagraphStyle(
        'CVTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary_color,
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        'CVSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=accent_color,
        alignment=TA_CENTER,
        spaceAfter=6
    )

    contact_style = ParagraphStyle(
        'CVContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#4A5568"),
        alignment=TA_CENTER
    )

    section_heading = ParagraphStyle(
        'CVSectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.white,
        backColor=primary_color,
        borderPadding=4.5,
        leftIndent=-5,
        rightIndent=-5,
        spaceBefore=10,
        spaceAfter=12,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'CVBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=text_color,
        alignment=TA_LEFT
    )

    bullet_style = ParagraphStyle(
        'CVBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=text_color,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=0.5
    )

    # 1. HEADER SECTION (Name, Title, Contact Info)
    hero = data.get("hero", {})
    contact = data.get("contact", {})

    story.append(Paragraph(hero.get("name", "Manik Chaudhary"), title_style))
    story.append(Spacer(1, 2))
    
    # Use override title if defined, else fallback to JSON
    pdf_title = OVERRIDE_TITLE if OVERRIDE_TITLE else hero.get("title", "")
    story.append(Paragraph(pdf_title, subtitle_style))

    # Format contact info beautifully on a single line
    clean_email = contact.get("email", "")
    clean_phone = contact.get("phone", "")
    clean_location = contact.get("location", "")
    
    # Strip URL prefixes for print clean display
    linkedin_url = contact.get("linkedin", "")
    github_url = contact.get("github", "")
    portfolio_url = contact.get("portfolio", "https://manik1441.github.io/CV_2.0/")
    clean_linkedin = linkedin_url.replace("https://", "").replace("www.", "")
    clean_github = github_url.replace("https://", "").replace("www.", "")
    clean_portfolio = portfolio_url.replace("https://", "").replace("www.", "")

    contact_text = f"<b>Email:</b> <a href=\"mailto:{clean_email}\"><font color=\"#2B6CB0\">{clean_email}</font></a>  |  <b>Phone:</b> {clean_phone}  |  <b>Location:</b> {clean_location}<br/><b>LinkedIn:</b> <a href=\"{linkedin_url}\"><font color=\"#2B6CB0\">{clean_linkedin}</font></a>  |  <b>GitHub:</b> <a href=\"{github_url}\"><font color=\"#2B6CB0\">{clean_github}</font></a>  |  <b>Portfolio:</b> <a href=\"{portfolio_url}\"><font color=\"#2B6CB0\">{clean_portfolio}</font></a>"
    story.append(Paragraph(contact_text, contact_style))
    story.append(Spacer(1, 2))
    story.append(draw_line(primary_color, thickness=1.5))
    story.append(Spacer(1, 1))

    # 2. PROFESSIONAL SUMMARY
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
    summary_p = hero.get("paragraphs", [])
    
    # Apply override for first summary paragraph if configured
    if OVERRIDE_SUMMARY:
        summary_paragraphs = [OVERRIDE_SUMMARY] + summary_p[1:]
    else:
        summary_paragraphs = summary_p
        
    full_summary = " ".join(summary_paragraphs)
    story.append(Paragraph(clean_html_tags(full_summary), body_style))
    story.append(Spacer(1, 4))
    story.append(draw_line())

    # 3. CORE EXPERTISE & TECHNICAL SKILLS
    story.append(Paragraph("CORE EXPERTISE & TECHNICAL SKILLS", section_heading))
    
    # Let's compile a list of skill categories that are high impact
    # We will format this into a highly structured table to save vertical space.
    skills_data = []
    
    # We will group and map some subcategories dynamically
    skills_map = {}
    for cat in data.get("skills", []):
        for sub in cat.get("subcategories", []):
            name = sub.get("name", "")
            items = ", ".join(sub.get("items", []))
            
            # Group or clean names slightly
            if "AI" in name or "ML" in name or "Agentic" in name:
                skills_map["AI, ML & Generative AI"] = skills_map.get("AI, ML & Generative AI", []) + sub.get("items", [])
            elif "Programming" in name or "Scripting" in name:
                skills_map["Languages"] = skills_map.get("Languages", []) + sub.get("items", [])
            elif "Frameworks" in name:
                skills_map["Test Frameworks"] = skills_map.get("Test Frameworks", []) + sub.get("items", [])
            elif "CI/CD" in name or "DevOps" in name:
                skills_map["CI/CD & DevOps"] = skills_map.get("CI/CD & DevOps", []) + sub.get("items", [])
            elif "Data" in name or "Cloud" in name:
                skills_map["Cloud, Data & DB"] = skills_map.get("Cloud, Data & DB", []) + sub.get("items", [])
            elif "Testing & Automation" in name or "Quality Engineering" in name:
                skills_map["Testing & Quality Eng."] = skills_map.get("Testing & Quality Eng.", []) + sub.get("items", [])
            elif "Management" in name or "Leadership" in name or "Soft Skills" in name:
                skills_map["Leadership & Practices"] = skills_map.get("Leadership & Practices", []) + sub.get("items", [])
            else:
                skills_map[name] = sub.get("items", [])

    # Order the skills logically
    skills_order = [
        "Languages",
        "Test Frameworks",
        "AI, ML & Generative AI",
        "Testing & Quality Eng.",
        "Cloud, Data & DB",
        "CI/CD & DevOps",
        "Leadership & Practices"
    ]

    skill_cell_label_style = ParagraphStyle(
        'SkillCellLabel', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10, textColor=text_color
    )
    skill_cell_items_style = ParagraphStyle(
        'SkillCellItems', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10, textColor=text_color
    )

    skill_rows = []
    for cat_name in skills_order:
        items_list = skills_map.get(cat_name, [])
        if not items_list:
            continue
        # Remove duplicates while preserving order
        seen = set()
        items_clean = [x for x in items_list if not (x in seen or seen.add(x))]
        items_str = ", ".join(items_clean)
        
        # Paragraphs to allow auto-wrap
        p_label = Paragraph(cat_name, skill_cell_label_style)
        p_items = Paragraph(items_str, skill_cell_items_style)
        skill_rows.append([p_label, p_items])

    # Table layout for skills (Widths: 130pt, 410pt)
    skills_table = Table(skill_rows, colWidths=[130, 410])
    skills_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#2D3748")), # Exact solid dark charcoal borders
    ]))
    
    story.append(skills_table)
    story.append(Spacer(1, 4))
    story.append(draw_line())

    # 4. PROFESSIONAL EXPERIENCE
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_heading))

    role_title_style = ParagraphStyle(
        'RoleTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, leading=11.5, textColor=primary_color
    )
    company_style = ParagraphStyle(
        'Company', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, leading=11.5, textColor=accent_color
    )
    duration_style = ParagraphStyle(
        'Duration', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8.5, leading=11, textColor=colors.HexColor("#4A5568"), alignment=TA_RIGHT
    )

    experiences = data.get("experience", [])
    
    # We will build and render experience items.
    # To keep Page 1 perfectly balanced, we will place EPAM Systems and S&P Global on Page 1, 
    # and Guardian India + SoftTech India on Page 2.
    for index, exp in enumerate(experiences):
        role_p = Paragraph(f"<b>{exp.get('role', '')}</b>", role_title_style)
        company_name = exp.get("company", "").replace("&", "&amp;")
        company_p = Paragraph(company_name, company_style)
        duration_p = Paragraph(exp.get("duration", ""), duration_style)
        
        # We place them in a single borderless table to ensure perfect alignment
        header_table = Table([[role_p, ''], [company_p, duration_p]], colWidths=[380, 160])
        header_table.setStyle(TableStyle([
            ('SPAN', (0, 0), (1, 0)), # Span the role title across both columns
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        exp_flowables = [
            Spacer(1, 2),
            header_table,
            Spacer(1, 2)
        ]
        
        for detail in exp.get("details", []):
            bullet_text = f"&bull; {clean_html_tags(detail)}"
            exp_flowables.append(Paragraph(bullet_text, bullet_style))
            
        story.append(KeepTogether(exp_flowables))
        
        # Page break logic: Split exactly after the first two experiences (EPAM & S&P Global)
        # to ensure that Page 1 does not overflow and Page 2 holds the remaining content.
        if index == 1:
            story.append(PageBreak())

    story.append(Spacer(1, 4))
    story.append(draw_line())

    # PAGE 2 CONTINUES
    # 5. KEY PROJECTS
    story.append(Paragraph("KEY PROJECTS", section_heading))
    
    # We'll render 2 Professional and 2 Personal high-impact projects
    # to maintain high density but fit on Page 2 beautifully.
    proj_title_style = ParagraphStyle(
        'ProjTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10.5, textColor=primary_color
    )
    proj_role_style = ParagraphStyle(
        'ProjRole', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.5, leading=9.5, textColor=accent_color
    )
    proj_desc_style = ParagraphStyle(
        'ProjDesc', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=9.5, textColor=text_color
    )
    proj_sub_style = ParagraphStyle(
        'ProjSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=primary_color, leftIndent=4, spaceBefore=4, spaceAfter=2
    )

    project_list = []
    
    # 1. Professional: Google GGRC
    prof_projects = data.get("projects", {}).get("professional", [])
    if prof_projects:
        ggrc = prof_projects[0]
        project_list.append((ggrc.get("title"), ggrc.get("role"), ggrc.get("description"), None))
    
    # 2. Professional: Amazon PLOA
    if len(prof_projects) > 1:
        ploa = prof_projects[1]
        project_list.append((ploa.get("title"), ploa.get("role"), ploa.get("description"), None))

    # 3. Personal: Agentic AI-Powered TDM
    pers_projects = data.get("projects", {}).get("personal", [])
    for p in pers_projects:
        if "TDM" in p.get("title", "") or "Agentic" in p.get("title", ""):
            project_list.append((p.get("title"), p.get("role"), p.get("description"), p.get("github")))
            break
            
    # 4. Personal: AI-Assisted Test Automation Framework
    for p in pers_projects:
        if "Assisted" in p.get("title", "") or "AI-Assisted" in p.get("title", ""):
            project_list.append((p.get("title"), p.get("role"), p.get("description"), p.get("github")))
            break

    # Build an elegant 2x2 grid for projects to save space
    proj_cells = []
    for title, role, desc, git_url in project_list:
        title_markup = f"<b>{title}</b>"
        if git_url:
            title_markup += f" &nbsp;<a href=\"{git_url}\"><font color=\"#2B6CB0\"><b>[Link]</b></font></a>"
        p_cell = [
            Paragraph(title_markup, proj_title_style),
            Paragraph(f"Role: {role}", proj_role_style),
            Spacer(1, 1),
            Paragraph(desc, proj_desc_style),
            Spacer(1, 4)
        ]
        proj_cells.append(p_cell)

    # Layout: Two columns of projects, with spanning headers to differentiate Professional and Personal sections
    proj_table_data = [
        [Paragraph("Professional Projects", proj_sub_style), '', ''],
        [proj_cells[0], '', proj_cells[1]],
        ['', '', ''],
        [Paragraph("Personal Projects", proj_sub_style), '', ''],
        [proj_cells[2], '', proj_cells[3]]
    ]
    
    proj_table = Table(proj_table_data, colWidths=[260, 20, 260])
    proj_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (2, 0)), # Span "Professional Projects" header across columns
        ('SPAN', (0, 3), (2, 3)), # Span "Personal Projects" header across columns
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EBF8FF")), # Continuous light blue background line for Professional
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor("#EBF8FF")), # Continuous light blue background line for Personal
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 2.5),
        ('TOPPADDING', (0, 0), (-1, 0), 2.5),
        ('BOTTOMPADDING', (0, 3), (-1, 3), 2.5),
        ('TOPPADDING', (0, 3), (-1, 3), 2.5),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 0),
        ('TOPPADDING', (0, 1), (-1, 1), 3),
        ('BOTTOMPADDING', (0, 4), (-1, 4), 0),
        ('TOPPADDING', (0, 4), (-1, 4), 3),
        ('BOTTOMPADDING', (0, 2), (-1, 2), 0),
        ('TOPPADDING', (0, 2), (-1, 2), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    story.append(proj_table)
    story.append(Spacer(1, 4))
    story.append(draw_line())

    # 6. CERTIFICATIONS
    story.append(Paragraph("PROFESSIONAL CERTIFICATIONS", section_heading))
    
    cert_item_style = ParagraphStyle(
        'CertItem', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10, textColor=text_color
    )
    
    # We will arrange certifications in an elegant 2-column or 3-column table
    certifications = data.get("certifications", [])
    cert_cells = []
    for c in certifications:
        title = c.get("title", "")
        issuer = c.get("issuer", "")
        cert_cells.append(Paragraph(f"&bull; <b>{title}</b> ({issuer})", cert_item_style))
        
    # Hardcode SAFe 5.0 Practitioner directly in the PDF representation (PDF-only display)
    for c in PDF_ONLY_CERTIFICATIONS:
        title = c.get("title", "")
        issuer = c.get("issuer", "")
        cert_cells.append(Paragraph(f"&bull; <b>{title}</b> ({issuer})", cert_item_style))
        
    # Standardize to 2 columns (Widths: 270pt, 270pt)
    cert_rows = []
    for idx in range(0, len(cert_cells), 2):
        col1 = cert_cells[idx]
        col2 = cert_cells[idx+1] if idx+1 < len(cert_cells) else ''
        cert_rows.append([col1, col2])
        
    cert_table = Table(cert_rows, colWidths=[270, 270])
    cert_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    story.append(cert_table)
    story.append(Spacer(1, 4))
    story.append(draw_line())

    # 7. EDUCATION
    story.append(Paragraph("EDUCATION", section_heading))
    
    edu_degree_style = ParagraphStyle(
        'EduDegree', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=primary_color
    )
    edu_detail_style = ParagraphStyle(
        'EduDetail', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11, textColor=text_color
    )
    edu_year_style = ParagraphStyle(
        'EduYear', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8.5, leading=11, textColor=colors.HexColor("#4A5568"), alignment=TA_RIGHT
    )
    
    education = data.get("education", [])
    if education:
        edu = education[0]
        deg_p = Paragraph(edu.get("degree", ""), edu_degree_style)
        coll_p = Paragraph(f"{edu.get('college', '')} &nbsp;|&nbsp; <i>{edu.get('location', '')}</i>", edu_detail_style)
        year_p = Paragraph(f"Graduated: {edu.get('year', '')}", edu_year_style)
        
        edu_table = Table([[coll_p, year_p]], colWidths=[420, 120])
        edu_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        story.append(deg_p)
        story.append(edu_table)

    # Build the document
    doc.build(story)
    print("SUCCESS: Beautiful 2-Page Executive Resume PDF has been generated!")

if __name__ == "__main__":
    build_pdf()
