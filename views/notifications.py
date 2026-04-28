import streamlit as st
import time
import json
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
from config import *

def render_notifications():
    # st.markdown(f"<h2 style='font-family: sans-serif;color:#f1f5f9;font-size:1.6rem;font-weight:800;margin:0 0 12px'>{bi('bell','1.2rem')} Notifications</h2>", unsafe_allow_html=True)
    if st.button("Mark All Read", key="notif_read"):
        db.mark_all_read(); st.rerun()
    notifs = db.get_all_notifications()
    if not notifs:
        st.info("No notifications.")
    for n in notifs:
        icon  = bi('circle-fill','0.5em','var(--blue)') if not n["read"] else bi('circle','0.5em','var(--text3)')
        alpha = "1" if not n["read"] else "0.7"
        st.markdown(f"""
        <div class="table-card" style="opacity:{alpha}; margin-bottom:8px; padding:12px 15px; border-left: 3px solid {'var(--blue)' if not n['read'] else 'var(--border)'}; background: var(--bg2);">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div style="color:var(--text);font-size:14px; font-weight:{'600' if not n['read'] else '400'}">{icon} {n['msg']}</div>
            <div style="color:var(--text3);font-size:12px;">{n['ts']}</div>
          </div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════════════
#  SETTINGS
# ══════════════════════════════════════════════════════════════════════════════
