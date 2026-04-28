import streamlit as st

def load_css():
    st.markdown('<link href="https://cdn.jsdelivr.net/npm/remixicon@4.2.0/fonts/remixicon.css" rel="stylesheet" />', unsafe_allow_html=True)
    st.markdown("""
<style>

:root {
    --bg:        #111111;
    --bg2:       #1E1E1E;
    --bg3:       #181818;
    --sidebar:   #0D0D0D;
    --sidebar-hov:#1A1A1A;
    --sidebar-txt:#D1D1D1;
    --blue:      #3788D8;
    --blue-d:    #2C6DBA;
    --teal:      #1ABC9C;
    --green:     #1ABB9C;
    --yellow:    #F39C12;
    --red:       #E74C3C;
    --purple:    #9B59B6;
    --text:      #ECECEC;
    --text2:     #A0A0A0;
    --text3:     #707070;
    --border:    #333333;
    --border2:   #444444;
    --radius:    4px;
    --radius-sm: 3px;
    --shadow:    0 2px 8px rgba(0,0,0,0.3);
}

*, *::before, *::after { box-sizing: border-box; }

/* ── App shell ───────────────────────────────── */
.stApp                    { background: var(--bg); font-family: "Helvetica Neue", Roboto, Arial, sans-serif; color: var(--text); }
.block-container          { padding-top: 1rem !important; max-width: 1300px !important; }
#MainMenu,footer,header   { visibility: hidden; }
section[data-testid="stSidebar"] { background: var(--sidebar) !important; border-right: none !important; }
section[data-testid="stSidebar"] > div { background: var(--sidebar) !important; }

/* ── Sidebar nav buttons ─────────────────────── */
div[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: var(--sidebar-txt) !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 10px 20px !important;
    margin: 0 !important;
    text-align: left !important;
    justify-content: flex-start !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    transition: all .2s ease !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
}
div[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--sidebar-hov) !important;
    color: #fff !important;
    border-left: 4px solid var(--green) !important;
}
div[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1); margin: 10px 0; }

/* ── Main action buttons ─────────────────────── */
.stButton > button {
    background: var(--blue) !important;
    color: white !important;
    border: 1px solid var(--blue-d) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
}
.stButton > button:hover { background: var(--blue-d) !important; }
.stButton > button[kind="secondary"] {
    background: var(--bg3) !important;
    border: 1px solid var(--border2) !important;
    color: var(--text) !important;
}
.stButton > button[kind="secondary"]:hover { background: var(--border) !important; }

/* ── Inputs ──────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 0 !important;
    box-shadow: inset 0 1px 1px rgba(0,0,0,.1);
}
.stTextInput label, .stTextArea label, .stSelectbox label {
    color: var(--text2) !important;
    font-weight: 600 !important;
}

/* ── Tabs ────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 2px solid var(--border) !important;
    gap: 15px !important;
}
.stTabs [data-baseweb="tab"] {
    color: var(--text2) !important;
    font-weight: 600 !important;
    border: none !important;
    background: transparent !important;
    padding: 10px 15px !important;
}
.stTabs [aria-selected="true"] { 
    color: var(--text) !important; 
    border-bottom: 3px solid var(--blue) !important;
}

/* ── Custom cards ────────────────────────────── */
.card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 15px;
    margin-bottom: 20px;
    box-shadow: var(--shadow);
}
.card p, .card div, .card span {
    color: var(--text);
}

/* ── Resume preview (Live Preview) ───────────── */
.rp-card {
    background: #ffffff !important;
    color: #1a1a1a !important;
    border-radius: var(--radius);
    padding: 2.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    font-family: 'Inter', 'Segoe UI', serif;
    max-width: 800px;
    margin: 0 auto;
    border: 1px solid #e2e8f0;
}
.rp-name {
    font-size: 2.2rem;
    font-weight: 800;
    color: #1e293b;
    margin: 0 0 0.2rem;
    letter-spacing: -0.025em;
}
.rp-contact {
    font-size: 0.85rem;
    color: #64748b;
    display: flex;
    flex-wrap: wrap;
    gap: 0.8rem;
    margin-bottom: 0.6rem;
    font-family: sans-serif;
}
.rp-hr {
    border: none;
    border-top: 2px solid #3b82f6;
    margin: 0.6rem 0 1.2rem;
}
.rp-sec {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1e293b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 1.5rem 0 0.6rem;
    border-bottom: 2px solid #f1f5f9;
    padding-bottom: 0.3rem;
    font-family: sans-serif;
}
.rp-etitle {
    font-weight: 700;
    font-size: 1rem;
    color: #0f172a;
    font-family: sans-serif;
}
.rp-esub {
    font-size: 0.9rem;
    color: #3b82f6;
    font-weight: 600;
    font-family: sans-serif;
}
.rp-edate {
    font-size: 0.85rem;
    color: #94a3b8;
    white-space: nowrap;
    font-family: sans-serif;
}
.rp-edesc {
    font-size: 0.95rem;
    color: #334155;
    line-height: 1.6;
    margin-top: 0.4rem;
    font-family: sans-serif;
}
.rp-chip {
    background: #eff6ff;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
    border-radius: 6px;
    padding: 0.25rem 0.75rem;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
    margin: 3px;
    font-family: sans-serif;
}
.x_panel {
    background: var(--bg2);
    border: 1px solid var(--border);
    padding: 10px 17px;
    margin-bottom: 10px;
    border-radius: 4px;
}
.x_title {
    border-bottom: 2px solid var(--border);
    padding: 1px 5px 6px;
    margin-bottom: 10px;
}
.x_title h2 {
    margin: 5px 0 6px;
    font-size: 18px;
    font-weight: 400;
    color: var(--text2);
}

/* ── Tile Stats (KPI Blocks) ─────────────────── */
.tile-stats {
    position: relative;
    display: block;
    margin-bottom: 12px;
    border: 1px solid var(--border);
    border-radius: 4px;
    overflow: hidden;
    color: #fff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.tile-stats .inner {
    padding: 15px;
}
.tile-stats h3 {
    font-size: 38px !important;
    font-weight: bold !important;
    margin: 0 0 5px 0 !important;
    white-space: nowrap !important;
    text-align: right !important;
    line-height: 1 !important;
    color: #fff !important;
}
.tile-stats p {
    font-size: 14px;
    margin: 0;
    text-align: right;
    opacity: 0.9;
    font-weight: 500;
    color: #fff !important;
}
.tile-stats .icon {
    position: absolute;
    top: 15px;
    left: 15px;
    font-size: 45px;
    color: rgba(255,255,255,0.3);
}
.tile-stats .footer {
    background: rgba(0,0,0,0.1);
    padding: 8px 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    font-weight: 600;
}

.bg-darkblue { background: #34495E; border-color: #2e4154; }
.bg-green    { background: #1ABB9C; border-color: #18a98c; }
.bg-teal     { background: #1ABC9C; border-color: #18a98c; }
.bg-red      { background: #E74C3C; border-color: #e43725; }
.bg-blue     { background: #337AB7; border-color: #2e6da4; }
.bg-purple   { background: #9B59B6; border-color: #8c49a6; }
.bg-orange   { background: #F39C12; border-color: #da8c10; }

/* ── Table / Cards with Header ───────────────── */
.table-card {
    background: var(--bg2);
    border-radius: 4px;
    border: 1px solid var(--border);
    overflow: hidden;
    margin-bottom: 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.2);
}
.table-header {
    padding: 12px 15px;
    color: #fff;
    font-size: 15px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
}
.table-header-darkblue { background: #34495E; }
.table-header-teal { background: #1ABC9C; }

/* ── Status Badges ───────────────────────────── */
.badge {
    display: inline-block; padding: 4px 10px;
    border-radius: 2px; font-size: 11px; font-weight: 600;
    text-transform: uppercase;
}
.badge-green  { background: #1ABB9C; color: #fff; }
.badge-yellow { background: #F39C12; color: #fff; }
.badge-red    { background: #E74C3C; color: #fff; }
.badge-blue   { background: #337AB7; color: #fff; }
.badge-gray   { background: #94a3b8; color: #fff; }

/* ── Topbar ──────────────────────────────────── */
.topbar {
    display: flex; justify-content: space-between; align-items: center;
    background: var(--bg2); border-bottom: 1px solid var(--border);
    padding: 12px 20px; margin: -1rem -1rem 20px -1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.2);
}
.topbar-title { color: var(--text2); font-size: 1.3rem; font-weight: 500; }
.topbar-item { display: flex; align-items: center; gap: 8px; color: var(--sidebar-txt); font-size: 14px; font-weight: 500; }

/* ── Sidebar profile / Logo ──────────────────── */
.logo-wrap { padding: 10px 20px; color: #ECF0F1; font-size: 22px; font-weight: 400; display: flex; align-items: center; gap: 10px; }
.logo-wrap span { font-weight: bold; }
.profile_info { padding: 15px 20px 10px; display: flex; align-items: center; gap: 15px; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 10px; }
.profile_info img { border-radius: 50%; width: 45px; height: 45px; border: 2px solid var(--border); }
.profile_info_text span { font-size: 12px; color: #BAB8B8; }
.profile_info_text h2 { font-size: 14px; color: #ECF0F1; margin: 0; font-weight: 600; }

/* Typography overrides */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5 {
    color: var(--text2) !important;
    font-family: "Helvetica Neue", Roboto, Arial, sans-serif !important;
}
.stMarkdown p { color: var(--text); }

/* Miscellaneous fixes */
.timeline-item { display: flex; gap: 12px; padding: 10px 0; border-bottom: 1px solid var(--border); }
.timeline-dot { width: 10px; height: 10px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; background: var(--border2); }
</style>
""", unsafe_allow_html=True)

# ── Icon helper (Bootstrap Icons) ─────────────────────────────────────────────
