import streamlit as st
import time
import json
import random
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
from config import *

def render_dashboard():
    uid   = st.session_state.user_id
    stats = db.get_stats(uid)
    hist  = db.get_job_history(uid)

    # st.markdown(f"<h2 style='font-family: sans-serif;color:#f1f5f9;font-size:1.6rem;font-weight:800;margin:0 0 12px'>{bi('speedometer2','1.2rem')} Dashboard</h2>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    c4,c5,c6 = st.columns(3)
    boxes = [
        (c1, stats["total"],     "Analyzed Jobs", "bg-darkblue", "briefcase-fill"),
        (c2, stats["legit"],     "Legit Jobs",    "bg-green", "check-circle-fill"),
        (c3, stats["suspicious"],"Suspicious",    "bg-orange", "exclamation-triangle-fill"),
        (c4, stats["fraud"],     "Fraudulent",    "bg-red", "shield-fill-x"),
        (c5, stats["saved"],     "Saved Jobs",    "bg-purple", "bookmark-fill"),
        (c6, stats["applied"],   "Applied Jobs",  "bg-teal", "send-fill"),
    ]
    for col,val,lbl,clr,icon in boxes:
        with col:
            st.markdown(f"""
            <div class="tile-stats {clr}">
              <div class="icon">{bi(icon)}</div>
              <div class="inner">
                <h3>{val}</h3>
                <p>{lbl}</p>
              </div>
              <div class="footer">
                View Details <span>{bi('arrow-right-circle-fill')}</span>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([1.8,1])

    with left:
        st.markdown(f"""
        <div class="table-card">
          <div class="table-header table-header-darkblue">
            {bi('list-task')} Recent Job Analyses
          </div>
          <div style="padding:10px 15px;">
        """, unsafe_allow_html=True)
        
        if not hist:
            st.markdown("<div style='color:var(--text2)'>No analyses yet. Head to Job Analyzer!</div>", unsafe_allow_html=True)
        else:
            for j in hist[:5]:
                conf  = j.get("confidence_score",0)
                status_color = STATUS_COLOR.get(j['result'],'gray')
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid var(--border);">
                  <div>
                    <div style="font-weight:600;color:var(--text);font-size:14px">{j['job_title']}</div>
                    <div style="color:var(--text2);font-size:12px">{j['company']} · {j['timestamp']}</div>
                  </div>
                  <div style="text-align:right">
                    <div style="font-size:12px;color:var(--text2);margin-bottom:2px">Conf: {conf:.0%}</div>
                    <span class="badge badge-{status_color}">{j['result']}</span>
                  </div>
                </div>""", unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        if st.button("Analyze a New Job", use_container_width=True):
            st.session_state.current_page = "analyzer"
            st.rerun()

    with right:
        st.markdown(f"""
        <div class="x_panel">
          <div class="x_title" style="margin-bottom:0; border-bottom:none;">
            <h2 style="margin-bottom:0;">{bi('lightning-charge')} Quick Actions</h2>
          </div>
        </div>
        """, unsafe_allow_html=True)
        actions = [
            ("Analyze Job URL", "analyzer"),
            ("Browse Job Board", "job_search"),
            ("Build My Resume", "resume_builder"),
            ("Write Cover Letter", "cover_letters"),
            ("EasyApply Kit", "easyapply"),
        ]
        for lbl, page in actions:
            if st.button(lbl, use_container_width=True, key=f"dash_{page}"):
                st.session_state.current_page = page
                st.rerun()

        # Fraud tip of the day
        tips = [
            f"Never pay to apply for a job. Legitimate employers don't ask for money.",
            f"Verify company's CIN on MCA portal before sharing personal info.",
            f"A 'too good to be true' salary is almost always a red flag.",
            f"Google the job title + company + 'scam' before applying.",
            f"Real jobs have structured interview processes — not just a WhatsApp chat.",
        ]
        st.markdown(f"""
        <div class="x_panel" style="margin-top:20px; border-top: 3px solid var(--blue);">
          <div class="x_title">
            <h2>{bi('lightbulb')} Tip of the Day</h2>
          </div>
          <div style="padding: 5px 0; color: var(--text); font-size:13px;">
            {random.choice(tips)}
          </div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  JOB ANALYZER
# ══════════════════════════════════════════════════════════════════════════════
