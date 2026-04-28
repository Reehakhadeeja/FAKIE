import streamlit as st
import time
import json
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
from config import *

def render_cover_letters():
    uid = st.session_state.user_id
    # st.markdown(f"<h2 style='font-family: sans-serif;color:#f1f5f9;font-size:1.6rem;font-weight:800;margin:0 0 12px'>{bi('envelope-paper','1.2rem')} Cover Letters</h2>", unsafe_allow_html=True)

    tab_gen, tab_saved = st.tabs(["Generate","Saved"])

    with tab_gen:
        st.markdown(f'<div class="x_title"><h2>{bi("magic")} AI Cover Letter Generator</h2></div>', unsafe_allow_html=True)
        st.markdown('<div class="table-card" style="padding:20px; background:#fff;">', unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1:
            cl_title   = st.text_input("Job Title",  value=st.session_state.get("cl_prefill_title",""),  placeholder="Senior Python Developer", key="cl_title")
            cl_company = st.text_input("Company",    value=st.session_state.get("cl_prefill_company",""),placeholder="Flipkart",               key="cl_company")
            cl_tone    = st.selectbox("Tone", ["Professional","Enthusiastic","Concise","Creative"],       key="cl_tone")
        with c2:
            cl_skills  = st.text_input("Your top skills", placeholder="Python, AWS, Leadership",          key="cl_skills")
            cl_exp     = st.text_input("Years of experience", placeholder="4 years",                      key="cl_exp")
            cl_why     = st.text_area("Why this role?", placeholder="I'm passionate about fintech…",      height=72, key="cl_why")

        if st.button("Generate Cover Letter", use_container_width=True, key="cl_gen_btn"):
            if not cl_title or not cl_company:
                st.error("Please fill in Job Title and Company")
            else:
                with st.spinner("Drafting your cover letter…"):
                    time.sleep(1.2)
                    tone_phrases = {
                        "Professional": "I am writing to express my strong interest",
                        "Enthusiastic": "I am thrilled to apply for",
                        "Concise": "Please consider my application for",
                        "Creative": "Imagine a candidate who brings both creativity and rigor to",
                    }
                    skills_str = cl_skills or "software development, problem solving"
                    exp_str    = cl_exp or "several years of"
                    why_str    = cl_why or f"I admire {cl_company}'s mission and believe I can contribute significantly."
                    letter = f"""Dear Hiring Manager,

{tone_phrases.get(cl_tone, 'I am writing to apply for')} the {cl_title} position at {cl_company}.

With {exp_str} experience in {skills_str}, I have consistently delivered results that align with the responsibilities you have outlined. My background has equipped me with both the technical depth and the collaborative mindset required to excel in this role.

{why_str}

I am confident that my skills in {skills_str} make me an excellent fit for your team. I would welcome the opportunity to discuss how I can contribute to {cl_company}'s continued success.

Thank you for your time and consideration.

Warm regards,
{st.session_state.get('rb_name', '[Your Name]')}
{st.session_state.get('rb_email', '[Your Email]')}
{st.session_state.get('rb_phone', '[Your Phone]')}"""

                st.session_state.generated_cl = letter
                st.session_state.cl_prefill_title   = ""
                st.session_state.cl_prefill_company = ""
        st.markdown('</div>', unsafe_allow_html=True)

        if "generated_cl" in st.session_state and st.session_state.generated_cl:
            st.markdown("---")
            edited = st.text_area("Edit your cover letter", value=st.session_state.generated_cl, height=300, key="cl_edit")
            a1,a2,a3 = st.columns(3)
            with a1:
                st.download_button("Download .txt", data=edited, file_name=f"cover_letter_{cl_company}.txt",
                                   mime="text/plain", use_container_width=True)
            with a2:
                if st.button("Save", use_container_width=True, key="cl_save_btn"):
                    db.save_cover_letter(uid, cl_title, cl_company, edited)
                    st.success("Saved!")
            with a3:
                if st.button("Regenerate", use_container_width=True, key="cl_regen"):
                    del st.session_state["generated_cl"]; st.rerun()

    with tab_saved:
        st.markdown(f'<div class="x_title"><h2>{bi("archive")} Saved Cover Letters</h2></div>', unsafe_allow_html=True)
        letters = db.get_cover_letters(uid)
        if not letters:
            st.info("No saved cover letters yet.")
        for cl in letters:
            with st.expander(f"{cl['title']} @ {cl['company']} — {cl['created_at']}"):
                st.text_area("", value=cl["content"], height=200, key=f"cl_view_{cl['id']}")
                st.download_button("Download", data=cl["content"], file_name=f"cl_{cl['company']}.txt",
                                   mime="text/plain", key=f"cl_dl_{cl['id']}")


# ══════════════════════════════════════════════════════════════════════════════
#  AI ASSISTANT
# ══════════════════════════════════════════════════════════════════════════════
