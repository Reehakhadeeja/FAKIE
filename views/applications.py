import streamlit as st
import time
import json
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
from config import *

def render_applications():
    uid = st.session_state.user_id
    st.markdown(f"<h2 style='font-family: sans-serif;color:var(--text);font-size:1.6rem;font-weight:800;margin:0 0 12px'>{bi('kanban','1.2rem')} Applications Tracker</h2>", unsafe_allow_html=True)
    applied = db.get_applied_jobs(uid)
    if not applied:
        st.info("No applications tracked yet.")
        return

    # Kanban columns
    st.markdown("#### Application Kanban")
    stages = ["Applied","Interview","Offer","Rejected"]
    cols = st.columns(len(stages))
    for col, stage in zip(cols, stages):
        with col:
            # mock distribute
            items = [j for j in applied if hash(j["id"] + hash(stage)) % 4 == stages.index(stage)]
            colors_k = {"Applied":"#3b82f6","Interview":"#f59e0b","Offer":"#10b981","Rejected":"#ef4444"}
            st.markdown(f"""
            <div class="kanban-col">
              <div class="kanban-title" style="color:{colors_k.get(stage,'#94a3b8')}">{stage} ({len(applied) if stage=='Applied' else 0})</div>""",
                unsafe_allow_html=True)
            if stage == "Applied":
                for j in applied:
                    st.markdown(f"<div class='card' style='padding:10px;margin:4px 0'><div style='font-size:.8rem;font-weight:600;color:var(--text)'>{j['title']}</div><div style='font-size:.75rem;color:var(--text2)'>{j['company']}</div></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  UPLOAD CV
# ══════════════════════════════════════════════════════════════════════════════
