import io
import streamlit as st
def build_pdf() -> bytes:
    if not REPORTLAB_OK:
        return b""
    buf = io.BytesIO()
    ss  = st.session_state
    G_DARK  = colors.HexColor("#1b5e20")
    G_MID   = colors.HexColor("#2e7d32")
    G_LIGHT = colors.HexColor("#e8f5e9")
    GREY    = colors.HexColor("#555")
    LGREY   = colors.HexColor("#888")
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm)
    bs  = getSampleStyleSheet()
    def sty(name, **kw): return ParagraphStyle(name, parent=bs["Normal"], **kw)
    s_name  = sty("N", fontSize=22, textColor=G_DARK,  fontName="Helvetica-Bold", spaceAfter=2)
    s_cont  = sty("C", fontSize=8,  textColor=GREY,    spaceAfter=4, leading=12)
    s_sec   = sty("S", fontSize=10, textColor=G_MID,   fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=3, leading=13)
    s_sum   = sty("Su",fontSize=9,  textColor=GREY,    leading=14, spaceAfter=4)
    s_title = sty("T", fontSize=9,  fontName="Helvetica-Bold", textColor=colors.HexColor("#111"))
    s_sub   = sty("Sb",fontSize=8,  textColor=G_MID,   fontName="Helvetica-Oblique")
    s_date  = sty("D", fontSize=8,  textColor=LGREY,   alignment=2)
    s_desc  = sty("De",fontSize=8.5,textColor=GREY,    leading=13, spaceAfter=3)
    s_chip  = sty("Ch",fontSize=8,  textColor=G_DARK,  leading=12)
    story   = []
    story.append(Paragraph(ss.rb_name or "Your Name", s_name))
    parts = [p for p in [ss.rb_email, ss.rb_phone, ss.rb_location, ss.rb_linkedin] if p.strip()]
    if parts: story.append(Paragraph("  •  ".join(parts), s_cont))
    story.append(HRFlowable(width="100%", thickness=1.5, color=G_MID, spaceAfter=6))
    if ss.rb_summary.strip():
        story.append(Paragraph("Professional Summary", s_sec))
        story.append(Paragraph(ss.rb_summary, s_sum))
    valid_exp = [e for e in ss.rb_experience if e["title"].strip() or e["company"].strip()]
    if valid_exp:
        story.append(Paragraph("Work Experience", s_sec))
        story.append(HRFlowable(width="100%", thickness=.5, color=G_LIGHT, spaceAfter=4))
        for e in valid_exp:
            row = Table([[Paragraph(e["title"],s_title), Paragraph(e["duration"],s_date)]], colWidths=["75%","25%"])
            row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0)]))
            story.append(row)
            if e["company"]:     story.append(Paragraph(e["company"], s_sub))
            if e["description"]: story.append(Paragraph(e["description"].replace("\n","<br/>"), s_desc))
            story.append(Spacer(1,3))
    valid_edu = [e for e in ss.rb_education if e["institution"].strip() or e["degree"].strip()]
    if valid_edu:
        story.append(Paragraph("Education", s_sec))
        story.append(HRFlowable(width="100%", thickness=.5, color=G_LIGHT, spaceAfter=4))
        for e in valid_edu:
            row = Table([[Paragraph(e["degree"],s_title), Paragraph(e["year"],s_date)]], colWidths=["75%","25%"])
            row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0)]))
            story.append(row)
            if e["institution"]: story.append(Paragraph(e["institution"], s_sub))
            if e["grade"]:       story.append(Paragraph(f"Grade / GPA: {e['grade']}", s_desc))
            story.append(Spacer(1,3))
    valid_proj = [p for p in ss.rb_projects if p["name"].strip()]
    if valid_proj:
        story.append(Paragraph("Projects", s_sec))
        story.append(HRFlowable(width="100%", thickness=.5, color=G_LIGHT, spaceAfter=4))
        for p in valid_proj:
            story.append(Paragraph(p["name"], s_title))
            if p["tech"]:        story.append(Paragraph(p["tech"], s_sub))
            if p["description"]: story.append(Paragraph(p["description"].replace("\n","<br/>"), s_desc))
            if p["link"]:        story.append(Paragraph(f'<link href="{p["link"]}" color="#2e7d32">{p["link"]}</link>', s_chip))
            story.append(Spacer(1,3))
    valid_skills = [sk for sk in ss.rb_skills if sk["items"].strip()]
    if valid_skills:
        story.append(Paragraph("Skills", s_sec))
        story.append(HRFlowable(width="100%", thickness=.5, color=G_LIGHT, spaceAfter=4))
        for sk in valid_skills:
            label = f"<b>{sk['category']}:</b>  " if sk["category"] else ""
            story.append(Paragraph(label + sk["items"], s_desc))
    # Certifications
    valid_certs = [c for c in ss.get("rb_certifications",[]) if c["name"].strip()]
    if valid_certs:
        story.append(Paragraph("Certifications", s_sec))
        story.append(HRFlowable(width="100%", thickness=.5, color=G_LIGHT, spaceAfter=4))
        for c in valid_certs:
            row = Table([[Paragraph(c["name"],s_title), Paragraph(c["year"],s_date)]], colWidths=["75%","25%"])
            row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0)]))
            story.append(row)
            if c["issuer"]: story.append(Paragraph(c["issuer"], s_sub))
            story.append(Spacer(1,3))
    # Languages
    langs = ss.get("rb_languages","").strip()
    if langs:
        story.append(Paragraph("Languages", s_sec))
        story.append(Paragraph(langs, s_desc))
    # Achievements
    ach = ss.get("rb_achievements","").strip()
    if ach:
        story.append(Paragraph("Achievements & Awards", s_sec))
        story.append(Paragraph(ach.replace("\n","<br/>"), s_desc))
    doc.build(story)
    return buf.getvalue()


# ── Sidebar ───────────────────────────────────────────────────────────────────
