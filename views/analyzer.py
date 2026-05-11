import streamlit as st
import time
import json
import logging
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result, _rule_based_analysis
from config import *

def render_analyzer():
    uid = st.session_state.user_id
    # st.markdown(f"<h2 style='font-family: sans-serif;color:#f1f5f9;font-size:1.6rem;font-weight:800;margin:0 0 12px'>{bi('search','1.2rem')} Job Post Analyzer</h2>", unsafe_allow_html=True)

    tab_url, tab_text, tab_bulk = st.tabs(["Paste URL", "Paste Text", "Bulk Analyze"])

    # ── URL tab ──
    with tab_url:
        st.markdown(f"""
        <div class="table-card" style="border-left: 5px solid #337AB7;">
          <div style="padding:15px; display:flex; align-items:center; gap:12px;">
            <div style="font-size:1.5rem; color:#337AB7; line-height:1;">{bi('info-circle-fill')}</div>
            <div style="color:#73879C; font-size:14px; font-weight:500;">Paste any job listing URL from LinkedIn, Indeed, Naukri, Internshala, etc. to analyze its legitimacy.</div>
          </div>
        </div>""", unsafe_allow_html=True)

        job_url = st.text_input("Job URL", placeholder="https://www.linkedin.com/jobs/view/...", key="ana_url")
        c1,c2 = st.columns([3,1])
        with c2:
            analyze = st.button("Sniff It!", use_container_width=True, key="ana_btn")
        with c1:
            note_for_save = st.text_input("Personal note (optional)", placeholder="e.g. looks interesting, follow up Monday", key="ana_note")

        if analyze:
            if not job_url.strip():
                st.error("Please enter a URL.")
            else:
                try:
                    with st.spinner("Sniffing the job posting..."):
                        logging.info(f"Starting URL analysis for: {job_url}")
                        result = simulate_analysis(job_url)
                        
                        # Check for analysis errors
                        if result.get("status") == "Error":
                            st.error(f"Analysis Failed: {result.get('details', 'Unknown error')}")
                            if result.get("error"):
                                st.caption(f"Technical details: {result['error']}")
                            return
                        
                        # Show debug info in development
                        if st.checkbox("Show Debug Info", key="show_debug"):
                            st.json({
                                "URL Received": result.get("url_received"),
                                "Scraping Success": result.get("scraping_success"),
                                "Content Length": result.get("content_length", 0),
                                "Title Extracted": result.get("title"),
                                "Company Extracted": result.get("company")
                            })
                    
                    db.add_job_analysis(uid, job_url, result["title"], result["company"],
                                        result["status"], result["confidence"], result["details"], note_for_save)
                    db.add_notification(f"Analysis complete: {result['title']} → {result['status']}")

                    _show_result(result, job_url)
                    
                except Exception as e:
                    logging.error(f"Error in URL analysis: {str(e)}")
                    st.error(f"Analysis failed: {str(e)}")
                    st.caption("Please check the URL and try again, or contact support if the issue persists.")
                    return

        if not job_url:
            st.markdown(f"""
            <div style="text-align:center;padding:50px 20px; border: 2px dashed #D9DEE4; border-radius:8px; background:#f9f9f9; margin-top:20px;">
              <div style="font-size:5rem;margin-bottom:16px; line-height:1;">{bi('search-heart-fill','5rem','#D9DEE4')}</div>
              <div style="color:#73879C;font-size:1.2rem;font-weight:600">Ready to Analyze</div>
              <div style="color:#999;font-size:14px;margin-top:6px">Paste a job URL above and click "Sniff It!" to start the verification process.</div>
            </div>""", unsafe_allow_html=True)

 # ── Paste text tab ──
    with tab_text:
        col_t, col_c = st.columns(2)
        with col_t:
            manual_title = st.text_input("Job Title", placeholder="e.g. Data Analyst", key="ana_manual_title")
        with col_c:
            manual_company = st.text_input("Company Name", placeholder="e.g. Valeo Health", key="ana_manual_company")
        jd_text = st.text_area("Paste the full job description here", height=200,
                               placeholder="Copy and paste the complete job listing text…", key="ana_text")
        if st.button("Analyze Text", key="ana_text_btn"):
            if not jd_text.strip():
                st.error("Please paste some text.")
            else:
                try:
                    with st.spinner("Analyzing…"):
                        logging.info(f"Starting manual text analysis for {len(jd_text)} characters")
                        
                        # For manual text entry, create a mock URL object for the analysis
                        mock_url = f"manual_text_entry_{len(jd_text)}"
                        result = simulate_analysis(mock_url)
                        
                        # Override with manual entries and use the text directly
                        result["title"] = manual_title or "Manual Entry"
                        result["company"] = manual_company or "User Provided"
                        
                        # Use rule-based analysis on the actual text
                        rule_result = _rule_based_analysis(jd_text, "manual_entry")
                        result["status"] = rule_result["status"]
                        result["confidence"] = rule_result["confidence"]
                        result["risk_score"] = rule_result["risk_score"]
                        result["details"] = "Analysis based on manually provided job description text."
                        result["red_flags"] = rule_result["red_flags"]
                        result["pos_signals"] = rule_result["pos_signals"]
                        
                        if manual_title:
                            result["title"] = manual_title
                        if manual_company:
                            result["company"] = manual_company
                        
                        logging.info(f"Manual text analysis completed: {result['status']} with {result['confidence']:.1%} confidence")
                        
                except Exception as e:
                    logging.error(f"Error in manual text analysis: {str(e)}")
                    st.error(f"Analysis failed: {str(e)}")
                    st.caption("Please try again or contact support if the issue persists.")
                    return
                        
                db.add_job_analysis(uid, "(text entry)", result["title"], result["company"],
                                    result["status"], result["confidence"], result["details"])
                _show_result(result, "(text entry)")

    # ── Bulk tab ──
    with tab_bulk:
        st.markdown("##### Paste up to 5 job URLs, one per line")
        bulk_input = st.text_area("URLs (one per line)", height=140, key="ana_bulk",
                                  placeholder="https://linkedin.com/...\nhttps://naukri.com/...\n…")
        if st.button("Sniff All", key="ana_bulk_btn"):
            urls = [u.strip() for u in bulk_input.strip().split("\n") if u.strip()][:5]
            if not urls:
                st.error("Enter at least one URL.")
            else:
                try:
                    prog = st.progress(0, text="Analyzing…")
                    successful_analyses = 0
                    failed_analyses = 0
                    
                    for i, url in enumerate(urls):
                        try:
                            time.sleep(1.0)  # Increased delay for bulk processing
                            logging.info(f"Processing bulk URL {i+1}/{len(urls)}: {url}")
                            
                            result = simulate_analysis(url)
                            
                            # Check for analysis errors
                            if result.get("status") == "Error":
                                st.error(f"Failed to analyze {url[:50]}...: {result.get('details', 'Unknown error')}")
                                failed_analyses += 1
                            else:
                                db.add_job_analysis(uid, url, result["title"], result["company"],
                                                    result["status"], result["confidence"], result["details"])
                                _show_result(result, url, compact=True)
                                successful_analyses += 1
                            
                            prog.progress((i+1)/len(urls), text=f"Analyzed {i+1}/{len(urls)}")
                            
                        except Exception as e:
                            logging.error(f"Error analyzing URL {url}: {str(e)}")
                            st.error(f"Error with {url[:50]}...: {str(e)}")
                            failed_analyses += 1
                            prog.progress((i+1)/len(urls), text=f"Analyzed {i+1}/{len(urls)}")
                    
                    if successful_analyses > 0:
                        st.success(f"Successfully analyzed {successful_analyses} job(s). See full details in Sniff History.")
                    if failed_analyses > 0:
                        st.warning(f"Failed to analyze {failed_analyses} job(s). Check the logs for details.")
                        
                except Exception as e:
                    logging.error(f"Bulk analysis failed: {str(e)}")
                    st.error(f"Bulk analysis failed: {str(e)}")
                    st.caption("Please try again with fewer URLs or contact support if the issue persists.")


