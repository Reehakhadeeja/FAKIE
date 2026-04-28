import streamlit as st
import time
import json
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
from config import *
from pdf_builder import build_pdf
import io
import re

try:
    import reportlab
    REPORTLAB_OK = True
except ImportError:
    REPORTLAB_OK = False

def _init_resume_state():
    defs = {
        "rb_name":"","rb_email":"","rb_phone":"","rb_location":"","rb_linkedin":"","rb_summary":"",
        "rb_education":  [{"degree":"","institution":"","year":"","grade":""}],
        "rb_experience": [{"title":"","company":"","duration":"","description":""}],
        "rb_projects":   [{"name":"","tech":"","description":"","link":""}],
        "rb_skills":     [{"category":"Technical","items":""}],
        "rb_certifications":[{"name":"","issuer":"","year":""}],
        "rb_languages":"",
        "rb_achievements":"",
        "rb_template":"classic",
        "rb_active_tab":"Personal",
    }
    for k,v in defs.items():
        if k not in st.session_state: st.session_state[k]=v

def render_resume_preview():
    ss = st.session_state
    contact = ""
    for icon,val in [(bi('envelope','1em'),ss.rb_email),(bi('telephone','1em'),ss.rb_phone),(bi('geo-alt','1em'),ss.rb_location),(bi('link-45deg','1em'),ss.rb_linkedin)]:
        if val.strip(): contact += f"<span>{icon} {val}</span> "
    body = ""
    if ss.rb_summary.strip():
        body += f'<div class="rp-sec">Professional Summary</div><div style="font-family: sans-serif;font-size:.85rem;color:#333;line-height:1.65">{ss.rb_summary}</div>'
    valid_exp = [e for e in ss.rb_experience if e["title"].strip() or e["company"].strip()]
    if valid_exp:
        body += '<div class="rp-sec">Work Experience</div>'
        for e in valid_exp:
            body += f'<div style="margin-bottom:.8rem"><div style="display:flex;justify-content:space-between"><span class="rp-etitle">{e["title"]}</span><span class="rp-edate">{e["duration"]}</span></div><div class="rp-esub">{e["company"]}</div><div class="rp-edesc">{e["description"].replace(chr(10),"<br>")}</div></div>'
    valid_edu = [e for e in ss.rb_education if e["institution"].strip() or e["degree"].strip()]
    if valid_edu:
        body += '<div class="rp-sec">Education</div>'
        for e in valid_edu:
            grade_html = f'<div style="font-size:.78rem;color:#555">GPA: {e["grade"]}</div>' if e["grade"] else ""
            body += f'<div style="margin-bottom:.8rem"><div style="display:flex;justify-content:space-between"><span class="rp-etitle">{e["degree"]}</span><span class="rp-edate">{e["year"]}</span></div><div class="rp-esub">{e["institution"]}</div>{grade_html}</div>'
    valid_proj = [p for p in ss.rb_projects if p["name"].strip()]
    if valid_proj:
        body += '<div class="rp-sec">Projects</div>'
        for p in valid_proj:
            link = f"<br><a href='{p['link']}' style='color:#43a047;font-size:.76rem'>{p['link']}</a>" if p["link"] else ""
            body += f'<div style="margin-bottom:.8rem"><div class="rp-etitle">{p["name"]}</div><div class="rp-esub">{p["tech"]}</div><div class="rp-edesc">{p["description"].replace(chr(10),"<br>")}{link}</div></div>'
    valid_certs = [c for c in ss.rb_certifications if c["name"].strip()]
    if valid_certs:
        body += '<div class="rp-sec">Certifications</div>'
        for c in valid_certs:
            body += f'<div style="margin-bottom:.5rem"><div style="display:flex;justify-content:space-between"><span class="rp-etitle">{c["name"]}</span><span class="rp-edate">{c["year"]}</span></div><div class="rp-esub">{c["issuer"]}</div></div>'
    valid_skills = [sk for sk in ss.rb_skills if sk["items"].strip()]
    if valid_skills:
        body += '<div class="rp-sec">Skills</div><div style="display:flex;flex-wrap:wrap;gap:4px">'
        for sk in valid_skills:
            if sk["category"]: body += f'<span class="rp-chip"><b>{sk["category"]}:</b> {sk["items"]}</span>'
            else:
                for item in sk["items"].split(","):
                    if item.strip(): body += f'<span class="rp-chip">{item.strip()}</span>'
        body += '</div>'
    if ss.rb_languages.strip():
        body += f'<div class="rp-sec">Languages</div><div style="font-family: sans-serif;font-size:.83rem;color:#333">{ss.rb_languages}</div>'
    if ss.rb_achievements.strip():
        body += f'<div class="rp-sec">Achievements</div><div style="font-family: sans-serif;font-size:.83rem;color:#333;line-height:1.6">{ss.rb_achievements.replace(chr(10),"<br>")}</div>'

    st.markdown(f"""
    <div class="rp-card">
      <div class="rp-name">{ss.rb_name or "<span style='color:#aaa'>Your Name</span>"}</div>
      <div class="rp-contact">{contact}</div>
      <hr class="rp-hr">
      {body}
    </div>""", unsafe_allow_html=True)

