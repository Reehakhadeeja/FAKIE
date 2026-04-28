import streamlit as st
import time
import json
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
from config import *

def render_saved_jobs():
    uid = st.session_state.user_id
    # st.markdown(f"<h2 style='font-family: sans-serif;color:#f1f5f9;font-size:1.6rem;font-weight:800;margin:0 0 12px'>{bi('pin-angle','1.2rem')} Saved Jobs</h2>", unsafe_allow_html=True)
    st.markdown(f'<div class="x_title"><h2>{bi("bookmark-fill")} Saved Opportunities</h2></div>', unsafe_allow_html=True)
    saved = db.get_saved_jobs(uid)
    if not saved:
        st.info("No saved jobs yet. Analyze a job and hit 'Save Job'.")
        return
    applied_ids = {a["saved_job_id"] for a in db.store["applied_jobs"] if a["user_id"]==uid}
    for j in saved:
        sc = STATUS_CLASS.get(j["status"],"")
        em = bi(STATUS_EMOJI.get(j["status"],"clipboard"), '1em', {'Legit':'#1ABB9C','Suspicious':'#F39C12','Fraud':'#E74C3C'}.get(j['status'],'#999'))
        c1,c2,c3 = st.columns([4,1,1])
        with c1:
            st.markdown(f"""
            <div class="table-card" style="padding:15px; border-left: 4px solid {'var(--green)' if j['status']=='Legit' else 'var(--yellow)' if j['status']=='Suspicious' else 'var(--red)'};">
              <div style="font-weight:700;color:var(--text)">{em} {j['title']}</div>
              <div style="color:var(--text2);font-size:13px">{j['company']} · <small>Saved {j['saved_at']}</small></div>
            </div>""", unsafe_allow_html=True)
        with c2:
            if j["id"] not in applied_ids:
                if st.button("Applied", key=f"app_{j['id']}", use_container_width=True):
                    db.mark_applied(uid, j["id"])
                    st.rerun()
            else:
                st.markdown(f"<div style='color:#10b981;font-size:.82rem;padding-top:12px;text-align:center'>{bi('check-circle-fill','1em','#10b981')} Applied</div>", unsafe_allow_html=True)
        with c3:
            if st.button("Cover", key=f"cl_sv_{j['id']}", use_container_width=True):
                st.session_state.cl_prefill_title   = j["title"]
                st.session_state.cl_prefill_company = j["company"]
                st.session_state.current_page = "cover_letters"
                st.rerun()


