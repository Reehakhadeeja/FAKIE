import streamlit as st
import time
import random
from datetime import datetime
import re
from config import *

def bi(name, size="1em", color="inherit", extra_style=""):
    """Return an inline Remix Icon <i> tag. Maps Bootstrap Icon names to Remix Icons."""
    mapping = {
        "search-heart": "search-heart-line",
        "house-door": "home-4-line",
        "search": "search-line",
        "globe2": "global-line",
        "bar-chart-line": "bar-chart-line",
        "bookmark": "bookmark-line",
        "send": "send-plane-line",
        "cloud-upload": "upload-cloud-2-line",
        "file-earmark-person": "file-user-line",
        "envelope-paper": "mail-open-line",
        "robot": "robot-line",
        "rocket-takeoff": "rocket-line",
        "journal-text": "book-read-line",
        "folder2-open": "folder-open-line",
        "bell": "notification-3-line",
        "gem": "vip-diamond-line",
        "gear": "settings-4-line",
        "person-circle": "user-3-line",
        "bell-fill": "notification-3-fill",
        "check-circle-fill": "checkbox-circle-fill",
        "exclamation-triangle-fill": "alert-fill",
        "shield-exclamation": "shield-star-fill",
        "info-circle": "information-fill",
        "check": "check-line",
        "pin-angle": "pushpin-line",
        "clipboard-check": "clipboard-line",
        "trophy-fill": "trophy-fill",
        "award-fill": "award-fill",
        "star-fill": "star-fill",
        "emoji-smile": "emotion-line",
        "chat-dots-fill": "message-3-fill",
        "heart-fill": "heart-3-fill",
        "chevron-left": "arrow-left-s-line",
        "chevron-right": "arrow-right-s-line",
        "trash": "delete-bin-line",
        "copy": "clipboard-line",
        "plus-circle": "add-circle-line",
        "upload": "upload-2-line",
        "calendar": "calendar-line",
        "list-task": "list-check",
        "card-text": "article-line",
        "credit-card": "bank-card-line",
        "x-circle": "close-circle-line",
        "circle": "checkbox-blank-circle-line",
        "eye": "eye-line",
        "eye-slash": "eye-off-line",
        "box-arrow-right": "logout-box-r-line",
        "file-earmark-pdf": "file-pdf-line",
        "download": "download-2-line",
        "play": "play-line",
        "pause": "pause-line",
        "stop": "stop-line",
        "arrow-repeat": "refresh-line",
        "pencil": "pencil-line"
    }
    ri_name = mapping.get(name, name)
    if not ri_name.startswith('ri-'):
        ri_name = f"ri-{ri_name}"
    return f'<i class="{ri_name}" style="font-size:{size};color:{color};{extra_style}"></i>'

