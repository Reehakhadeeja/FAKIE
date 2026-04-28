import streamlit as st
import time
import json
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
from config import *

def render_notes():
    uid = st.session_state.user_id
    st.markdown(f"<h2 style='font-family: sans-serif;color:#f1f5f9;font-size:1.6rem;font-weight:800;margin:0 0 12px'>{bi('journal-text','1.2rem')} Notes</h2>", unsafe_allow_html=True)

    with st.expander("＋ Add Note", expanded=False):
        n_title   = st.text_input("Title", placeholder="Interview prep for Flipkart", key="note_title")
        n_content = st.text_area("Content", height=100, placeholder="Questions asked, impressions, follow-up actions…", key="note_content")
        if st.button("Save Note", key="note_save"):
            if n_title.strip():
                db.add_note(uid, n_title, n_content)
                st.success("Note saved!")
                st.rerun()
            else:
                st.error("Title required.")

    notes = db.get_notes(uid)
    if not notes:
        st.info("No notes yet. Create one above!")
        return
    for n in notes:
        c1,c2 = st.columns([5,1])
        with c1:
            with st.expander(f"{n['title']} — {n['created_at']}"):
                st.markdown(f"<div style='color:#94a3b8;font-size:.85rem;line-height:1.65'>{n['content'].replace(chr(10),'<br>')}</div>", unsafe_allow_html=True)
        with c2:
            if st.button("Delete", key=f"del_note_{n['id']}", use_container_width=True):
                db.delete_note(uid, n["id"]); st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  FILES
# ══════════════════════════════════════════════════════════════════════════════
