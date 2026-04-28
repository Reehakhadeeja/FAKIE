import streamlit as st
import time
import json
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
from config import *

def render_history():
    uid  = st.session_state.user_id
    # st.markdown(f"<h2 style='font-family: sans-serif;color:#f1f5f9;font-size:1.6rem;font-weight:800;margin:0 0 12px'>{bi('clock-history','1.2rem')} Sniff History</h2>", unsafe_allow_html=True)

    hist = db.get_job_history(uid)
    if not hist:
        st.markdown(f"""
        <div style="text-align:center;padding:60px 20px; border: 2px dashed var(--border); border-radius:8px; background:var(--bg3);">
          <div style="font-size:4rem; line-height:1;">{bi('clipboard-data-fill','4rem','var(--border)')}</div>
          <div style="color:var(--text2);font-size:1.2rem;font-weight:600;margin-top:15px">No history found</div>
          <div style="color:var(--text3);font-size:14px;margin-top:6px">Analyze a job post to see it here in your history.</div>
        </div>""", unsafe_allow_html=True)
        return

    # Filters
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        filter_status = st.selectbox("Filter by status", ["All","Legit","Suspicious","Fraud"], key="hist_filter")
    with fc2:
        sort_by = st.selectbox("Sort by", ["Newest","Oldest","Confidence ↑","Confidence ↓"], key="hist_sort")
    with fc3:
        search_q = st.text_input("Search", placeholder="Title or company…", key="hist_search")

    filtered = [j for j in hist if (filter_status=="All" or j["result"]==filter_status)
                and (not search_q or search_q.lower() in j["job_title"].lower() or search_q.lower() in j["company"].lower())]

    if sort_by == "Oldest":          filtered = filtered[::-1]
    elif sort_by == "Confidence ↑":  filtered.sort(key=lambda x: x["confidence_score"])
    elif sort_by == "Confidence ↓":  filtered.sort(key=lambda x: x["confidence_score"], reverse=True)

    st.markdown(f"<div style='color:var(--text2);font-size:.8rem;margin-bottom:12px'>{len(filtered)} result(s)</div>", unsafe_allow_html=True)

    for j in filtered:
        cls   = STATUS_CLASS.get(j["result"],"")
        emoji = bi(STATUS_EMOJI.get(j["result"],"clipboard"), '1em', {'Legit':'#10b981','Suspicious':'#f59e0b','Fraud':'#ef4444'}.get(j['result'],'#94a3b8'))
        clr_b = STATUS_COLOR.get(j["result"],"blue")
        with st.expander(f"{j['job_title']} @ {j['company']} — {j['result']} ({j['confidence_score']:.0%})"):
            c1,c2 = st.columns([3,1])
            with c1:
                st.markdown(f"""
                <div class="table-card" style="padding:15px; border-left: 4px solid { '#1ABB9C' if j['result']=='Legit' else '#F39C12' if j['result']=='Suspicious' else '#E74C3C' };">
                  <div style="display:flex;justify-content:space-between;margin-bottom:10px; align-items:center;">
                    <span class="badge badge-{clr_b}">{j['result']}</span>
                    <div style="color:var(--text3);font-size:12px;">{bi('calendar-event')} {j['timestamp']}</div>
                  </div>
                  <div style="color:var(--text);font-size:13px;margin-bottom:6px">
                    <b style="color:var(--text2)">Source URL:</b> <a href="{j['job_url']}" target="_blank" style="color:var(--blue); text-decoration:none;">{j['job_url'][:60]}…</a>
                  </div>
                  <div style="color:var(--text);font-size:13px;margin-bottom:6px"><b style="color:var(--text2)">Confidence Level:</b> {j['confidence_score']:.1%}</div>
                  <div style="background:var(--bg3); padding:10px; border-radius:4px; color:var(--text); font-size:13px; line-height:1.6; border:1px solid var(--border);">{j['details']}</div>
                  {f"<div style='color:var(--text2);font-size:12px;margin-top:10px; padding-top:10px; border-top:1px solid var(--border);'><b>Analysis Note:</b> {j.get('notes','')}</div>" if j.get('notes') else ""}
                </div>""", unsafe_allow_html=True)
            with c2:
                if st.button("Save", key=f"hist_save_{j['id']}", use_container_width=True):
                    db.save_job(st.session_state.user_id, j["job_title"], j["company"], j["job_url"], j["result"])
                    st.success("Saved!")
                if st.button("Delete", key=f"hist_del_{j['id']}", use_container_width=True):
                    db.delete_job_analysis(uid, j["id"])
                    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  JOB SEARCH
# ══════════════════════════════════════════════════════════════════════════════
