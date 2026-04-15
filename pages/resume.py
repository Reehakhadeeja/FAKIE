import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import io
import re


def render_resume_page():
    """Render the resume builder page within the main app"""

    # ─────────────────────────────────────────────
    #  Scoped CSS – green theme for resume builder only
    #  Uses .rb- prefix to avoid colliding with main app styles
    # ─────────────────────────────────────────────
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

/* ── Resume builder wrapper ─────────────────── */
.rb-wrap { font-family: 'DM Sans', sans-serif; }

/* Cards / expanders inside the resume page */
.rb-wrap .stExpander {
    border: 1.5px solid #c8e6c9 !important;
    border-radius: 10px !important;
    background: #1e293b !important;
    margin-bottom: 0.6rem;
}
.rb-wrap .stExpander > div:first-child {
    background: #243b24 !important;
    border-radius: 10px 10px 0 0 !important;
}

/* Download button */
.rb-wrap .stDownloadButton > button {
    background: linear-gradient(135deg, #1b5e20, #2e7d32) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em;
    padding: 0.5rem 1.5rem !important;
    width: 100%;
    font-size: 0.95rem;
    box-shadow: 0 4px 14px rgba(27,94,32,0.35) !important;
    transition: all 0.2s !important;
}
.rb-wrap .stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(27,94,32,0.45) !important;
}

