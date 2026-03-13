"""Streamlit Dashboard - Exact Match to Reference."""

import streamlit as st
import json
import sqlite3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "phase2"))
sys.path.insert(0, str(Path(__file__).parent / "phase3"))

st.set_page_config(page_title="InsightReviewer", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 2rem !important; max-width: 1200px !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_report():
    path = Path(__file__).parent / "phase3" / "outputs" / "weekly_pulse.json"
    if path.exists():
        with open(path, 'r') as f:
            return json.load(f)
    return None

report = load_report()
if not report:
    st.error("No data found")
    st.stop()

# Header
st.markdown("<h1 style='font-size:1.5rem; font-weight:700; color:#0f172a; margin:0;'>Weekly Product Insight Summary</h1>", unsafe_allow_html=True)

# Main content - two columns (2:1 ratio)
left_col, right_col = st.columns([2, 1])

with left_col:
    # Top 3 Themes Card
    themes = report.get('themes', [])[:3]
    cats = ['HIGH IMPACT', 'USABILITY', 'ONBOARDING']
    
    themes_html = "<div style='background:white; border-radius:12px; border:1px solid #e2e8f0; padding:1.5rem; margin-bottom:1.5rem;'>"
    themes_html += "<div style='display:flex; align-items:center; gap:0.5rem; font-weight:600; color:#6366f1; margin-bottom:1.5rem;'><span style='font-size:1.1rem;'>🔥</span> Top 3 Themes</div>"
    themes_html += "<div style='display:grid; grid-template-columns: repeat(3, 1fr); gap:1rem;'>"
    
    for i, theme in enumerate(themes):
        themes_html += "<div>"
        themes_html += f"<div style='font-size:0.65rem; font-weight:700; text-transform:uppercase; color:#64748b; margin-bottom:0.5rem;'>{cats[i]}</div>"
        themes_html += f"<div style='font-weight:600; color:#0f172a; margin-bottom:0.5rem; font-size:0.95rem;'>{theme['name']}</div>"
        themes_html += f"<div style='font-size:0.8rem; color:#64748b; line-height:1.5;'>{theme['description']}</div>"
        themes_html += "</div>"
    
    themes_html += "</div></div>"
    st.markdown(themes_html, unsafe_allow_html=True)
    
    # Representative User Quotes Card
    quotes = report.get('quotes', [])[:3]
    
    st.markdown("""
    <div style='background:white; border-radius:12px; border:1px solid #e2e8f0; padding:1.5rem; margin-bottom:1.5rem;'>
        <div style='display:flex; align-items:center; gap:0.5rem; font-weight:600; color:#6366f1; margin-bottom:1.5rem;'>
            <span style='font-size:1.1rem;'>💬</span> Representative User Quotes
        </div>
    """, unsafe_allow_html=True)
    
    for i, quote in enumerate(quotes):
        border = "1px solid #f1f5f9" if i < 2 else "none"
        st.markdown(f"""
        <div style="padding:1rem 0; border-bottom:{border};">
            <div style="color:#374151; font-size:0.9rem; line-height:1.6; margin-bottom:0.5rem;">"{quote['text']}"</div>
            <div style="font-size:0.75rem; color:#9ca3af;">— Verified User, {quote.get('rating', 1)} Star Review</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Suggested Action Ideas Card
    actions = report.get('actions', [])[:3]
    
    st.markdown("""
    <div style='background:white; border-radius:12px; border:1px solid #e2e8f0; padding:1.5rem; margin-bottom:1.5rem;'>
        <div style='display:flex; align-items:center; gap:0.5rem; font-weight:600; color:#6366f1; margin-bottom:1.5rem;'>
            <span style='font-size:1.1rem;'>💡</span> Suggested Action Ideas
        </div>
    """, unsafe_allow_html=True)
    
    for i, action in enumerate(actions):
        border = "1px solid #f1f5f9" if i < 2 else "none"
        st.markdown(f"""
        <div style="display:flex; gap:1rem; padding:1rem 0; border-bottom:{border};">
            <div style="width:28px; height:28px; background:#eff6ff; color:#4f46e5; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:600; font-size:0.85rem; flex-shrink:0;">{i+1}</div>
            <div style="flex:1;">
                <div style="font-weight:600; color:#0f172a; font-size:0.9rem; margin-bottom:0.25rem;">{action['title']}</div>
                <div style="font-size:0.8rem; color:#64748b; line-height:1.5;">{action['description']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    # Send Report Card
    st.markdown("<div style='background:white; border-radius:12px; border:1px solid #e2e8f0; padding:1.5rem;'>" +
               "<div style='display:flex; align-items:center; gap:0.5rem; font-weight:600; color:#6366f1; margin-bottom:1.5rem;'>" +
               "<span>📧</span> Send Report</div>", unsafe_allow_html=True)
    
    with st.form("email"):
        to_email = st.text_input("Recipient Email", placeholder="product-team@company.com", key="email_to")
        subject = st.text_input("Subject", value="Weekly Insight Summary - Negative Reviews", key="email_subject")
        
        # Generate key themes list from actual LLM data
        themes_list = "".join([f"<li>{t['name']} ({t.get('impact', 'High Impact')})</li>" for t in themes])
        total_reviews = report.get('total_reviews_analyzed', 667)
        
        st.markdown(f"""
        <div style="background:#f8fafc; border-radius:8px; padding:1rem; margin:1rem 0; font-size:0.8rem; color:#64748b;">
            <div style="font-weight:600; color:#0f172a; margin-bottom:0.75rem;">Preview Summary</div>
            <div><strong>SUMMARY OVERVIEW</strong><br>
            This week, we analyzed {total_reviews} negative reviews. The most critical themes relate to stability and performance.<br><br>
            <strong>KEY THEMES:</strong>
            <ul style="margin:0.5rem 0; padding-left:1rem;">
                {themes_list}
            </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        submitted = st.form_submit_button("📧 Send Email", use_container_width=True, type="primary")
        
        # Custom CSS to make button purple
        st.markdown("""
        <style>
            .stButton > button[kind="primary"] {
                background-color: #6366f1 !important;
                color: white !important;
                border: none !important;
                font-weight: 500 !important;
            }
            .stButton > button[kind="primary"]:hover {
                background-color: #4f46e5 !important;
                color: white !important;
            }
        </style>
        """, unsafe_allow_html=True)
        if submitted:
            try:
                # Import email functions
                sys.path.insert(0, str(Path(__file__).parent / "backend"))
                from app.core.config import get_settings
                from app.api.email import send_email_via_smtp, generate_email_content
                
                settings = get_settings()
                email_body = generate_email_content(report)
                
                # Use form values
                to_email_value = to_email if to_email else 'product-team@company.com'
                subject_value = subject if subject else 'Weekly Insight Summary'
                
                send_email_via_smtp(
                    to_email=to_email_value,
                    subject=subject_value,
                    html_body=email_body,
                    settings=settings
                )
                st.success("✅ Email sent successfully!")
            except Exception as e:
                st.error(f"❌ Failed to send email: {str(e)}")
    
    st.markdown("<div style='font-size:0.7rem; color:#9ca3af; text-align:center; margin-top:1rem;'>This report will be sent as a PDF attachment with a formatted HTML body.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="margin-top:2rem; padding:1.5rem 0; border-top:1px solid #e2e8f0; display:flex; justify-content:space-between; color:#9ca3af; font-size:0.75rem;">
    <div>© 2024 InsightReviewer. All rights reserved.</div>
    <div style="display:flex; gap:1.5rem;">
        <span>Privacy Policy</span>
        <span>Terms of Service</span>
        <span>Support</span>
    </div>
</div>
""", unsafe_allow_html=True)
