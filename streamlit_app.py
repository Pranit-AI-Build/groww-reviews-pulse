"""Streamlit Dashboard - Improved Professional UI."""

import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="InsightReviewer", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 2.5rem !important; max-width: 1400px !important; }
    
    /* Card hover effect */
    .css-1r6slb0 {
        transition: all 0.3s ease;
    }
    .css-1r6slb0:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }
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

# Header Section
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown("<h1 style='font-size:1.75rem; font-weight:700; color:#0f172a; margin:0;'>Weekly Product Insight Summary</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; font-size:0.95rem; margin:0.5rem 0 0 0;'>AI-powered analysis of user feedback</p>", unsafe_allow_html=True)

with header_col2:
    if st.button("↻ Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Main content - two columns (2:1 ratio)
left_col, right_col = st.columns([2, 1], gap="large")

with left_col:
    # Top 3 Themes Card
    themes = report.get('themes', [])[:3]
    cats = ['HIGH IMPACT', 'USABILITY', 'ONBOARDING']
    
    st.markdown("""
    <div style='background:white; border-radius:12px; border:1px solid #e2e8f0; padding:1.5rem; margin-bottom:1.5rem; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>
        <div style='display:flex; align-items:center; gap:0.5rem; font-weight:600; color:#6366f1; margin-bottom:1.25rem;'>
            <span style='font-size:1.25rem;'>🔥</span>
            <span style='font-size:1.125rem;'>Top 3 Themes</span>
        </div>
        <div style='display:grid; grid-template-columns: repeat(3, 1fr); gap:1.25rem;'>
    """, unsafe_allow_html=True)
    
    for i, theme in enumerate(themes):
        st.markdown(f"""
        <div style='background:{['#fef2f2', '#fffbeb', '#eff6ff'][i]}; border:1px solid {['#fecaca', '#fcd34d', '#bfdbfe'][i]}; border-radius:10px; padding:1.25rem;'>
            <div style='font-size:0.65rem; font-weight:700; text-transform:uppercase; color:#64748b; margin-bottom:0.5rem; letter-spacing:0.5px;'>{cats[i]}</div>
            <div style='font-weight:600; color:#0f172a; margin-bottom:0.5rem; font-size:0.95rem; line-height:1.4;'>{theme['name']}</div>
            <div style='font-size:0.8rem; color:#64748b; line-height:1.5;'>{theme['description'][:80]}...</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("        </div></div>", unsafe_allow_html=True)
    
    # Representative User Quotes Card
    quotes = report.get('quotes', [])[:3]
    
    st.markdown("""
    <div style='background:white; border-radius:12px; border:1px solid #e2e8f0; padding:1.5rem; margin-bottom:1.5rem; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>
        <div style='display:flex; align-items:center; gap:0.5rem; font-weight:600; color:#6366f1; margin-bottom:1.25rem;'>
            <span style='font-size:1.25rem;'>💬</span>
            <span style='font-size:1.125rem;'>Representative User Quotes</span>
        </div>
        <div style='background:#f9fafb; border-radius:10px; padding:1.25rem; border:1px solid #e5e7eb;'>
    """, unsafe_allow_html=True)
    
    for i, quote in enumerate(quotes):
        is_last = i == len(quotes) - 1
        st.markdown(f"""
        <div style="padding-bottom:{'1rem' if not is_last else '0'}; margin-bottom:{'1rem' if not is_last else '0'}; border-bottom:{'1px solid #e5e7eb' if not is_last else 'none'};">
            <div style="color:#374151; font-size:0.9rem; line-height:1.6; margin-bottom:0.5rem; font-style:italic;">\"{quote['text']}\"</div>
            <div style="font-size:0.75rem; color:#9ca3af;">— Verified User, {quote.get('rating', 1)} Star Review</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("        </div></div>", unsafe_allow_html=True)
    
    # Suggested Action Ideas Card
    actions = report.get('actions', [])[:3]
    
    st.markdown("""
    <div style='background:white; border-radius:12px; border:1px solid #e2e8f0; padding:1.5rem; margin-bottom:1.5rem; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>
        <div style='display:flex; align-items:center; gap:0.5rem; font-weight:600; color:#6366f1; margin-bottom:1.25rem;'>
            <span style='font-size:1.25rem;'>💡</span>
            <span style='font-size:1.125rem;'>Suggested Action Ideas</span>
        </div>
        <div>
    """, unsafe_allow_html=True)
    
    for i, action in enumerate(actions):
        is_last = i == len(actions) - 1
        st.markdown(f"""
        <div style="display:flex; gap:1rem; padding:{'1.25rem' if not is_last else '0'}; margin-bottom:{'1rem' if not is_last else '0'}; border-bottom:{'1px solid #f1f5f9' if not is_last else 'none'};">
            <div style="width:32px; height:32px; background:linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); color:white; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:600; font-size:0.9rem; flex-shrink:0; box-shadow:0 2px 4px rgba(99,102,241,0.3);">{i+1}</div>
            <div style="flex:1;">
                <div style="font-weight:600; color:#0f172a; font-size:0.95rem; margin-bottom:0.35rem;">{action['title']}</div>
                <div style="font-size:0.825rem; color:#64748b; line-height:1.5;">{action['description']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("        </div></div>", unsafe_allow_html=True)

with right_col:
    # Send Report Card - Sticky positioning
    st.markdown("""
    <div style='background:white; border-radius:12px; border:1px solid #e2e8f0; padding:1.5rem; box-shadow:0 1px 3px rgba(0,0,0,0.05); position:sticky; top:2rem;'>
        <div style='display:flex; align-items:center; gap:0.5rem; font-weight:600; color:#6366f1; margin-bottom:1.25rem;'>
            <span style='font-size:1.25rem;'>📧</span>
            <span style='font-size:1.125rem;'>Send Report</span>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("email"):
        to_email = st.text_input("Recipient Email", placeholder="product-team@company.com", key="email_to")
        subject = st.text_input("Subject", value="Weekly Insight Summary - Negative Reviews", key="email_subject")
        
        # Generate key themes list from actual LLM data
        themes_list = "".join([f"<li>{t['name']} ({t.get('impact', 'High Impact')})</li>" for t in themes])
        total_reviews = report.get('total_reviews_analyzed', 667)
        
        st.markdown(f"""
        <div style="background:linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius:10px; padding:1.25rem; margin:1.25rem 0; font-size:0.825rem; color:#64748b; border:1px solid #e2e8f0;">
            <div style="font-weight:600; color:#0f172a; margin-bottom:0.75rem; font-size:0.875rem;">📊 Preview Summary</div>
            <div style="line-height:1.6;">
                <strong style="color:#0f172a;">SUMMARY OVERVIEW</strong><br>
                This week, we analyzed <strong style="color:#6366f1;">{total_reviews}</strong> negative reviews. The most critical themes relate to stability and performance.<br><br>
                <strong style="color:#0f172a;">KEY THEMES:</strong>
                <ul style="margin:0.5rem 0; padding-left:1.25rem; line-height:1.8;">
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
                background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
                color: white !important;
                border: none !important;
                font-weight: 600 !important;
                padding: 0.625rem 1.25rem !important;
                border-radius: 8px !important;
                box-shadow: 0 2px 4px rgba(99,102,241,0.3) !important;
                transition: all 0.2s ease !important;
            }
            .stButton > button[kind="primary"]:hover {
                background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important;
                box-shadow: 0 4px 8px rgba(99,102,241,0.4) !important;
                transform: translateY(-1px) !important;
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
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.75rem; color:#94a3b8; text-align:center; margin-top:1rem; line-height:1.5;'>📎 Report will be sent as PDF attachment with formatted HTML body</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="margin-top:3rem; padding:2rem 0; border-top:1px solid #e2e8f0; display:flex; justify-content:space-between; align-items:center; color:#94a3b8; font-size:0.8rem;">
    <div>© 2024 InsightReviewer. All rights reserved.</div>
    <div style="display:flex; gap:2rem;">
        <span style="cursor:pointer; transition:color 0.2s;">Privacy Policy</span>
        <span style="cursor:pointer; transition:color 0.2s;">Terms of Service</span>
        <span style="cursor:pointer; transition:color 0.2s;">Support</span>
    </div>
</div>
""", unsafe_allow_html=True)
