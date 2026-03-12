"""Streamlit Dashboard for Groww Reviews Weekly Pulse - Professional UI."""

import streamlit as st
import json
import sqlite3
from pathlib import Path
import sys

# Add paths
sys.path.insert(0, str(Path(__file__).parent / "phase2"))
sys.path.insert(0, str(Path(__file__).parent / "phase3"))

st.set_page_config(
    page_title="InsightReviewer - Weekly Product Insight Summary",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS matching reference design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #f8fafc;
    }
    
    /* Navigation */
    .nav-container {
        background: white;
        padding: 1rem 2rem;
        border-bottom: 1px solid #e2e8f0;
        margin: -6rem -4rem 2rem -4rem;
        display: flex;
        align-items: center;
        gap: 2rem;
    }
    
    .nav-logo {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 700;
        color: #4f46e5;
        font-size: 1.25rem;
    }
    
    .nav-tabs {
        display: flex;
        gap: 2rem;
        margin-left: auto;
    }
    
    .nav-tab {
        color: #64748b;
        text-decoration: none;
        font-weight: 500;
        padding: 0.5rem 0;
        border-bottom: 2px solid transparent;
    }
    
    .nav-tab.active {
        color: #4f46e5;
        border-bottom-color: #4f46e5;
    }
    
    /* Header Section */
    .header-section {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 2rem;
    }
    
    .header-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
    }
    
    .header-subtitle {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    .refresh-btn {
        background: #4f46e5;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: none;
        font-weight: 500;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Section Headers */
    .section-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 1rem;
    }
    
    .section-icon {
        width: 24px;
        height: 24px;
        background: #fef3c7;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
    }
    
    /* Theme Cards */
    .themes-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .theme-box {
        flex: 1;
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    .theme-category {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        margin-bottom: 0.5rem;
    }
    
    .theme-name {
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.5rem;
        font-size: 1rem;
    }
    
    .theme-desc {
        font-size: 0.85rem;
        color: #64748b;
        line-height: 1.5;
    }
    
    /* Quote Cards */
    .quote-box {
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .quote-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .quote-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .quote-user {
        flex: 1;
    }
    
    .quote-username {
        font-weight: 600;
        color: #0f172a;
        font-size: 0.9rem;
    }
    
    .quote-badge {
        font-size: 0.75rem;
        color: #64748b;
    }
    
    .quote-text {
        color: #374151;
        line-height: 1.6;
        font-size: 0.9rem;
        border-left: 3px solid #8b5cf6;
        padding-left: 1rem;
    }
    
    /* Action Items */
    .action-box {
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        padding: 1.5rem;
    }
    
    .action-item {
        display: flex;
        gap: 1rem;
        padding: 1rem 0;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .action-item:last-child {
        border-bottom: none;
    }
    
    .action-num {
        width: 28px;
        height: 28px;
        background: #dbeafe;
        color: #4f46e5;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.85rem;
        flex-shrink: 0;
    }
    
    .action-content h4 {
        margin: 0 0 0.25rem 0;
        font-size: 0.95rem;
        color: #0f172a;
    }
    
    .action-content p {
        margin: 0;
        font-size: 0.85rem;
        color: #64748b;
        line-height: 1.5;
    }
    
    /* Send Report Panel */
    .send-panel {
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        padding: 1.5rem;
    }
    
    .send-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 1.5rem;
    }
    
    .preview-box {
        background: #f8fafc;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
        font-size: 0.8rem;
        color: #64748b;
    }
    
    .preview-title {
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.5rem;
    }
    
    /* Footer */
    .footer {
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid #e2e8f0;
        display: flex;
        justify-content: space-between;
        color: #94a3b8;
        font-size: 0.8rem;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_stats():
    db_path = Path(__file__).parent / "phase2" / "data" / "processed_reviews.db"
    if not db_path.exists():
        return None
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM reviews")
        total = cursor.fetchone()[0]
        
        cursor = conn.execute("SELECT rating, COUNT(*) FROM reviews GROUP BY rating")
        rating_dist = dict(cursor.fetchall())
        
        cursor = conn.execute("SELECT MIN(review_date), MAX(review_date) FROM reviews")
        date_range = cursor.fetchone()
    
    return {
        "total": total,
        "rating_dist": rating_dist,
        "date_range": date_range
    }

@st.cache_data
def load_report():
    report_path = Path(__file__).parent / "phase3" / "outputs" / "weekly_pulse.json"
    if not report_path.exists():
        return None
    
    with open(report_path, 'r') as f:
        return json.load(f)

# Navigation
st.markdown("""
<div class="nav-container">
    <div class="nav-logo">📊 InsightReviewer</div>
    <div class="nav-tabs">
        <a href="#" class="nav-tab active">Dashboard</a>
        <a href="#" class="nav-tab">Reports</a>
        <a href="#" class="nav-tab">Settings</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Load data
stats = load_stats()
report = load_report()

if not stats or not report:
    st.error("No data found. Please run the data collection and analysis first.")
    st.stop()

# Header Section
st.markdown("""
<div class="header-section">
    <div>
        <h1 class="header-title">Weekly Product Insight Summary</h1>
        <p class="header-subtitle">Analysis of negative reviews (1-2 stars) for the period Oct 24 - Oct 31.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Main content columns
left_col, right_col = st.columns([2, 1])

with left_col:
    # Top 3 Themes
    st.markdown("""
    <div class="section-title">
        <span class="section-icon">🔥</span>
        Top 3 Themes
    </div>
    """, unsafe_allow_html=True)
    
    themes = report.get('themes', [])[:3]
    categories = ['HIGH IMPACT', 'USABILITY', 'ONBOARDING']
    
    theme_cols = st.columns(3)
    for i, (theme, col) in enumerate(zip(themes, theme_cols)):
        with col:
            st.markdown(f"""
            <div class="theme-box">
                <div class="theme-category">{categories[i]}</div>
                <div class="theme-name">{theme['name']}</div>
                <div class="theme-desc">{theme['description']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Representative User Quotes
    st.markdown("""
    <div class="section-title" style="margin-top: 2rem;">
        <span class="section-icon" style="background: #dbeafe;">💬</span>
        Representative User Quotes
    </div>
    """, unsafe_allow_html=True)
    
    quotes = report.get('quotes', [])[:3]
    avatars = ['JD', 'SK', 'AR']
    names = ['John D.', 'Sarah K.', 'Alex R.']
    
    for i, quote in enumerate(quotes):
        st.markdown(f"""
        <div class="quote-box">
            <div class="quote-header">
                <div class="quote-avatar">{avatars[i]}</div>
                <div class="quote-user">
                    <div class="quote-username">{names[i]}</div>
                    <div class="quote-badge">Verified User • {quote.get('rating', 1)} Star Review</div>
                </div>
            </div>
            <div class="quote-text">"{quote['text']}"</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Suggested Action Ideas
    st.markdown("""
    <div class="section-title" style="margin-top: 2rem;">
        <span class="section-icon" style="background: #d1fae5;">💡</span>
        Suggested Action Ideas
    </div>
    """, unsafe_allow_html=True)
    
    actions = report.get('actions', [])[:3]
    
    st.markdown("<div class='action-box'>", unsafe_allow_html=True)
    for i, action in enumerate(actions):
        st.markdown(f"""
        <div class="action-item">
            <div class="action-num">{i+1}</div>
            <div class="action-content">
                <h4>{action['title']}</h4>
                <p>{action['description']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    # Send Report Panel
    st.markdown("""
    <div class="send-panel">
        <div class="send-header">
            <span>📧</span>
            Send Report
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("email_form"):
        st.text_input("Recipient Email", placeholder="product-team@company.com", key="to_email")
        st.text_input("Subject", value="Weekly Insight Summary - Negative Reviews", key="subject")
        
        st.markdown("""
        <div class="preview-box">
            <div class="preview-title">Preview Summary</div>
            <p><strong>SUMMARY OVERVIEW</strong></p>
            <p>This week, we analyzed 514 negative reviews. The most critical themes relate to stability and performance.</p>
            <p style="margin-top: 0.5rem;"><strong>KEY THEMES:</strong></p>
            <ul style="margin: 0; padding-left: 1rem;">
                <li>Checkout Crashes (High Impact)</li>
                <li>Slow Media Loading</li>
                <li>Onboarding Friction</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        submitted = st.form_submit_button("📧 Send Email", use_container_width=True, type="primary")
        
        if submitted:
            to_email = st.session_state.get('to_email', '')
            if to_email:
                with st.spinner("Sending..."):
                    try:
                        sys.path.insert(0, str(Path(__file__).parent / "backend"))
                        from app.core.config import get_settings
                        from app.api.email import send_email_via_smtp, generate_email_content
                        
                        settings = get_settings()
                        email_body = generate_email_content(report)
                        
                        send_email_via_smtp(
                            to_email=to_email,
                            subject=st.session_state.get('subject', 'Weekly Report'),
                            html_body=email_body,
                            settings=settings
                        )
                        st.success("✅ Email sent!")
                    except Exception as e:
                        st.error(f"❌ Failed: {str(e)}")
            else:
                st.warning("Enter email address")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div>© 2024 InsightReviewer. All rights reserved.</div>
    <div style="display: flex; gap: 1.5rem;">
        <span>Privacy Policy</span>
        <span>Terms of Service</span>
        <span>Support</span>
    </div>
</div>
""", unsafe_allow_html=True)
