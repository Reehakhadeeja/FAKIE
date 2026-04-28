import streamlit as st
import time
import json
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
from config import *

def render_analyzer():
    uid = st.session_state.user_id
    # st.markdown(f"<h2 style='font-family: sans-serif;color:#f1f5f9;font-size:1.6rem;font-weight:800;margin:0 0 12px'>{bi('search','1.2rem')} Job Post Analyzer</h2>", unsafe_allow_html=True)

    tab_url, tab_text, tab_bulk = st.tabs(["Paste URL", "Paste Text", "Bulk Analyze"])

    # ── URL tab ──
    with tab_url:
        st.markdown(f"""
        <div class="table-card" style="border-left: 5px solid #337AB7;">
          <div style="padding:15px; display:flex; align-items:center; gap:12px;">
            <div style="font-size:1.5rem; color:#337AB7; line-height:1;">{bi('info-circle-fill')}</div>
            <div style="color:#73879C; font-size:14px; font-weight:500;">Paste any job listing URL from LinkedIn, Indeed, Naukri, Internshala, etc. to analyze its legitimacy.</div>
          </div>
        </div>""", unsafe_allow_html=True)

        job_url = st.text_input("Job URL", placeholder="https://www.linkedin.com/jobs/view/...", key="ana_url")
        c1,c2 = st.columns([3,1])
        with c2:
            analyze = st.button("Sniff It!", use_container_width=True, key="ana_btn")
        with c1:
            note_for_save = st.text_input("Personal note (optional)", placeholder="e.g. looks interesting, follow up Monday", key="ana_note")

        if analyze:
            if not job_url.strip():
                st.error("Please enter a URL.")
            else:
                with st.spinner("Sniffing the job posting..."):
                    result = simulate_analysis(job_url)
                db.add_job_analysis(uid, job_url, result["title"], result["company"],
                                    result["status"], result["confidence"], result["details"], note_for_save)
                db.add_notification(f"Analysis complete: {result['title']} → {result['status']}")

                _show_result(result, job_url)

        if not job_url:
            st.markdown(f"""
            <div style="text-align:center;padding:50px 20px; border: 2px dashed #D9DEE4; border-radius:8px; background:#f9f9f9; margin-top:20px;">
              <div style="font-size:5rem;margin-bottom:16px; line-height:1;">{bi('search-heart-fill','5rem','#D9DEE4')}</div>
              <div style="color:#73879C;font-size:1.2rem;font-weight:600">Ready to Analyze</div>
              <div style="color:#999;font-size:14px;margin-top:6px">Paste a job URL above and click "Sniff It!" to start the verification process.</div>
            </div>""", unsafe_allow_html=True)

    # ── Paste text tab ──
    with tab_text:
        jd_text = st.text_area("Paste the full job description here", height=200,
                               placeholder="Copy and paste the complete job listing text…", key="ana_text")
        if st.button("Analyze Text", key="ana_text_btn"):
            if not jd_text.strip():
                st.error("Please paste some text.")
            else:
                with st.spinner("Analyzing…"):
                    result = simulate_analysis(jd_text[:60])
                db.add_job_analysis(uid, "(text entry)", result["title"], result["company"],
                                    result["status"], result["confidence"], result["details"])
                _show_result(result, "(text entry)")

    # ── Bulk tab ──
    with tab_bulk:
        st.markdown("##### Paste up to 5 job URLs, one per line")
        bulk_input = st.text_area("URLs (one per line)", height=140, key="ana_bulk",
                                  placeholder="https://linkedin.com/...\nhttps://naukri.com/...\n…")
        if st.button("Sniff All", key="ana_bulk_btn"):
            urls = [u.strip() for u in bulk_input.strip().split("\n") if u.strip()][:5]
            if not urls:
                st.error("Enter at least one URL.")
            else:
                prog = st.progress(0, text="Analyzing…")
                for i, url in enumerate(urls):
                    time.sleep(0.8)
                    result = simulate_analysis(url)
                    db.add_job_analysis(uid, url, result["title"], result["company"],
                                        result["status"], result["confidence"], result["details"])
                    prog.progress((i+1)/len(urls), text=f"Analyzed {i+1}/{len(urls)}")
                    _show_result(result, url, compact=True)
                st.success(f"Analyzed {len(urls)} job(s). See full details in Sniff History.")


