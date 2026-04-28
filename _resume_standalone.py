import streamlit as st
import pandas as pd
from datetime import datetime

def render_resume_page():
    """Render the resume builder page as a standalone component"""
    # ---------- PAGE CONFIG ----------
    st.set_page_config(page_title="Resume Builder", layout="wide")

    # ---------- CUSTOM CSS (White + Light Green Theme) ----------
    st.markdown("""
    <style>
    /* Overall background */
    .stApp {
        background-color: #f8faf8;
    }
    
    /* Cards and containers */
    div[data-testid="stForm"] {
        background-color: white;
        border: 1px solid #d1f0d1;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,40,0,0.05);
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #1b5e20;
        box-shadow: 0 2px 8px rgba(46,125,50,0.3);
    }
    
    /* Section headers */
    h2, h3 {
        color: #1b5e20 !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 1px solid #c8e6c9 !important;
        border-radius: 8px !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #2e7d32 !important;
        box-shadow: 0 0 0 2px rgba(46,125,50,0.2) !important;
    }
    
    /* Preview card */
    .preview-card {
        background: white;
        border: 2px solid #c8e6c9;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 16px rgba(0,30,0,0.08);
    }
    
    /* Skill tags */
    .skill-tag {
        display: inline-block;
        background: #e8f5e9;
        color: #1b5e20;
        padding: 4px 12px;
        border-radius: 20px;
        margin: 4px;
        border: 1px solid #a5d6a7;
        font-size: 0.9rem;
    }
    
    /* Print styles */
    @media print {
        .no-print {
            display: none !important;
        }
        .print-only {
            display: block !important;
        }
        body {
            background: white;
            padding: 0.3in;
        }
        .preview-card {
            box-shadow: none;
            border: none;
            padding: 0;
        }
        .stApp {
            background: white;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------- SESSION STATE INITIALIZATION ----------
    if "resume" not in st.session_state:
        st.session_state.resume = {
            "personal": {
                "full_name": "Alex Morgan",
                "title": "Frontend Developer",
                "email": "alex.morgan@example.com",
                "phone": "+1 (555) 123-4567",
                "location": "San Francisco, CA"
            },
            "summary": "Creative frontend developer with 5+ years of experience building responsive web applications. Passionate about clean design and user experience.",
            "experience": [
                {
                    "id": 1,
                    "company": "TechCorp",
                    "position": "Senior Frontend Developer",
                    "start_date": "2021",
                    "end_date": "Present",
                    "description": "Led development of a design system used across 10+ products."
                },
                {
                    "id": 2,
                    "company": "WebStudio",
                    "position": "Frontend Developer",
                    "start_date": "2018",
                    "end_date": "2021",
                    "description": "Built and maintained client websites using React and TypeScript."
                }
            ],
            "education": [
                {
                    "id": 1,
                    "institution": "University of Technology",
                    "degree": "B.Sc. in Computer Science",
                    "start_date": "2014",
                    "end_date": "2018"
                }
            ],
            "skills": ["React", "JavaScript", "TypeScript", "Tailwind CSS", "Node.js"]
        }

    # Helper to generate unique IDs
    def get_next_id(items):
        if not items:
            return 1
        return max(item.get("id", 0) for item in items) + 1

    # ---------- HEADER ----------
    col_title, col_btn = st.columns([3, 1])
    with col_title:
        st.markdown("<h1 style='color:#1b5e20;'>📄 Resume Builder</h1>", unsafe_allow_html=True)
    with col_btn:
        # Download button (triggers print)
        st.markdown("""
            <div style="display: flex; justify-content: flex-end; padding-top: 1.5rem;">
                <button onclick="window.print();" style="
                    background-color: #2e7d32;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 24px;
                    font-weight: 600;
                    font-size: 1rem;
                    cursor: pointer;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                ">
                    ⬇️ Download PDF
                </button>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ---------- MAIN LAYOUT: Editor (left) and Preview (right) ----------
    editor_col, preview_col = st.columns([1, 1], gap="large")

    with editor_col:
        st.markdown('<div class="no-print">', unsafe_allow_html=True)
        
        # --- Personal Details ---
        with st.container():
            st.subheader("👤 Personal Details")
            with st.form("personal_form", clear_on_submit=False):
                cols = st.columns(2)
                with cols[0]:
                    full_name = st.text_input("Full Name", value=st.session_state.resume["personal"]["full_name"], key="name_input")
                    email = st.text_input("Email", value=st.session_state.resume["personal"]["email"], key="email_input")
                    phone = st.text_input("Phone", value=st.session_state.resume["personal"]["phone"], key="phone_input")
                with cols[1]:
                    title = st.text_input("Professional Title", value=st.session_state.resume["personal"]["title"], key="title_input")
                    location = st.text_input("Location", value=st.session_state.resume["personal"]["location"], key="location_input")
                
                if st.form_submit_button("Update Personal Info"):
                    st.session_state.resume["personal"].update({
                        "full_name": full_name,
                        "title": title,
                        "email": email,
                        "phone": phone,
                        "location": location
                    })
                    st.success("Personal details updated!")
        
        # --- Professional Summary ---
        with st.container():
            st.subheader("📝 Professional Summary")
            summary = st.text_area("Summary", value=st.session_state.resume["summary"], height=100, key="summary_input")
            if st.button("Update Summary", key="update_summary"):
                st.session_state.resume["summary"] = summary
                st.success("Summary updated!")
        
        # --- Experience ---
        st.subheader("💼 Experience")
        for idx, exp in enumerate(st.session_state.resume["experience"]):
            with st.expander(f"{exp.get('position', 'New Position')} at {exp.get('company', 'Company')}", expanded=(idx == 0)):
                cols = st.columns(2)
                with cols[0]:
                    company = st.text_input("Company", value=exp.get("company", ""), key=f"exp_company_{exp['id']}")
                    position = st.text_input("Position", value=exp.get("position", ""), key=f"exp_position_{exp['id']}")
                with cols[1]:
                    start_date = st.text_input("Start Year", value=exp.get("start_date", ""), key=f"exp_start_{exp['id']}")
                    end_date = st.text_input("End Year", value=exp.get("end_date", ""), key=f"exp_end_{exp['id']}")
                description = st.text_area("Description", value=exp.get("description", ""), key=f"exp_desc_{exp['id']}")
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Update This Experience", key=f"update_exp_{exp['id']}"):
                        exp.update({
                            "company": company,
                            "position": position,
                            "start_date": start_date,
                            "end_date": end_date,
                            "description": description
                        })
                        st.success("Experience updated!")
                with col2:
                    if st.button("🗑️ Remove", key=f"remove_exp_{exp['id']}"):
                        st.session_state.resume["experience"] = [e for e in st.session_state.resume["experience"] if e["id"] != exp["id"]]
                        st.rerun()
        
        if st.button("➕ Add Experience", key="add_exp"):
            new_id = get_next_id(st.session_state.resume["experience"])
            st.session_state.resume["experience"].append({
                "id": new_id,
                "company": "",
                "position": "",
                "start_date": "",
                "end_date": "",
                "description": ""
            })
            st.rerun()
        
        # --- Education ---
        st.subheader("🎓 Education")
        for idx, edu in enumerate(st.session_state.resume["education"]):
            with st.expander(f"{edu.get('degree', 'Degree')} - {edu.get('institution', 'Institution')}", expanded=(idx == 0)):
                cols = st.columns(2)
                with cols[0]:
                    institution = st.text_input("Institution", value=edu.get("institution", ""), key=f"edu_inst_{edu['id']}")
                    degree = st.text_input("Degree", value=edu.get("degree", ""), key=f"edu_deg_{edu['id']}")
                with cols[1]:
                    start_date = st.text_input("Start Year", value=edu.get("start_date", ""), key=f"edu_start_{edu['id']}")
                    end_date = st.text_input("End Year", value=edu.get("end_date", ""), key=f"edu_end_{edu['id']}")
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Update This Education", key=f"update_edu_{edu['id']}"):
                        edu.update({
                            "institution": institution,
                            "degree": degree,
                            "start_date": start_date,
                            "end_date": end_date
                        })
                        st.success("Education updated!")
                with col2:
                    if st.button("🗑️ Remove", key=f"remove_edu_{edu['id']}"):
                        st.session_state.resume["education"] = [e for e in st.session_state.resume["education"] if e["id"] != edu["id"]]
                        st.rerun()
        
        if st.button("➕ Add Education", key="add_edu"):
            new_id = get_next_id(st.session_state.resume["education"])
            st.session_state.resume["education"].append({
                "id": new_id,
                "institution": "",
                "degree": "",
                "start_date": "",
                "end_date": ""
            })
            st.rerun()
        
        # --- Skills ---
        st.subheader("🛠️ Skills")
        skills_str = st.text_input("Skills (comma-separated)", value=", ".join(st.session_state.resume["skills"]), key="skills_input")
        if st.button("Update Skills", key="update_skills"):
            st.session_state.resume["skills"] = [s.strip() for s in skills_str.split(",") if s.strip()]
            st.success("Skills updated!")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------- PREVIEW SECTION ----------
    with preview_col:
        st.markdown('<div class="preview-card">', unsafe_allow_html=True)
        
        personal = st.session_state.resume["personal"]
        
        # Header
        st.markdown(f"""
            <div style="border-bottom: 3px solid #c8e6c9; padding-bottom: 1rem; margin-bottom: 1.5rem;">
                <h1 style="color: #1b5e20; margin-bottom: 0.2rem; font-size: 2.5rem;">{personal['full_name']}</h1>
                <p style="color: #2e7d32; font-size: 1.3rem; margin: 0.2rem 0;">{personal['title']}</p>
                <div style="display: flex; flex-wrap: wrap; gap: 1.5rem; color: #555; margin-top: 0.8rem;">
                    <span>📧 {personal['email']}</span>
                    <span>📞 {personal['phone']}</span>
                    <span>📍 {personal['location']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Summary
        if st.session_state.resume["summary"]:
            st.markdown("""
                <h3 style="color: #1b5e20; border-left: 5px solid #2e7d32; padding-left: 12px; margin-bottom: 0.8rem;">Professional Summary</h3>
            """, unsafe_allow_html=True)
            st.markdown(f"<p style='margin-bottom: 1.5rem;'>{st.session_state.resume['summary']}</p>", unsafe_allow_html=True)
        
        # Experience
        if st.session_state.resume["experience"]:
            st.markdown("""
                <h3 style="color: #1b5e20; border-left: 5px solid #2e7d32; padding-left: 12px; margin-bottom: 1rem;">Experience</h3>
            """, unsafe_allow_html=True)
            for exp in st.session_state.resume["experience"]:
                st.markdown(f"""
                    <div style="margin-bottom: 1.5rem;">
                        <div style="display: flex; justify-content: space-between; align-items: baseline;">
                            <h4 style="margin: 0; color: #1b5e20;">{exp['position']}</h4>
                            <span style="color: #666; font-style: italic;">{exp['start_date']} – {exp['end_date']}</span>
                        </div>
                        <p style="font-weight: 600; margin: 0.2rem 0; color: #2e7d32;">{exp['company']}</p>
                        <p style="margin-top: 0.3rem;">{exp['description']}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        # Education
        if st.session_state.resume["education"]:
            st.markdown("""
                <h3 style="color: #1b5e20; border-left: 5px solid #2e7d32; padding-left: 12px; margin: 1.5rem 0 1rem 0;">Education</h3>
            """, unsafe_allow_html=True)
            for edu in st.session_state.resume["education"]:
                st.markdown(f"""
                    <div style="margin-bottom: 1rem;">
                        <div style="display: flex; justify-content: space-between;">
                            <h4 style="margin: 0; color: #1b5e20;">{edu['degree']}</h4>
                            <span style="color: #666;">{edu['start_date']} – {edu['end_date']}</span>
                        </div>
                        <p style="color: #2e7d32; margin: 0.2rem 0;">{edu['institution']}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        # Skills
        if st.session_state.resume["skills"]:
            st.markdown("""
                <h3 style="color: #1b5e20; border-left: 5px solid #2e7d32; padding-left: 12px; margin: 1.5rem 0 1rem 0;">Skills</h3>
            """, unsafe_allow_html=True)
            skills_html = " ".join([f'<span class="skill-tag">{skill}</span>' for skill in st.session_state.resume["skills"]])
            st.markdown(f"<div>{skills_html}</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------- FOOTER (print hint) ----------
    st.markdown("---")
    st.caption("💡 Click **Download PDF** then choose 'Save as PDF' in the print dialog. Only the resume preview will be printed.")

# Main execution for standalone mode
if __name__ == "__main__":
    render_resume_page()
