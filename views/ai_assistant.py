import streamlit as st
import time
import json
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
from config import *

def render_ai_assistant():
    st.markdown(f"<h2 style='font-family: sans-serif;color:#f1f5f9;font-size:1.6rem;font-weight:800;margin:0 0 12px'>{bi('robot','1.2rem')} AI Assistant</h2>", unsafe_allow_html=True)
    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = [
            {"role":"assistant","content":f"{bi('search-heart','1em','#3b82f6')} Hi! I'm your SniffJob AI assistant. Ask me anything about job hunting, resume tips, interview prep, or salary negotiation!"}
        ]

    # Display messages
    for msg in st.session_state.ai_messages:
        role  = msg["role"]
        color = "#1e3a5f" if role=="assistant" else "#1e293b"
        align = "left" if role=="assistant" else "right"
        icon  = bi('robot','1em','#3b82f6') if role=="assistant" else bi('person','1em')
        st.markdown(f"""
        <div style="text-align:{align};margin:8px 0">
          <div style="display:inline-block;background:{color};border-radius:12px;padding:12px 16px;max-width:75%;text-align:left">
            <div style="font-size:.75rem;color:#64748b;margin-bottom:4px">{icon} {role.title()}</div>
            <div style="color:#f1f5f9;font-size:.88rem;line-height:1.6">{msg["content"]}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    # Quick prompts
    st.markdown("**Quick prompts:**")
    qp1,qp2,qp3,qp4 = st.columns(4)
    quick_prompts = [
        ("Resume tips", "What are the top 5 resume tips for tech jobs in India?"),
        ("Salary negotiation", "How do I negotiate a better salary offer?"),
        ("Spot fake jobs", "How can I identify a fake job posting?"),
        ("Interview prep", "What are common behavioral interview questions?"),
    ]
    for (col,(label,prompt)) in zip([qp1,qp2,qp3,qp4],quick_prompts):
        with col:
            if st.button(label, use_container_width=True, key=f"qp_{label}"):
                st.session_state.ai_messages.append({"role":"user","content":prompt})
                st.session_state.ai_pending = prompt
                st.rerun()

    user_input = st.chat_input("Ask me anything about jobs, resumes, interviews…")
    if user_input:
        st.session_state.ai_messages.append({"role":"user","content":user_input})
        st.session_state.ai_pending = user_input
        st.rerun()

    if "ai_pending" in st.session_state and st.session_state.ai_pending:
        pending = st.session_state.pop("ai_pending")
        with st.spinner("Thinking…"):
            time.sleep(0.8)
            # Mock smart responses
            responses = {
                "resume": "Great question! For tech resumes in India: (1) Keep it 1-2 pages, (2) Lead with a strong summary, (3) Quantify achievements (e.g., 'improved performance by 40%'), (4) List skills with proficiency levels, (5) Include GitHub/portfolio links. Use ATS-friendly formatting — avoid tables and graphics in the main content.",
                "salary": "Salary negotiation tips: (1) Always research market rates on Glassdoor/Levels.fyi first, (2) Let them make the first offer, (3) Negotiate the full package — not just base pay, (4) Use silence as a tactic, (5) Be ready to walk away. In India, a 20-30% hike from current CTC is typical when switching jobs.",
                "fake": "Key red flags for fake jobs: 🚩 Salary too good to be true, 🚩 Vague job description, 🚩 Requests money or bank details, 🚩 Contact is a free email (gmail/yahoo), 🚩 No company address or registration, 🚩 Immediate WhatsApp hiring. Always verify the company on LinkedIn and MCA portal.",
                "interview": "Common behavioral questions: (1) Tell me about yourself, (2) Greatest achievement, (3) Failure and what you learned, (4) Conflict resolution, (5) Why this company? Use the STAR method: Situation → Task → Action → Result for structured, compelling answers.",
            }
            reply = "That's a great question! Here are some insights based on current job market trends in India: job hunting requires a combination of a strong resume, smart application strategy, and interview preparation. Feel free to ask me about any specific aspect — resume writing, interview prep, salary negotiation, or how to spot fake jobs!"
            for kw,ans in responses.items():
                if kw.lower() in pending.lower():
                    reply = ans; break
        st.session_state.ai_messages.append({"role":"assistant","content":reply})
        st.rerun()

    if st.button("Clear Chat", key="ai_clear"):
        st.session_state.ai_messages = [st.session_state.ai_messages[0]]
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  EASYAPPLY KIT
# ══════════════════════════════════════════════════════════════════════════════
