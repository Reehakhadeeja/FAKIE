import streamlit as st
import time
import json
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
from config import *

def render_job_search():
    uid = st.session_state.user_id
    # st.markdown(f"<h2 style='font-family: sans-serif;color:#f1f5f9;font-size:1.6rem;font-weight:800;margin:0 0 12px'>{bi('globe2','1.2rem')} Job Search</h2>", unsafe_allow_html=True)

    sc1,sc2,sc3,sc4 = st.columns(4)
    with sc1: q        = st.text_input("Job title / keyword", placeholder="Python Developer", key="js_q")
    with sc2: location = st.text_input("Location", placeholder="Bengaluru", key="js_loc")
    with sc3: jtype    = st.selectbox("Type", ["All","Full-time","Part-time","Freelance","Contract"], key="js_type")
    with sc4: status_f = st.selectbox("Show", ["All","Legit only","Hide Fraud"], key="js_status")

    if st.button("Search", use_container_width=False, key="js_btn"):
        st.session_state.js_searched = True

    results = JOB_MOCK.copy()
    if q:           results = [j for j in results if q.lower() in j["title"].lower() or any(q.lower() in t.lower() for t in j["tags"])]
    if location:    results = [j for j in results if location.lower() in j["location"].lower() or j["location"]=="Remote"]
    if jtype!="All":results = [j for j in results if j["type"]==jtype]
    if status_f=="Legit only": results = [j for j in results if j["status"]=="Legit"]
    if status_f=="Hide Fraud": results = [j for j in results if j["status"]!="Fraud"]

    st.markdown(f"<div style='color:var(--text2);font-size:.8rem;margin:8px 0'>{len(results)} jobs found</div>", unsafe_allow_html=True)

    for j in results:
        sc = STATUS_CLASS.get(j["status"],"")
        em = bi(STATUS_EMOJI.get(j["status"],"clipboard"), '1em', {'Legit':'#10b981','Suspicious':'#f59e0b','Fraud':'#ef4444'}.get(j['status'],'#94a3b8'))
        with st.container():
            c1, c2 = st.columns([4,1])
            with c1:
                tags_html = "".join(f"<span class='tag' style='background:var(--bg3); color:var(--text2); border:1px solid var(--border);'>{t}</span>" for t in j["tags"])
                st.markdown(f"""
                <div class="table-card" style="padding:15px; border-left: 4px solid { '#1ABB9C' if j['status']=='Legit' else '#F39C12' if j['status']=='Suspicious' else '#E74C3C' };">
                  <div style="display:flex;justify-content:space-between;align-items:start">
                    <div>
                      <div style="font-size:16px; font-weight:600; color:var(--text); margin-bottom:2px;">{em} {j['title']}</div>
                      <div style="color:var(--text2); font-size:13px;">{j['company']} · {j['location']} · {j['type']}</div>
                    </div>
                    <div style="text-align:right">
                      <div style="font-weight:700;color:#1ABB9C;font-size:14px">{j['salary']}</div>
                      <div style="color:var(--text3);font-size:11px; margin-top:2px;">{j['exp']}</div>
                    </div>
                  </div>
                  <div style="margin-top:12px; display:flex; flex-wrap:wrap; gap:5px;">{tags_html}</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Save", key=f"js_sv_{j['title']}", use_container_width=True):
                    db.save_job(uid, j["title"], j["company"], j.get("url","#"), j["status"])
                    st.success("Saved!")
                if st.button("Analyze", key=f"js_an_{j['title']}", use_container_width=True):
                    with st.spinner("Analyzing…"):
                        result = simulate_analysis(j.get("url","#"))
                    db.add_job_analysis(uid, j.get("url","#"), j["title"], j["company"],
                                        result["status"], result["confidence"], result["details"])
                    _show_result(result, j.get("url","#"))


# ══════════════════════════════════════════════════════════════════════════════
#  SAVED JOBS & APPLICATIONS
# ══════════════════════════════════════════════════════════════════════════════
