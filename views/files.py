import streamlit as st
import time
import json
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
from config import *

def render_files():
    uid = st.session_state.user_id
    st.markdown(f"<h2 style='font-family: sans-serif;color:#f1f5f9;font-size:1.6rem;font-weight:800;margin:0 0 12px'>{bi('folder2-open','1.2rem')} Files</h2>", unsafe_allow_html=True)
    resumes = db.get_user_resumes(uid)
    cls     = db.get_cover_letters(uid)
    notes   = db.get_notes(uid)
    analyses= db.get_job_history(uid)

    c1,c2,c3,c4 = st.columns(4)
    for col,label,val,icon in [(c1,"Resumes",len(resumes),bi('file-earmark-person','1.6rem','#3b82f6')),(c2,"Cover Letters",len(cls),bi('envelope-paper','1.6rem','#8b5cf6')),(c3,"Notes",len(notes),bi('journal-text','1.6rem','#f59e0b')),(c4,"Analyses",len(analyses),bi('search','1.6rem','#10b981'))]:
        with col:
            st.markdown(f"""
            <div class="stat-box">
              <div style="font-size:1.6rem">{icon}</div>
              <div class="stat-num">{val}</div>
              <div class="stat-lbl">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### All Exported Files")
    # Export all analyses as JSON
    if analyses:
        export_data = json.dumps(analyses, indent=2)
        st.download_button("Export All Analyses (JSON)", data=export_data,
                           file_name="sniffjob_analyses.json", mime="application/json")
    if cls:
        all_cls = "\n\n" + "="*50 + "\n\n".join(f"{c['title']} @ {c['company']}\n{c['content']}" for c in cls)
        st.download_button("Export All Cover Letters (.txt)", data=all_cls,
                           file_name="cover_letters.txt", mime="text/plain")


# ══════════════════════════════════════════════════════════════════════════════
#  NOTIFICATIONS
# ══════════════════════════════════════════════════════════════════════════════
