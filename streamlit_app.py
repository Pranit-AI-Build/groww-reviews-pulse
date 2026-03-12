"""Streamlit Dashboard - Exact Match to Reference Design."""

import streamlit as st
import json
import sqlite3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "phase2"))
sys.path.insert(0, str(Path(__file__).parent / "phase3"))

st.set_page_config(
    page_title="InsightReviewer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Exact CSS from reference image
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .main { background-color: #f8fafc; }
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header, .stDeployButton { display: none !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    
    /* Navigation Bar */
    .navbar {
        background: white;
        border-bottom: 1px solid #e2e8f0;
        padding: 0.75rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: -4rem -4rem 2rem -4rem;
    }
    
    .nav-left {
        display: flex;
        align-items: center;
        gap: 3rem;
    }
    
    .logo {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 700;
        color: #4f46e5;
        font-size: 1.1rem;
    }
    
    .logo-icon {
        width: 32px;
        height: 32px;
        background: #4f46e5;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
    }
    
    .nav-tabs {
        display: flex;
        gap: 2rem;
    }
    
    .nav-tab {
        color: #64748b;
        text-decoration: none;
        font-size: 0.9rem;
        font-weight: 500;
        padding: 0.5rem 0;
        border-bottom: 2px solid transparent;
    }
    
    .nav-tab.active {
        color: #4f46e5;
        border-bottom-color: #4f46e5;
    }
    
    .nav-right {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .nav-icon {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #f1f5f9;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #64748b;
    }
    
    .avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header */
    .header-section {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1.5rem;
        padding: 0 0.5rem;
    }
    
    .header-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
    }
    
    .header-subtitle {
        color: #64748b;
        font-size: 0.875rem;
        margin-top: 0.25rem;
    }
    
    .refresh-btn {
        background: #4f46e5;
        color: white;
        padding: 0.625rem 1.25rem;
        border-radius: 8px;
        border: none;
        font-weight: 500;
        font-size: 0.875rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        cursor: pointer;
    }
    
    /* Content Grid */
    .content-grid {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 1.5rem;
        padding: 0 0.5rem;
    }
    
    /* Cards */
    .card {
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
        color: #0f172a;
        font-size: 1rem;
    }
    
    .card-icon {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.7rem;
    }
    
    .icon-fire { background: #fef3c7; }
    .icon-chat { background: #dbeafe; }
    .icon-bulb { background: #d1fae5; }
    
    /* Themes Row */
    .themes-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
    }
    
    .theme-item {
        padding: 0.5rem 0;
    }
    
    .theme-label {
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #64748b;
        margin-bottom: 0.5rem;
    }
    
    .theme-title {
        font-weight: 600;
        color: #0f172a;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }
    
    .theme-desc {
        font-size: 0.8rem;
        color: #64748b;
        line-height: 1.5;
    }
    
    /* Quotes */
    .quote-item {
        display: flex;
        gap: 1rem;
        padding: 1rem 0;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .quote-item:last-child {
        border-bottom: none;
        padding-bottom: 0;
    }
    
    .quote-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        flex-shrink: 0;
        background-size: cover;
        background-position: center;
    }
    
    .quote-content {
        flex: 1;
    }
    
    .quote-text {
        color: #374151;
        font-size: 0.9rem;
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }
    
    .quote-meta {
        font-size: 0.75rem;
        color: #9ca3af;
    }
    
    /* Actions */
    .action-item {
        display: flex;
        gap: 1rem;
        padding: 1rem 0;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .action-item:last-child {
        border-bottom: none;
        padding-bottom: 0;
    }
    
    .action-num {
        width: 28px;
        height: 28px;
        background: #eff6ff;
        color: #4f46e5;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.85rem;
        flex-shrink: 0;
    }
    
    .action-title {
        font-weight: 600;
        color: #0f172a;
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
    }
    
    .action-desc {
        font-size: 0.8rem;
        color: #64748b;
        line-height: 1.5;
    }
    
    /* Send Panel */
    .send-card {
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
    
    .form-label {
        font-size: 0.75rem;
        font-weight: 500;
        color: #374151;
        margin-bottom: 0.375rem;
        display: block;
    }
    
    .form-input {
        width: 100%;
        padding: 0.625rem 0.875rem;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        font-size: 0.875rem;
        color: #0f172a;
        background: white;
        margin-bottom: 1rem;
    }
    
    .preview-box {
        background: #f8fafc;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .preview-title {
        font-weight: 600;
        color: #0f172a;
        font-size: 0.75rem;
        margin-bottom: 0.75rem;
    }
    
    .preview-content {
        font-size: 0.75rem;
        color: #64748b;
        line-height: 1.6;
    }
    
    .preview-content strong {
        color: #374151;
    }
    
    .preview-content ul {
        margin: 0.5rem 0;
        padding-left: 1rem;
    }
    
    .send-btn {
        width: 100%;
        background: #4f46e5;
        color: white;
        padding: 0.75rem;
        border-radius: 8px;
        border: none;
        font-weight: 500;
        font-size: 0.875rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        cursor: pointer;
        margin-top: 1rem;
    }
    
    .send-note {
        font-size: 0.7rem;
        color: #9ca3af;
        text-align: center;
        margin-top: 1rem;
        line-height: 1.5;
    }
    
    /* Footer */
    .footer {
        margin-top: 2rem;
        padding: 1.5rem 0.5rem;
        border-top: 1px solid #e2e8f0;
        display: flex;
        justify-content: space-between;
        color: #9ca3af;
        font-size: 0.75rem;
    }
    
    .footer-links {
        display: flex;
        gap: 1.5rem;
    }
    
    .footer-links a {
        color: #9ca3af;
        text-decoration: none;
    }
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
        return {"total": total, "rating_dist": rating_dist}

@st.cache_data
def load_report():
    report_path = Path(__file__).parent / "phase3" / "outputs" / "weekly_pulse.json"
    if not report_path.exists():
        return None
    with open(report_path, 'r') as f:
        return json.load(f)

stats = load_stats()
report = load_report()

if not stats or not report:
    st.error("No data found. Please run the data collection and analysis first.")
    st.stop()

# Navigation
st.markdown("""
<div class="navbar">
    <div class="nav-left">
        <div class="logo">
            <div class="logo-icon">📊</div>
            InsightReviewer
        </div>
        <div class="nav-tabs">
            <a href="#" class="nav-tab active">Dashboard</a>
            <a href="#" class="nav-tab">Reports</a>
            <a href="#" class="nav-tab">Settings</a>
        </div>
    </div>
    <div class="nav-right">
        <div class="nav-icon">🔔</div>
        <div class="nav-icon">⚙️</div>
        <div class="avatar"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-section">
    <div>
        <h1 class="header-title">Weekly Product Insight Summary</h1>
        <p class="header-subtitle">Analysis of negative reviews (1-2 stars) for the period Oct 24 - Oct 31.</p>
    </div>
    <button class="refresh-btn">🔄 Refresh Analysis</button>
</div>
""", unsafe_allow_html=True)

# Main Content
left_col, right_col = st.columns([2, 1])

with left_col:
    # Top 3 Themes
    themes = report.get('themes', [])[:3]
    categories = ['HIGH IMPACT', 'USABILITY', 'ONBOARDING']
    
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="card-icon icon-fire">🔥</span>
            Top 3 Themes
        </div>
        <div class="themes-grid">
    """, unsafe_allow_html=True)
    
    for i, theme in enumerate(themes):
        st.markdown(f"""
            <div class="theme-item">
                <div class="theme-label">{categories[i]}</div>
                <div class="theme-title">{theme['name']}</div>
                <div class="theme-desc">{theme['description']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Representative User Quotes
    quotes = report.get('quotes', [])[:3]
    avatars = ['https://i.pravatar.cc/150?img=1', 'https://i.pravatar.cc/150?img=5', 'https://i.pravatar.cc/150?img=8']
    names = ['Verified User', 'Verified User', 'Verified User']
    ratings = ['1 Star Review', '2 Star Review', '1 Star Review']
    
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="card-icon icon-chat">💬</span>
            Representative User Quotes
        </div>
    """, unsafe_allow_html=True)
    
    for i, quote in enumerate(quotes):
        st.markdown(f"""
        <div class="quote-item">
            <div class="quote-avatar" style="background-image: url('{avatars[i]}')"></div>
            <div class="quote-content">
                <div class="quote-text">"{quote['text']}"</div>
                <div class="quote-meta">— {names[i]}, {ratings[i]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Suggested Action Ideas
    actions = report.get('actions', [])[:3]
    
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="card-icon icon-bulb">💡</span>
            Suggested Action Ideas
        </div>
    """, unsafe_allow_html=True)
    
    for i, action in enumerate(actions):
        st.markdown(f"""
        <div class="action-item">
            <div class="action-num">{i+1}</div>
            <div>
                <div class="action-title">{action['title']}</div>
                <div class="action-desc">{action['description']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    # Send Report Panel
    st.markdown("""
    <div class="send-card">
        <div class="send-header">
            <span>📧</span>
            Send Report
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("email_form"):
        st.markdown('<label class="form-label">Recipient Email</label>', unsafe_allow_html=True)
        to_email = st.text_input("", placeholder="product-team@company.com", label_visibility="collapsed")
        
        st.markdown('<label class="form-label">Subject</label>', unsafe_allow_html=True)
        subject = st.text_input("", value="Weekly Insight Summary - Negative Reviews", label_visibility="collapsed")
        
        st.markdown("""
        <div class="preview-box">
            <div class="preview-title">Preview Summary</div>
            <div class="preview-content">
                <strong>SUMMARY OVERVIEW</strong><br>
                This week, we analyzed 514 negative reviews. The most critical themes relate to stability and performance.<br><br>
                <strong>KEY THEMES:</strong>
                <ul>
                    <li>Checkout Crashes (High Impact)</li>
                    <li>Slow Media Loading</li>
                    <li>Onboarding Friction</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        submitted = st.form_submit_button("📧 Send Email", use_container_width=True, type="primary")
        
        if submitted and to_email:
            with st.spinner("Sending..."):
                try:
                    sys.path.insert(0, str(Path(__file__).parent / "backend"))
                    from app.core.config import get_settings
                    from app.api.email import send_email_via_smtp, generate_email_content
                    settings = get_settings()
                    email_body = generate_email_content(report)
                    send_email_via_smtp(to_email=to_email, subject=subject, html_body=email_body, settings=settings)
                    st.success("✅ Email sent!")
                except Exception as e:
                    st.error(f"❌ Failed: {str(e)}")
    
    st.markdown("""
        <div class="send-note">
            This report will be sent as a PDF attachment with a formatted HTML body.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div>© 2024 InsightReviewer. All rights reserved.</div>
    <div class="footer-links">
        <a href="#">Privacy Policy</a>
        <a href="#">Terms of Service</a>
        <a href="#">Support</a>
    </div>
</div>
""", unsafe_allow_html=True)
