import streamlit as st
import time
import json
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
from config import *

def render_easyapply():
    uid = st.session_state.user_id
    # st.markdown(f"<h2 style='font-family: sans-serif;color:#f1f5f9;font-size:1.6rem;font-weight:800;margin:0 0 12px'>{bi('clipboard-check','1.2rem')} EasyApply Kit</h2>", unsafe_allow_html=True)

    t1,t2,t3,t4 = st.tabs(["Elevator Pitch","Application Checklist","Follow-up Email","Interview Cheatsheet"])

    with t1:
        st.markdown(f'<div class="x_title"><h2>{bi("megaphone")} Elevator Pitch Generator</h2></div>', unsafe_allow_html=True)
        role    = st.text_input("Your target role",    placeholder="Data Scientist", key="ep_role")
        yoe     = st.text_input("Years of experience", placeholder="3 years",        key="ep_yoe")
        top3    = st.text_input("Top 3 skills",        placeholder="Python, ML, SQL",key="ep_skills")
        company = st.text_input("Target company (optional)", placeholder="Swiggy",   key="ep_company")
        if st.button("Generate Pitch", use_container_width=True, key="ep_btn"):
            if role and yoe and top3:
                comp_str = f" at {company}" if company else ""
                pitch = f"Hi! I'm a {role} with {yoe} of experience specializing in {top3}. I've built products that have driven measurable business impact — including [your best achievement]. I'm particularly excited about opportunities{comp_str} where I can apply my expertise in {top3.split(',')[0].strip()} to solve complex problems at scale. I'd love to connect and learn more about how I might contribute to your team."
                st.markdown(f"""
                <div class="table-card" style="padding:15px; background:#f9f9f9; border-left: 4px solid #337AB7;">
                  <div style="font-size:13px; color:#555; line-height:1.7;">{pitch}</div>
                </div>""", unsafe_allow_html=True)
                st.download_button("Save Pitch", data=pitch, file_name="elevator_pitch.txt", mime="text/plain")
            else:
                st.error("Please fill in all fields.")

    with t2:
        st.markdown(f'<div class="x_title"><h2>{bi("list-check")} Pre-Application Checklist</h2></div>', unsafe_allow_html=True)
        items = [
            ("Resume updated and ATS-friendly", "Your resume is tailored to the JD with relevant keywords."),
            ("Cover letter written", "Role-specific cover letter ready."),
            ("Company researched", "Know the company's mission, products, recent news, culture."),
            ("LinkedIn profile updated", "Profile matches resume, has a professional photo."),
            ("Portfolio / GitHub ready", "Projects are live and presentable."),
            ("References lined up", "At least 2 professional references ready to vouch."),
            ("Professional email address", "Using firstname.lastname@gmail.com format."),
            ("Job posting analyzed", "Ran through SniffJob to verify it's legitimate."),
        ]
        for item,tip in items:
            done = st.checkbox(item, key=f"chk_{item[:10]}")
            if done:
                st.markdown(f"<div style='color:#10b981;font-size:.75rem;padding-left:24px;margin-top:-8px'>{bi('check-lg','0.75em','#10b981')} {tip}</div>", unsafe_allow_html=True)
        completed = sum(1 for item,_ in items if st.session_state.get(f"chk_{item[:10]}",False))
        st.progress(completed/len(items), text=f"{completed}/{len(items)} complete")

    with t3:
        st.markdown(f'<div class="x_title"><h2>{bi("envelope-open")} Follow-Up Email Templates</h2></div>', unsafe_allow_html=True)
        ftype = st.selectbox("Template type", ["After Application","After Interview","Thank You Note","Request for Status Update"], key="fu_type")
        fname = st.text_input("Your name",            placeholder="Arjun Sharma",       key="fu_name")
        hrname= st.text_input("HR / Interviewer name",placeholder="Priya Mehta",        key="fu_hr")
        pos   = st.text_input("Position applied for", placeholder="Senior Python Dev",  key="fu_pos")
        templates = {
            "After Application": f"Subject: Following up on {pos} Application\n\nDear {hrname},\n\nI wanted to follow up on my application for the {pos} role submitted [date]. I remain very excited about this opportunity and am confident my skills align well with your requirements.\n\nPlease let me know if you need any additional information.\n\nBest regards,\n{fname}",
            "After Interview": f"Subject: Thank you — {pos} Interview\n\nDear {hrname},\n\nThank you for taking the time to speak with me yesterday about the {pos} position. Our conversation reinforced my enthusiasm for the role and the team.\n\nI look forward to hearing about the next steps.\n\nWarm regards,\n{fname}",
            "Thank You Note": f"Subject: Thank You — {pos}\n\nDear {hrname},\n\nThank you sincerely for the opportunity to interview for the {pos} role. I appreciated learning more about the team's vision and challenges.\n\nI am very excited about the possibility of joining your team.\n\nBest,\n{fname}",
            "Request for Status Update": f"Subject: Status Update — {pos} Application\n\nDear {hrname},\n\nI hope you're well. I'm writing to enquire about the status of my application for the {pos} position submitted [date]. I remain keenly interested and would appreciate any update you can share.\n\nThank you for your time.\n\nBest regards,\n{fname}",
        }
        email_text = templates.get(ftype,"")
        st.text_area("Template (edit as needed)", value=email_text, height=200, key="fu_preview")
        st.download_button("Download Template", data=email_text, file_name=f"followup_{ftype.replace(' ','_')}.txt", mime="text/plain")

    with t4:
        st.markdown(f'<div class="x_title"><h2>{bi("patch-question")} Interview Cheatsheet</h2></div>', unsafe_allow_html=True)
        cats = {
            "Technical": ["Explain your most complex project","Data structures & algorithms","System design basics","Tech stack deep dive","Debugging experience"],
            "Behavioral (STAR)": ["Tell me about yourself","Greatest achievement","A time you failed","Conflict with a colleague","Why do you want to leave?"],
            "Salary": ["What are your salary expectations?","Are you interviewing elsewhere?","What's your notice period?","Do you have competing offers?"],
            "Questions to Ask": ["What does success look like in 90 days?","What's the team culture like?","What are the biggest challenges?","What tech stack do you use?","Growth opportunities?"],
        }
        for cat,qs in cats.items():
            with st.expander(cat):
                for q in qs:
                    st.markdown(f"<div class='tag' style='margin:3px 0;display:block'>{q}</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  NOTES
# ══════════════════════════════════════════════════════════════════════════════