def render_resume_builder():
    _init_resume_state()
    ss = st.session_state
    # st.markdown(f"<h2 style='font-family: sans-serif;color:#f1f5f9;font-size:1.6rem;font-weight:800;margin:0 0 12px'>{bi('tools','1.2rem')} Resume Builder</h2>", unsafe_allow_html=True)

    # Validation
    issues = []
    if not ss.rb_name.strip(): issues.append("Name required")
    if ss.rb_email and not is_valid_email(ss.rb_email): issues.append("Invalid email")
    if ss.rb_phone and not is_valid_phone(ss.rb_phone): issues.append("Invalid phone")

    vc,dc = st.columns([3,1])
    with vc:
        if issues:
            for iss in issues: st.markdown(f"<span style='color:#f59e0b;font-size:.82rem'>{bi('exclamation-triangle','0.85em','#f59e0b')} {iss}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color:#10b981;font-size:.82rem'>{bi('check-circle','0.85em','#10b981')} All good!</span>", unsafe_allow_html=True)
    with dc:
        if ss.rb_name.strip() and REPORTLAB_OK:
            pdf = build_pdf()
            safe = re.sub(r"[^\w\s-]","",ss.rb_name).strip().replace(" ","_") or "resume"
            st.download_button("Download PDF", data=pdf, file_name=f"{safe}_resume.pdf",
                               mime="application/pdf", use_container_width=True)
        elif not REPORTLAB_OK:
            st.button("PDF (install reportlab)", disabled=True, use_container_width=True)
        else:
            st.button("Download PDF", disabled=True, use_container_width=True)

    st.markdown("---")
    tabs_def = ["Personal","Experience","Education","Projects","Skills","Certifications","Languages & Extras"]
    tab_cols = st.columns(len(tabs_def))
    for col,label in zip(tab_cols,tabs_def):
        with col:
            t = "primary" if ss.rb_active_tab==label else "secondary"
            if st.button(label, key=f"rbt_{label}", use_container_width=True, type=t):
                ss.rb_active_tab = label; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    form_col, prev_col = st.columns([1,1], gap="large")
    active = ss.rb_active_tab

    with form_col:
        if active=="Personal":
            st.markdown(f'<div class="x_title"><h2>{bi("person")} Personal Details</h2></div>', unsafe_allow_html=True)
            ss.rb_name     = st.text_input("Full Name *",          value=ss.rb_name,     placeholder="Arjun Sharma",             key="rb_inp_name")
            c1,c2 = st.columns(2)
            with c1: ss.rb_email    = st.text_input("Email *",     value=ss.rb_email,    placeholder="arjun@example.com",        key="rb_inp_email")
            with c2: ss.rb_phone    = st.text_input("Phone",       value=ss.rb_phone,    placeholder="+91 98765 43210",          key="rb_inp_phone")
            c3,c4 = st.columns(2)
            with c3: ss.rb_location = st.text_input("Location",    value=ss.rb_location, placeholder="Bengaluru, India",         key="rb_inp_loc")
            with c4: ss.rb_linkedin = st.text_input("LinkedIn/Web",value=ss.rb_linkedin, placeholder="linkedin.com/in/arjun",    key="rb_inp_li")
            ss.rb_summary = st.text_area("Professional Summary",   value=ss.rb_summary,  placeholder="Results-driven engineer with 4+ years…", height=120, key="rb_inp_sum")

        elif active=="Experience":
            st.markdown(f'<div class="x_title"><h2>{bi("briefcase")} Work Experience</h2></div>', unsafe_allow_html=True)
            for i,exp in enumerate(ss.rb_experience):
                lbl = f"Job {i+1}: {exp['title'] or 'Untitled'} @ {exp['company'] or '—'}"
                with st.expander(lbl, expanded=(i==0)):
                    exp["title"]       = st.text_input("Job Title",   value=exp["title"],       key=f"rb_exp_t_{i}",  placeholder="Software Engineer")
                    exp["company"]     = st.text_input("Company",     value=exp["company"],     key=f"rb_exp_c_{i}",  placeholder="Infosys")
                    exp["duration"]    = st.text_input("Duration",    value=exp["duration"],    key=f"rb_exp_d_{i}",  placeholder="Jun 2022 – Present")
                    exp["description"] = st.text_area("Key Achievements", value=exp["description"], key=f"rb_exp_dc_{i}", height=100,
                                                      placeholder="• Led migration to microservices reducing latency by 40%\n• Mentored 3 junior developers\n• Delivered feature X ahead of schedule")
                    if len(ss.rb_experience)>1:
                        if st.button("Remove",key=f"rb_rm_exp_{i}"): ss.rb_experience.pop(i); st.rerun()
            if st.button("＋ Add Experience",key="rb_add_exp"):
                ss.rb_experience.append({"title":"","company":"","duration":"","description":""}); st.rerun()

        elif active=="Education":
            st.markdown(f'<div class="x_title"><h2>{bi("mortarboard")} Education</h2></div>', unsafe_allow_html=True)
            for i,edu in enumerate(ss.rb_education):
                with st.expander(f"Entry {i+1}: {edu['degree'] or 'Untitled'}", expanded=(i==0)):
                    edu["degree"]      = st.text_input("Degree",         value=edu["degree"],      key=f"rb_edu_dg_{i}", placeholder="B.Tech Computer Science")
                    edu["institution"] = st.text_input("Institution",    value=edu["institution"], key=f"rb_edu_in_{i}", placeholder="IIT Bengaluru")
                    c1,c2=st.columns(2)
                    with c1: edu["year"]  = st.text_input("Year",      value=edu["year"],  key=f"rb_edu_yr_{i}", placeholder="2019–2023")
                    with c2: edu["grade"] = st.text_input("Grade/GPA", value=edu["grade"], key=f"rb_edu_gr_{i}", placeholder="8.5/10")
                    if len(ss.rb_education)>1:
                        if st.button("Remove",key=f"rb_rm_edu_{i}"): ss.rb_education.pop(i); st.rerun()
            if st.button("＋ Add Education",key="rb_add_edu"):
                ss.rb_education.append({"degree":"","institution":"","year":"","grade":""}); st.rerun()

        elif active=="Projects":
            st.markdown(f'<div class="x_title"><h2>{bi("rocket-takeoff")} Projects</h2></div>', unsafe_allow_html=True)
            for i,proj in enumerate(ss.rb_projects):
                with st.expander(f"Project {i+1}: {proj['name'] or 'Untitled'}", expanded=(i==0)):
                    proj["name"]        = st.text_input("Project Name",    value=proj["name"],        key=f"rb_pr_n_{i}", placeholder="SniffJob AI")
                    proj["tech"]        = st.text_input("Tech Stack",      value=proj["tech"],        key=f"rb_pr_t_{i}", placeholder="Python, Streamlit, OpenAI")
                    proj["description"] = st.text_area("Description",      value=proj["description"], key=f"rb_pr_d_{i}", height=90,
                                                       placeholder="Built a job fraud detector using NLP, achieving 94% accuracy…")
                    proj["link"]        = st.text_input("GitHub/Live URL", value=proj["link"],        key=f"rb_pr_l_{i}", placeholder="https://github.com/arjun/sniffjob")
                    if len(ss.rb_projects)>1:
                        if st.button("Remove",key=f"rb_rm_proj_{i}"): ss.rb_projects.pop(i); st.rerun()
            if st.button("＋ Add Project",key="rb_add_proj"):
                ss.rb_projects.append({"name":"","tech":"","description":"","link":""}); st.rerun()

        elif active=="Skills":
            st.markdown(f'<div class="x_title"><h2>{bi("tools")} Skills</h2></div>', unsafe_allow_html=True)
            st.markdown("<small style='color:#64748b'>Comma-separated values per category</small>", unsafe_allow_html=True)
            for i,sk in enumerate(ss.rb_skills):
                with st.expander(f"Category {i+1}: {sk['category'] or 'Untitled'}", expanded=(i==0)):
                    sk["category"] = st.text_input("Category", value=sk["category"], key=f"rb_sk_c_{i}", placeholder="Technical / Soft / Tools")
                    sk["items"]    = st.text_area("Skills",    value=sk["items"],    key=f"rb_sk_i_{i}", height=80,
                                                  placeholder="Python, SQL, Docker, Git, AWS…")
                    if len(ss.rb_skills)>1:
                        if st.button("Remove",key=f"rb_rm_sk_{i}"): ss.rb_skills.pop(i); st.rerun()
            if st.button("＋ Add Category",key="rb_add_sk"):
                ss.rb_skills.append({"category":"","items":""}); st.rerun()

        elif active=="Certifications":
            st.markdown(f'<div class="x_title"><h2>{bi("award")} Certifications</h2></div>', unsafe_allow_html=True)
            for i,c in enumerate(ss.rb_certifications):
                with st.expander(f"Cert {i+1}: {c['name'] or 'Untitled'}", expanded=(i==0)):
                    c["name"]   = st.text_input("Certificate Name", value=c["name"],   key=f"rb_cert_n_{i}", placeholder="AWS Solutions Architect")
                    c["issuer"] = st.text_input("Issuer",           value=c["issuer"], key=f"rb_cert_i_{i}", placeholder="Amazon Web Services")
                    c["year"]   = st.text_input("Year",             value=c["year"],   key=f"rb_cert_y_{i}", placeholder="2024")
                    if len(ss.rb_certifications)>1:
                        if st.button("Remove",key=f"rb_rm_cert_{i}"): ss.rb_certifications.pop(i); st.rerun()
            if st.button("＋ Add Certification",key="rb_add_cert"):
                ss.rb_certifications.append({"name":"","issuer":"","year":""}); st.rerun()

        elif active=="Languages & Extras":
            st.markdown(f'<div class="x_title"><h2>{bi("translate")} Languages & Extras</h2></div>', unsafe_allow_html=True)
            ss.rb_languages     = st.text_input("Languages Known", value=ss.rb_languages,
                                                placeholder="English (Fluent), Hindi (Native), French (Beginner)", key="rb_lang")
            ss.rb_achievements  = st.text_area("Achievements & Awards", value=ss.rb_achievements, height=120,
                                               placeholder="• Hackathon winner – HackIndia 2023\n• Published paper on NLP in XYZ Journal\n• National Math Olympiad Gold – 2018",
                                               key="rb_ach")
            st.markdown("---")
            st.markdown("##### ATS Score Estimator")
            score = 20
            if ss.rb_name.strip():        score += 10
            if ss.rb_email.strip():       score += 10
            if ss.rb_summary.strip():     score += 10
            if ss.rb_experience[0]["title"].strip(): score += 15
            if ss.rb_education[0]["degree"].strip(): score += 10
            if ss.rb_skills[0]["items"].strip():     score += 15
            if ss.rb_certifications[0]["name"].strip(): score += 5
            if ss.rb_languages.strip():   score += 5
            clr = "#10b981" if score>=75 else "#f59e0b" if score>=50 else "#ef4444"
            st.markdown(f"<div style='font-size:.85rem;color:#94a3b8'>Estimated ATS Score</div>", unsafe_allow_html=True)
            st.progress(score/100)
            st.markdown(f"<div style='font-weight:700;color:{clr};font-size:1.1rem'>{score}/100</div>", unsafe_allow_html=True)

    with prev_col:
        st.markdown(f'<div class="x_title"><h2>{bi("display")} Live Preview</h2></div>', unsafe_allow_html=True)
        render_resume_preview()


# ══════════════════════════════════════════════════════════════════════════════
#  COVER LETTERS
# ══════════════════════════════════════════════════════════════════════════════