/* Validation badges */
.badge-ok   { color:#4ade80; font-weight:600; }
.badge-warn { color:#fbbf24; font-weight:600; }

/* ── Resume preview card ────────────────────── */
.resume-card {
    background: #ffffff;
    border: 1.5px solid #c8e6c9;
    border-radius: 14px;
    padding: 2.2rem 2.5rem;
    box-shadow: 0 4px 24px rgba(46,125,50,0.12);
    font-family: 'DM Sans', sans-serif;
    max-width: 760px;
    margin: 0 auto;
    animation: rbFadeIn 0.4s ease;
    color: #1a2e1a;
}
@keyframes rbFadeIn {
    from { opacity:0; transform:translateY(8px); }
    to   { opacity:1; transform:none; }
}
.resume-name {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #1b5e20;
    margin: 0 0 0.15rem;
    letter-spacing: -0.02em;
}
.resume-contact {
    color: #4a4a4a;
    font-size: 0.82rem;
    margin-bottom: 0.6rem;
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}
.resume-contact span { display:flex; align-items:center; gap:0.3rem; }
.resume-divider {
    border: none;
    border-top: 2px solid #43a047;
    margin: 0.6rem 0 1.1rem;
}
.resume-section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.05rem;
    color: #2e7d32;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 1.2rem 0 0.5rem;
    border-bottom: 1.5px solid #e8f5e9;
    padding-bottom: 0.2rem;
}
.resume-summary {
    color: #3a3a3a;
    font-size: 0.88rem;
    line-height: 1.65;
    margin-bottom: 0.6rem;
}
.resume-entry-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.15rem;
}
.resume-entry-title  { font-weight:700; font-size:0.9rem; color:#1a2e1a; }
.resume-entry-sub    { font-size:0.82rem; color:#388e3c; font-style:italic; }
.resume-entry-date   { font-size:0.78rem; color:#777; white-space:nowrap; }
.resume-entry-desc   { font-size:0.83rem; color:#4a4a4a; line-height:1.6; margin-top:0.2rem; }
.skills-grid         { display:flex; flex-wrap:wrap; gap:0.4rem; margin-top:0.3rem; }
.skill-chip {
    background: #e8f5e9;
    color: #2e7d32;
    border: 1px solid #a5d6a7;
    border-radius: 20px;
    padding: 0.2rem 0.75rem;
    font-size: 0.78rem;
    font-weight: 600;
}

/* Tab strip for section navigation */
.rb-tabs {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 1.2rem;
}
.rb-tab-active {
    background: #2e7d32;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.4rem 1rem;
    font-weight: 700;
    font-size: 0.82rem;
    cursor: pointer;
}
.rb-tab {
    background: #1e293b;
    color: #94a3b8;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 0.4rem 1rem;
    font-weight: 500;
    font-size: 0.82rem;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    #  Session-state initialisation
    #  All keys are prefixed with "rb_" to avoid
    #  collision with main app session state
    # ─────────────────────────────────────────────
    def _init():
        defaults = {
            "rb_name": "", "rb_email": "", "rb_phone": "",
            "rb_location": "", "rb_linkedin": "", "rb_summary": "",
            "rb_education":  [{"degree": "", "institution": "", "year": "", "grade": ""}],
            "rb_experience": [{"title": "", "company": "", "duration": "", "description": ""}],
            "rb_projects":   [{"name": "", "tech": "", "description": "", "link": ""}],
            "rb_skills":     [{"category": "Technical", "items": ""}],
            "rb_active_tab": "Personal",
        }
        for k, v in defaults.items():
            if k not in st.session_state:
                st.session_state[k] = v

    _init()

    # ─────────────────────────────────────────────
    #  Helpers
    # ─────────────────────────────────────────────
    def is_valid_email(e): return bool(re.match(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$", e))
    def is_valid_phone(p): return bool(re.match(r"^[\d\s\+\-\(\)]{7,15}$", p))

    def validation_issues():
        issues = []
        if not st.session_state.rb_name.strip():
            issues.append("Name is required")
        if st.session_state.rb_email and not is_valid_email(st.session_state.rb_email):
            issues.append("Invalid email")
        if st.session_state.rb_phone and not is_valid_phone(st.session_state.rb_phone):
            issues.append("Invalid phone")
        return issues

    # ─────────────────────────────────────────────
    #  PDF generation
    # ─────────────────────────────────────────────
    GREEN_DARK  = colors.HexColor("#1b5e20")
    GREEN_MID   = colors.HexColor("#2e7d32")
    GREEN_LIGHT = colors.HexColor("#e8f5e9")
    GREY        = colors.HexColor("#555555")
    LIGHT_GREY  = colors.HexColor("#888888")

    def build_pdf() -> bytes:
        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf, pagesize=A4,
            leftMargin=18*mm, rightMargin=18*mm,
            topMargin=16*mm, bottomMargin=16*mm,
        )
        base_styles = getSampleStyleSheet()

        def s(name, **kw):
            return ParagraphStyle(name, parent=base_styles["Normal"], **kw)

        s_name    = s("Name",    fontSize=22, textColor=GREEN_DARK,  fontName="Helvetica-Bold", spaceAfter=2)
        s_contact = s("Contact", fontSize=8,  textColor=GREY,        spaceAfter=4, leading=12)
        s_section = s("Section", fontSize=10, textColor=GREEN_MID,   fontName="Helvetica-Bold",
                       spaceBefore=10, spaceAfter=3, leading=13)
        s_summary = s("Summary", fontSize=9,  textColor=GREY,        leading=14, spaceAfter=4)
        s_title   = s("Title",   fontSize=9,  fontName="Helvetica-Bold", textColor=colors.HexColor("#111"))
        s_sub     = s("Sub",     fontSize=8,  textColor=GREEN_MID,   fontName="Helvetica-Oblique")
        s_date    = s("Date",    fontSize=8,  textColor=LIGHT_GREY,  alignment=2)
        s_desc    = s("Desc",    fontSize=8.5, textColor=GREY,       leading=13, spaceAfter=3)
        s_chip    = s("Chip",    fontSize=8,  textColor=GREEN_DARK,  leading=12)

        ss = st.session_state
        story = []

        # Header
        story.append(Paragraph(ss.rb_name or "Your Name", s_name))
        parts = [p for p in [ss.rb_email, ss.rb_phone, ss.rb_location, ss.rb_linkedin] if p.strip()]
        if parts:
            story.append(Paragraph("  •  ".join(parts), s_contact))
        story.append(HRFlowable(width="100%", thickness=1.5, color=GREEN_MID, spaceAfter=6))

        # Summary
        if ss.rb_summary.strip():
            story.append(Paragraph("Professional Summary", s_section))
            story.append(Paragraph(ss.rb_summary, s_summary))

        # Experience
        valid_exp = [e for e in ss.rb_experience if e["title"].strip() or e["company"].strip()]
        if valid_exp:
            story.append(Paragraph("Work Experience", s_section))
            story.append(HRFlowable(width="100%", thickness=0.5, color=GREEN_LIGHT, spaceAfter=4))
            for e in valid_exp:
                row = Table(
                    [[Paragraph(e["title"], s_title), Paragraph(e["duration"], s_date)]],
                    colWidths=["75%", "25%"]
                )
                row.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 0)]))
                story.append(row)
                if e["company"]: story.append(Paragraph(e["company"], s_sub))
                if e["description"]: story.append(Paragraph(e["description"].replace("\n", "<br/>"), s_desc))
                story.append(Spacer(1, 3))

        # Education
        valid_edu = [e for e in ss.rb_education if e["institution"].strip() or e["degree"].strip()]
        if valid_edu:
            story.append(Paragraph("Education", s_section))
            story.append(HRFlowable(width="100%", thickness=0.5, color=GREEN_LIGHT, spaceAfter=4))
            for e in valid_edu:
                row = Table(
                    [[Paragraph(e["degree"], s_title), Paragraph(e["year"], s_date)]],
                    colWidths=["75%", "25%"]
                )
                row.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 0)]))
                story.append(row)
                if e["institution"]: story.append(Paragraph(e["institution"], s_sub))
                if e["grade"]: story.append(Paragraph(f"Grade / GPA: {e['grade']}", s_desc))
                story.append(Spacer(1, 3))

        # Projects
        valid_proj = [p for p in ss.rb_projects if p["name"].strip()]
        if valid_proj:
            story.append(Paragraph("Projects", s_section))
            story.append(HRFlowable(width="100%", thickness=0.5, color=GREEN_LIGHT, spaceAfter=4))
            for p in valid_proj:
                story.append(Paragraph(p["name"], s_title))
                if p["tech"]: story.append(Paragraph(p["tech"], s_sub))
                if p["description"]: story.append(Paragraph(p["description"].replace("\n", "<br/>"), s_desc))
                if p["link"]: story.append(Paragraph(f'<link href="{p["link"]}" color="#2e7d32">{p["link"]}</link>', s_chip))
                story.append(Spacer(1, 3))

        # Skills
        valid_skills = [sk for sk in ss.rb_skills if sk["items"].strip()]
        if valid_skills:
            story.append(Paragraph("Skills", s_section))
            story.append(HRFlowable(width="100%", thickness=0.5, color=GREEN_LIGHT, spaceAfter=4))
            for sk in valid_skills:
                label = f"<b>{sk['category']}:</b>  " if sk["category"] else ""
                story.append(Paragraph(label + sk["items"], s_desc))

        doc.build(story)
        return buf.getvalue()

    # ─────────────────────────────────────────────
    #  HTML Preview
    # ─────────────────────────────────────────────
    def render_preview():
        ss = st.session_state
        contact_html = ""
        for icon, val in [("✉️", ss.rb_email), ("📞", ss.rb_phone), ("📍", ss.rb_location), ("🔗", ss.rb_linkedin)]:
            if val.strip():
                contact_html += f"<span>{icon} {val}</span>"

        sections = ""

        if ss.rb_summary.strip():
            sections += f'<div class="resume-section-title">Professional Summary</div><div class="resume-summary">{ss.rb_summary}</div>'

        valid_exp = [e for e in ss.rb_experience if e["title"].strip() or e["company"].strip()]
        if valid_exp:
            sections += '<div class="resume-section-title">Work Experience</div>'
            for e in valid_exp:
                sections += f"""
                <div style="margin-bottom:0.75rem">
                  <div class="resume-entry-header">
                    <span class="resume-entry-title">{e['title']}</span>
                    <span class="resume-entry-date">{e['duration']}</span>
                  </div>
                  <div class="resume-entry-sub">{e['company']}</div>
                  <div class="resume-entry-desc">{e['description'].replace(chr(10),'<br>')}</div>
                </div>"""

        valid_edu = [e for e in ss.rb_education if e["institution"].strip() or e["degree"].strip()]
        if valid_edu:
            sections += '<div class="resume-section-title">Education</div>'
            for e in valid_edu:
                grade = f"<br><span style='color:#555;font-size:0.8rem'>Grade / GPA: {e['grade']}</span>" if e["grade"] else ""
                sections += f"""
                <div style="margin-bottom:0.75rem">
                  <div class="resume-entry-header">
                    <span class="resume-entry-title">{e['degree']}</span>
                    <span class="resume-entry-date">{e['year']}</span>
                  </div>
                  <div class="resume-entry-sub">{e['institution']}</div>{grade}
                </div>"""

        valid_proj = [p for p in ss.rb_projects if p["name"].strip()]
        if valid_proj:
            sections += '<div class="resume-section-title">Projects</div>'
            for p in valid_proj:
                link_html = f"<br><a href='{p['link']}' style='font-size:0.78rem;color:#43a047'>{p['link']}</a>" if p["link"] else ""
                sections += f"""
                <div style="margin-bottom:0.75rem">
                  <div class="resume-entry-title">{p['name']}</div>
                  <div class="resume-entry-sub">{p['tech']}</div>
                  <div class="resume-entry-desc">{p['description'].replace(chr(10),'<br>')}{link_html}</div>
                </div>"""

        valid_skills = [sk for sk in ss.rb_skills if sk["items"].strip()]
        if valid_skills:
            sections += '<div class="resume-section-title">Skills</div>'
            chips = ""
            for sk in valid_skills:
                if sk["category"]:
                    chips += f"<span class='skill-chip'><b>{sk['category']}:</b> {sk['items']}</span>"
                else:
                    for item in sk["items"].split(","):
                        if item.strip():
                            chips += f"<span class='skill-chip'>{item.strip()}</span>"
            sections += f'<div class="skills-grid">{chips}</div>'

        st.markdown(f"""
        <div class="resume-card">
          <div class="resume-name">{ss.rb_name or '<span style="color:#aaa">Your Name</span>'}</div>
          <div class="resume-contact">{contact_html}</div>
          <hr class="resume-divider">
          {sections}
        </div>""", unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    #  Page header + download — shown inline
    #  (no sidebar takeover)
    # ─────────────────────────────────────────────
    st.markdown('<div class="rb-wrap">', unsafe_allow_html=True)
    st.markdown("# 📄 Resume Builder")
    st.markdown("#### Build your professional resume with live preview")

    # Validation + download strip
    issues = validation_issues()
    vcol, dcol = st.columns([2, 1])
    with vcol:
        if issues:
            for iss in issues:
                st.markdown(f"<span class='badge-warn'>⚠ {iss}</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span class='badge-ok'>✅ All looks good!</span>", unsafe_allow_html=True)
    with dcol:
        if st.session_state.rb_name.strip():
            pdf_bytes = build_pdf()
            safe_name = re.sub(r"[^\w\s-]", "", st.session_state.rb_name).strip().replace(" ", "_") or "resume"
            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_bytes,
                file_name=f"{safe_name}_resume.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.button("⬇️ Download PDF", disabled=True, use_container_width=True)

    st.markdown("---")

    # ─────────────────────────────────────────────
    #  Section tab strip  (horizontal, not sidebar)
    # ─────────────────────────────────────────────
    tabs_def = [
        ("👤", "Personal"),
        ("💼", "Experience"),
        ("🎓", "Education"),
        ("🚀", "Projects"),
        ("🛠", "Skills"),
    ]

    tab_cols = st.columns(len(tabs_def))
    for col, (icon, label) in zip(tab_cols, tabs_def):
        with col:
            active = st.session_state.rb_active_tab == label
            btn_type = "primary" if active else "secondary"
            if st.button(f"{icon} {label}", key=f"rbtab_{label}", use_container_width=True, type=btn_type):
                st.session_state.rb_active_tab = label
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    #  Two-column: form | preview
    # ─────────────────────────────────────────────
    col_form, col_preview = st.columns([1, 1], gap="large")
    active = st.session_state.rb_active_tab

    with col_form:
        # ── Personal ────────────────────────────
        if active == "Personal":
            st.markdown("### 👤 Personal Details")
            st.session_state.rb_name = st.text_input(
                "Full Name *", value=st.session_state.rb_name, placeholder="Jane Doe", key="rb_inp_name")
            c1, c2 = st.columns(2)
            with c1:
                st.session_state.rb_email = st.text_input(
                    "Email *", value=st.session_state.rb_email, placeholder="jane@example.com", key="rb_inp_email")
            with c2:
                st.session_state.rb_phone = st.text_input(
                    "Phone", value=st.session_state.rb_phone, placeholder="+91 98765 43210", key="rb_inp_phone")
            c3, c4 = st.columns(2)
            with c3:
                st.session_state.rb_location = st.text_input(
                    "Location", value=st.session_state.rb_location, placeholder="Bengaluru, India", key="rb_inp_loc")
            with c4:
                st.session_state.rb_linkedin = st.text_input(
                    "LinkedIn / Website", value=st.session_state.rb_linkedin,
                    placeholder="linkedin.com/in/jane", key="rb_inp_li")
            st.session_state.rb_summary = st.text_area(
                "Professional Summary", value=st.session_state.rb_summary,
                placeholder="Brief 2-3 sentence professional summary…", height=120, key="rb_inp_sum")

            if st.session_state.rb_email and not is_valid_email(st.session_state.rb_email):
                st.markdown("<span class='badge-warn'>⚠ Please enter a valid email address.</span>", unsafe_allow_html=True)
            if st.session_state.rb_phone and not is_valid_phone(st.session_state.rb_phone):
                st.markdown("<span class='badge-warn'>⚠ Phone should contain 7-15 digits.</span>", unsafe_allow_html=True)

        # ── Experience ──────────────────────────
        elif active == "Experience":
            st.markdown("### 💼 Work Experience")
            for i, exp in enumerate(st.session_state.rb_experience):
                label = f"Job {i+1}: {exp['title'] or 'Untitled'} @ {exp['company'] or '—'}"
                with st.expander(label, expanded=(i == 0)):
                    exp["title"]       = st.text_input("Job Title",    value=exp["title"],       key=f"rb_exp_t_{i}",  placeholder="Software Engineer")
                    exp["company"]     = st.text_input("Company",      value=exp["company"],     key=f"rb_exp_c_{i}",  placeholder="Acme Corp")
                    exp["duration"]    = st.text_input("Duration",     value=exp["duration"],    key=f"rb_exp_d_{i}",  placeholder="Jan 2022 – Present")
                    exp["description"] = st.text_area("Description",   value=exp["description"], key=f"rb_exp_dc_{i}", height=100,
                                                       placeholder="• Led development of…\n• Improved performance by…")
                    if len(st.session_state.rb_experience) > 1:
                        if st.button("🗑 Remove", key=f"rb_rm_exp_{i}"):
                            st.session_state.rb_experience.pop(i)
                            st.rerun()
            if st.button("＋ Add Experience", key="rb_add_exp"):
                st.session_state.rb_experience.append({"title":"","company":"","duration":"","description":""})
                st.rerun()

        # ── Education ───────────────────────────
        elif active == "Education":
            st.markdown("### 🎓 Education")
            for i, edu in enumerate(st.session_state.rb_education):
                with st.expander(f"Entry {i+1}: {edu['degree'] or 'Untitled'}", expanded=(i == 0)):
                    edu["degree"]      = st.text_input("Degree / Qualification", value=edu["degree"],      key=f"rb_edu_dg_{i}", placeholder="B.Tech Computer Science")
                    edu["institution"] = st.text_input("Institution",            value=edu["institution"], key=f"rb_edu_in_{i}", placeholder="IIT Bengaluru")
                    c1, c2 = st.columns(2)
                    with c1: edu["year"]  = st.text_input("Year",       value=edu["year"],  key=f"rb_edu_yr_{i}", placeholder="2019 – 2023")
                    with c2: edu["grade"] = st.text_input("Grade / GPA",value=edu["grade"], key=f"rb_edu_gr_{i}", placeholder="8.5 / 10")
                    if len(st.session_state.rb_education) > 1:
                        if st.button("🗑 Remove", key=f"rb_rm_edu_{i}"):
                            st.session_state.rb_education.pop(i)
                            st.rerun()
            if st.button("＋ Add Education", key="rb_add_edu"):
                st.session_state.rb_education.append({"degree":"","institution":"","year":"","grade":""})
                st.rerun()

        # ── Projects ────────────────────────────
        elif active == "Projects":
            st.markdown("### 🚀 Projects")
            for i, proj in enumerate(st.session_state.rb_projects):
                with st.expander(f"Project {i+1}: {proj['name'] or 'Untitled'}", expanded=(i == 0)):
                    proj["name"]        = st.text_input("Project Name",     value=proj["name"],        key=f"rb_pr_n_{i}", placeholder="Smart Resume Builder")
                    proj["tech"]        = st.text_input("Tech / Stack",     value=proj["tech"],        key=f"rb_pr_t_{i}", placeholder="Python, Streamlit, ReportLab")
                    proj["description"] = st.text_area("Description",       value=proj["description"], key=f"rb_pr_d_{i}", height=90,
                                                        placeholder="What it does, your role, impact…")
                    proj["link"]        = st.text_input("GitHub / Live URL",value=proj["link"],        key=f"rb_pr_l_{i}", placeholder="https://github.com/jane/project")
                    if len(st.session_state.rb_projects) > 1:
                        if st.button("🗑 Remove", key=f"rb_rm_proj_{i}"):
                            st.session_state.rb_projects.pop(i)
                            st.rerun()
            if st.button("＋ Add Project", key="rb_add_proj"):
                st.session_state.rb_projects.append({"name":"","tech":"","description":"","link":""})
                st.rerun()

        # ── Skills ──────────────────────────────
        elif active == "Skills":
            st.markdown("### 🛠 Skills")
            st.markdown("<small style='color:#94a3b8'>Enter comma-separated skills per category.</small>", unsafe_allow_html=True)
            for i, sk in enumerate(st.session_state.rb_skills):
                with st.expander(f"Category {i+1}: {sk['category'] or 'Untitled'}", expanded=(i == 0)):
                    sk["category"] = st.text_input("Category", value=sk["category"], key=f"rb_sk_c_{i}", placeholder="Technical / Soft / Languages…")
                    sk["items"]    = st.text_area("Skills (comma-separated)", value=sk["items"], key=f"rb_sk_i_{i}", height=80,
                                                   placeholder="Python, SQL, Docker, Git…")
                    if len(st.session_state.rb_skills) > 1:
                        if st.button("🗑 Remove", key=f"rb_rm_sk_{i}"):
                            st.session_state.rb_skills.pop(i)
                            st.rerun()
            if st.button("＋ Add Skill Category", key="rb_add_sk"):
                st.session_state.rb_skills.append({"category":"","items":""})
                st.rerun()

    with col_preview:
        st.markdown("### 🖥 Live Preview")
        render_preview()

    st.markdown('</div>', unsafe_allow_html=True)