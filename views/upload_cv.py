import streamlit as st
import os
import time
import json
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
from config import *

def render_upload_cv():
    uid = st.session_state.user_id
    st.markdown(f"<h2 style='font-family: sans-serif;color:#f1f5f9;font-size:1.6rem;font-weight:800;margin:0 0 12px'>{bi('file-earmark-arrow-up','1.2rem')} Upload CV</h2>", unsafe_allow_html=True)

    uploaded = st.file_uploader("Choose your CV file", type=["pdf","doc","docx"],
                                 help="Upload your resume in PDF or Word format")
    if uploaded:
        import os
        os.makedirs("uploads", exist_ok=True)
        fpath = f"uploads/{uploaded.name}"
        with open(fpath,"wb") as f: f.write(uploaded.getbuffer())
        size = uploaded.size
        db.upload_resume(uid, uploaded.name, fpath, size)
        st.success(f"Uploaded: {uploaded.name}")
        db.add_notification(f"Resume uploaded: {uploaded.name}")

    resumes = db.get_user_resumes(uid)
    if resumes:
        st.markdown("#### Your Uploaded Resumes")
        for r in resumes:
            c1,c2 = st.columns([4,1])
            with c1:
                st.markdown(f"""
                <div class="card">
                  <div style="font-weight:700;color:#f1f5f9">{bi('paperclip','1em')} {r['file_name']}</div>
                  <div style="color:#64748b;font-size:.78rem">Uploaded: {r['upload_date']} · {r.get('size',0)//1024} KB</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                if st.button("Delete", key=f"del_res_{r['id']}", use_container_width=True):
                    db.delete_resume(uid, r["id"])
                    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  RESUME BUILDER
# ══════════════════════════════════════════════════════════════════════════════