# ── Helpers ───────────────────────────────────────────────────────────────────
def simulate_analysis(url: str) -> dict:
    time.sleep(1.8)
    weights     = [0.55, 0.25, 0.20]
    status      = random.choices(["Legit","Suspicious","Fraud"], weights=weights)[0]
    confidence  = {"Legit": random.uniform(0.82, 0.96), "Suspicious": random.uniform(0.58, 0.78), "Fraud": random.uniform(0.88, 0.98)}[status]
    num_flags   = {"Legit": random.randint(0,2), "Suspicious": random.randint(2,5), "Fraud": random.randint(5,8)}[status]
    num_pos     = {"Legit": random.randint(4,7), "Suspicious": random.randint(1,3), "Fraud": random.randint(0,1)}[status]
    risk_score  = {"Legit": random.randint(5,25), "Suspicious": random.randint(35,65), "Fraud": random.randint(75,98)}[status]
    return {
        "status":       status,
        "confidence":   confidence,
        "risk_score":   risk_score,
        "title":        random.choice(FAKE_TITLES),
        "company":      random.choice(FAKE_COMPANIES),
        "details":      random.choice(FAKE_DETAILS[status]),
        "red_flags":    random.sample(RED_FLAGS, k=num_flags),
        "pos_signals":  random.sample(POSITIVE_SIGNALS, k=num_pos),
        "analyzed_at":  datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

def is_valid_email(e): return bool(re.match(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$", e))
def is_valid_phone(p): return bool(re.match(r"^[\d\s\+\-\(\)]{7,15}$", p))


# ── PDF builder ───────────────────────────────────────────────────────────────
def _show_result(r: dict, url: str, compact=False):
    cls    = STATUS_CLASS.get(r["status"],"")
    emoji  = bi(STATUS_EMOJI.get(r["status"],"clipboard"), '1em', {'Legit':'#1ABB9C','Suspicious':'#F39C12','Fraud':'#E74C3C'}.get(r['status'],'#999'))
    clr_b  = STATUS_COLOR.get(r["status"],"blue")

    if compact:
        st.markdown(f"""
        <div class="table-card" style="padding:15px; border-left:4px solid {'#1ABB9C' if r['status']=='Legit' else '#F39C12' if r['status']=='Suspicious' else '#E74C3C'};">
          <div style="display:flex;justify-content:space-between">
            <div style="font-size:14px;font-weight:700;color:#2A3F54">{emoji} {r['title']} @ {r['company']}</div>
            <div class="badge badge-{clr_b}">{r['status']}</div>
          </div>
          <div style="color:#73879C;font-size:12px">{url[:60]}…</div>
        </div>""", unsafe_allow_html=True)
        return

    col_l, col_r = st.columns([2,1])
    with col_l:
        st.markdown(f"""
        <div class="table-card" style="padding:20px; border-top: 3px solid {'#1ABB9C' if r['status']=='Legit' else '#F39C12' if r['status']=='Suspicious' else '#E74C3C'};">
          <div style="display:flex;align-items:center;gap:15px;margin-bottom:15px">
            <span style="font-size:2.5rem; line-height:1;">{emoji}</span>
            <div>
              <div style="font-size:1.25rem;font-weight:700;color:#2A3F54">{r['status']} Verification</div>
              <div style="color:#73879C;font-size:13px">Confidence: {r['confidence']:.1%} · Risk score: {r['risk_score']}/100</div>
            </div>
          </div>
          <div style="color:#73879C;margin-bottom:6px"><b style="color:#2A3F54">Job Position:</b> {r['title']}</div>
          <div style="color:#73879C;margin-bottom:6px"><b style="color:#2A3F54">Company:</b> {r['company']}</div>
          <div style="color:#555;font-size:14px;line-height:1.6;margin-top:15px; padding:10px; background:#f9f9f9; border-radius:4px;">{r['details']}</div>
        </div>""", unsafe_allow_html=True)

    with col_r:
        if r.get("red_flags"):
            flags_html = "".join(f"<div style='color:#E74C3C;font-size:13px;margin:5px 0; display:flex; gap:8px;'>{bi('flag-fill','1em','#E74C3C')} <span>{f}</span></div>" for f in r["red_flags"])
            st.markdown(f"""
            <div class="table-card" style="padding:15px; border-left:4px solid #E74C3C">
              <div style="font-weight:700;color:#E74C3C;margin-bottom:10px;font-size:12px;text-transform:uppercase;letter-spacing:1px;">RED FLAGS DETECTED</div>
              {flags_html}
            </div>""", unsafe_allow_html=True)
        if r.get("pos_signals"):
            sig_html = "".join(f"<div style='color:#1ABB9C;font-size:13px;margin:5px 0; display:flex; gap:8px;'>{bi('check-circle-fill','1em','#1ABB9C')} <span>{s}</span></div>" for s in r["pos_signals"])
            st.markdown(f"""
            <div class="table-card" style="padding:15px; border-left:4px solid #1ABB9C">
              <div style="font-weight:700;color:#1ABB9C;margin-bottom:10px;font-size:12px;text-transform:uppercase;letter-spacing:1px;">POSITIVE SIGNALS</div>
              {sig_html}
            </div>""", unsafe_allow_html=True)

    # Action bar
    a1,a2,a3 = st.columns(3)
    with a1:
        if st.button("Save Job", use_container_width=True, key=f"save_{r['analyzed_at']}"):
            db.save_job(st.session_state.user_id, r["title"], r["company"], url, r["status"])
            st.success("Saved!")
    with a2:
        if st.button("Generate Cover Letter", use_container_width=True, key=f"cl_{r['analyzed_at']}"):
            st.session_state.cl_prefill_title   = r["title"]
            st.session_state.cl_prefill_company = r["company"]
            st.session_state.current_page = "cover_letters"
            st.rerun()
    with a3:
        report = f"SniffJob Analysis Report\n{'='*40}\nJob: {r['title']}\nCompany: {r['company']}\nStatus: {r['status']}\nConfidence: {r['confidence']:.1%}\nRisk Score: {r['risk_score']}/100\n\n{r['details']}\n\nRed Flags:\n" + "\n".join(f"  - {f}" for f in r.get("red_flags",[])) + "\n\nPositive Signals:\n" + "\n".join(f"  + {s}" for s in r.get("pos_signals",[]))
        st.download_button("Export Report", data=report, file_name="sniffjob_report.txt",
                           mime="text/plain", use_container_width=True, key=f"exp_{r['analyzed_at']}")


# ══════════════════════════════════════════════════════════════════════════════
#  SNIFF HISTORY
# ══════════════════════════════════════════════════════════════════════════════
