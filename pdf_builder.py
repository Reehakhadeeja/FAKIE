import io
import streamlit as st


try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.platypus.flowables import HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    REPORTLAB_OK = True
except ImportError:
    REPORTLAB_OK = False

def build_pdf() -> bytes:
    if not REPORTLAB_OK:
        return b""
    buf = io.BytesIO()
    ss  = st.session_state
    
    C_NAME   = colors.HexColor("#1e293b")
    C_CONT   = colors.HexColor("#64748b")
    C_HR     = colors.HexColor("#3b82f6")
    C_SEC    = colors.HexColor("#1e293b")
    C_SEC_HR = colors.HexColor("#f1f5f9")
    C_TITLE  = colors.HexColor("#0f172a")
    C_SUB    = colors.HexColor("#3b82f6")
    C_DATE   = colors.HexColor("#94a3b8")
    C_DESC   = colors.HexColor("#334155")
    C_CHIP_T = colors.HexColor("#1d4ed8")

    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm)
    bs  = getSampleStyleSheet()
    def sty(name, **kw): return ParagraphStyle(name, parent=bs["Normal"], **kw)
    
    # Removed all spaceAfter/spaceBefore and explicit leadings from styles to prevent unpredictable overlaps
    s_name  = sty("N", fontSize=24, textColor=C_NAME, fontName="Helvetica-Bold", leading=28)
    s_cont  = sty("C", fontSize=9,  textColor=C_CONT, leading=12)
    s_sec   = sty("S", fontSize=11, textColor=C_SEC,  fontName="Helvetica-Bold", leading=14)
    s_sum   = sty("Su",fontSize=9.5,textColor=C_DESC, leading=14)
    s_title = sty("T", fontSize=10, fontName="Helvetica-Bold", textColor=C_TITLE, leading=12)
    s_sub   = sty("Sb",fontSize=9,  textColor=C_SUB,  fontName="Helvetica-Bold", leading=12)
    s_date  = sty("D", fontSize=8.5,textColor=C_DATE, alignment=2, leading=12)
    s_desc  = sty("De",fontSize=9.5,textColor=C_DESC, leading=14)
    s_chip  = sty("Ch",fontSize=9, textColor=C_CHIP_T, leading=12)

    story   = []
    
    # Using explicit Spacers everywhere to guarantee separation
    story.append(Paragraph(ss.rb_name or "Your Name", s_name))
    story.append(Spacer(1, 6))
    
    parts = [p for p in [ss.rb_email, ss.rb_phone, ss.rb_location, ss.rb_linkedin] if p.strip()]
    if parts: 
        story.append(Paragraph("    ".join(parts), s_cont))
        story.append(Spacer(1, 8))
        
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_HR, spaceBefore=0, spaceAfter=0))
    story.append(Spacer(1, 14))
    
    if ss.rb_summary.strip():
        story.append(Paragraph("PROFESSIONAL SUMMARY", s_sec))
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", thickness=1.5, color=C_SEC_HR, spaceBefore=0, spaceAfter=0))
        story.append(Spacer(1, 8))
        story.append(Paragraph(ss.rb_summary, s_sum))
        story.append(Spacer(1, 14))
        
    valid_exp = [e for e in ss.rb_experience if e["title"].strip() or e["company"].strip()]
    if valid_exp:
        story.append(Paragraph("WORK EXPERIENCE", s_sec))
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", thickness=1.5, color=C_SEC_HR, spaceBefore=0, spaceAfter=0))
        story.append(Spacer(1, 8))
        for e in valid_exp:
            row = Table([[Paragraph(e["title"],s_title), Paragraph(e["duration"],s_date)]], colWidths=["75%","25%"])
            row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
            story.append(row)
            story.append(Spacer(1, 4))
            if e["company"]:
                story.append(Paragraph(e["company"], s_sub))
                story.append(Spacer(1, 4))
            if e["description"]:
                story.append(Paragraph(e["description"].replace("\n","<br/>"), s_desc))
            story.append(Spacer(1, 12))
            
    valid_edu = [e for e in ss.rb_education if e["institution"].strip() or e["degree"].strip()]
    if valid_edu:
        story.append(Paragraph("EDUCATION", s_sec))
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", thickness=1.5, color=C_SEC_HR, spaceBefore=0, spaceAfter=0))
        story.append(Spacer(1, 8))
        for e in valid_edu:
            row = Table([[Paragraph(e["degree"],s_title), Paragraph(e["year"],s_date)]], colWidths=["75%","25%"])
            row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
            story.append(row)
            story.append(Spacer(1, 4))
            if e["institution"]:
                story.append(Paragraph(e["institution"], s_sub))
                story.append(Spacer(1, 4))
            if e["grade"]:
                story.append(Paragraph(f"GPA: {e['grade']}", s_desc))
            story.append(Spacer(1, 12))
            
    valid_proj = [p for p in ss.rb_projects if p["name"].strip()]
    if valid_proj:
        story.append(Paragraph("PROJECTS", s_sec))
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", thickness=1.5, color=C_SEC_HR, spaceBefore=0, spaceAfter=0))
        story.append(Spacer(1, 8))
        for p in valid_proj:
            story.append(Paragraph(p["name"], s_title))
            story.append(Spacer(1, 4))
            if p["tech"]:
                story.append(Paragraph(p["tech"], s_sub))
                story.append(Spacer(1, 4))
            if p["description"]:
                story.append(Paragraph(p["description"].replace("\n","<br/>"), s_desc))
                story.append(Spacer(1, 4))
            if p["link"]:
                story.append(Paragraph(f'<link href="{p["link"]}" color="#1d4ed8">{p["link"]}</link>', s_desc))
            story.append(Spacer(1, 12))

    valid_certs = [c for c in ss.get("rb_certifications",[]) if c["name"].strip()]
    if valid_certs:
        story.append(Paragraph("CERTIFICATIONS", s_sec))
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", thickness=1.5, color=C_SEC_HR, spaceBefore=0, spaceAfter=0))
        story.append(Spacer(1, 8))
        for c in valid_certs:
            row = Table([[Paragraph(c["name"],s_title), Paragraph(c["year"],s_date)]], colWidths=["75%","25%"])
            row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
            story.append(row)
            story.append(Spacer(1, 4))
            if c["issuer"]:
                story.append(Paragraph(c["issuer"], s_sub))
            story.append(Spacer(1, 12))

    valid_skills = [sk for sk in ss.rb_skills if sk["items"].strip()]
    if valid_skills:
        story.append(Paragraph("SKILLS", s_sec))
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", thickness=1.5, color=C_SEC_HR, spaceBefore=0, spaceAfter=0))
        story.append(Spacer(1, 8))
        for sk in valid_skills:
            label = f"<b>{sk['category']}:</b>  " if sk["category"] else ""
            story.append(Paragraph(label + sk["items"], s_chip))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 6))
            
    langs = ss.get("rb_languages","").strip()
    if langs:
        story.append(Paragraph("LANGUAGES", s_sec))
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", thickness=1.5, color=C_SEC_HR, spaceBefore=0, spaceAfter=0))
        story.append(Spacer(1, 8))
        story.append(Paragraph(langs, s_desc))
        story.append(Spacer(1, 12))
        
    ach = ss.get("rb_achievements","").strip()
    if ach:
        story.append(Paragraph("ACHIEVEMENTS & AWARDS", s_sec))
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", thickness=1.5, color=C_SEC_HR, spaceBefore=0, spaceAfter=0))
        story.append(Spacer(1, 8))
        story.append(Paragraph(ach.replace("\n","<br/>"), s_desc))
        story.append(Spacer(1, 12))
        
    doc.build(story)
    return buf.getvalue()


# ── Sidebar ───────────────────────────────────────────────────────────────────
