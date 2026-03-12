"""Streamlit Dashboard for Groww Reviews Weekly Pulse - Styled Version."""

import streamlit as st
import json
import sqlite3
from pathlib import Path
import sys

# Add paths
sys.path.insert(0, str(Path(__file__).parent / "phase2"))
sys.path.insert(0, str(Path(__file__).parent / "phase3"))

# Custom CSS to match the reference design
st.set_page_config(
    page_title="InsightReviewer - Weekly Product Insight Summary",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header styling */
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
    }
    
    /* Stats cards */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 4px solid #667eea;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .stat-label {
        color: #6b7280;
        font-size: 0.9rem;
    }
    
    /* Theme cards */
    .theme-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-top: 4px solid;
    }
    
    .theme-card.high { border-top-color: #ef4444; }
    .theme-card.medium { border-top-color: #f59e0b; }
    .theme-card.low { border-top-color: #10b981; }
    
    .theme-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .theme-desc {
        color: #6b7280;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    .theme-count {
        display: inline-block;
        background: #f3f4f6;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        color: #6b7280;
        margin-top: 0.5rem;
    }
    
    /* Quote cards */
    .quote-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #8b5cf6;
    }
    
    .quote-text {
        font-style: italic;
        color: #374151;
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }
    
    .quote-source {
        color: #6b7280;
        font-size: 0.85rem;
    }
    
    /* Action cards */
    .action-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        display: flex;
        gap: 1rem;
    }
    
    .action-number {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        flex-shrink: 0;
    }
    
    .action-content {
        flex: 1;
    }
    
    .action-title {
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .action-desc {
        color: #6b7280;
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 0.5rem;
    }
    
    .action-meta {
        display: flex;
        gap: 1rem;
        font-size: 0.8rem;
    }
    
    .priority-high { color: #ef4444; }
    .priority-medium { color: #f59e0b; }
    .priority-low { color: #10b981; }
    
    /* Section headers */
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1f2937;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
    }
    
    /* Email form */
    .email-section {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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

# Header
st.markdown("""
<div class="dashboard-header">
    <h1 style="margin:0; font-size:2rem;">📊 InsightReviewer</h1>
    <p style="margin:0.5rem 0 0 0; opacity:0.9;">Weekly Product Insight Summary</p>
    <p style="margin:0.5rem 0 0 0; font-size:0.9rem; opacity:0.8;">
        Analysis of negative reviews (1-2 stars) for the period Oct 24 - Oct 31
    </p>
</div>
""", unsafe_allow_html=True)

# Load data
stats = load_stats()
report = load_report()

if not stats or not report:
    st.error("No data found. Please run the data collection and analysis first.")
    st.stop()

# Stats row
st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{stats['total']}</div>
        <div class="stat-label">Total Reviews</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{stats['rating_dist'].get(1, 0)}</div>
        <div class="stat-label">1-Star Reviews</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{stats['rating_dist'].get(2, 0)}</div>
        <div class="stat-label">2-Star Reviews</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    date_range_text = f"{stats['date_range'][0]} to {stats['date_range'][1]}" if stats['date_range'] else "N/A"
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number" style="font-size:1rem;">{date_range_text}</div>
        <div class="stat-label">Date Range</div>
    </div>
    """, unsafe_allow_html=True)

# Top 3 Themes
st.markdown("<div class='section-header'>🔥 Top 3 Themes</div>", unsafe_allow_html=True)
themes = report.get('themes', [])[:3]
impact_classes = {'HIGH': 'high', 'MEDIUM': 'medium', 'LOW': 'low'}

cols = st.columns(3)
for i, (theme, col) in enumerate(zip(themes, cols)):
    impact_class = impact_classes.get(theme.get('impact', 'MEDIUM'), 'medium')
    with col:
        st.markdown(f"""
        <div class="theme-card {impact_class}">
            <div style="font-size:0.75rem; color:#6b7280; margin-bottom:0.5rem;">
                {theme.get('impact', 'MEDIUM')} IMPACT
            </div>
            <div class="theme-title">{theme['name']}</div>
            <div class="theme-desc">{theme['description']}</div>
            <div class="theme-count">{theme['review_count']} mentions</div>
        </div>
        """, unsafe_allow_html=True)

# Three columns layout
st.markdown("<div class='section-header'>📋 Detailed Analysis</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

# Themes column
with col1:
    st.markdown("<h4 style='color:#667eea;'>☰ Top 3 Themes</h4>", unsafe_allow_html=True)
    for theme in themes:
        st.markdown(f"""
        <div style="background:white; padding:1rem; border-radius:8px; margin-bottom:0.75rem; box-shadow:0 1px 3px rgba(0,0,0,0.1);">
            <div style="font-weight:600; color:#1f2937; margin-bottom:0.25rem;">{theme['name']}</div>
            <div style="font-size:0.85rem; color:#6b7280;">{theme['description']}</div>
        </div>
        """, unsafe_allow_html=True)

# Quotes column
with col2:
    st.markdown("<h4 style='color:#8b5cf6;'>❝ User Quotes</h4>", unsafe_allow_html=True)
    quotes = report.get('quotes', [])[:3]
    for quote in quotes:
        st.markdown(f"""
        <div class="quote-card">
            <div class="quote-text">"{quote['text']}"</div>
            <div class="quote-source">— {quote['theme']}</div>
        </div>
        """, unsafe_allow_html=True)

# Actions column
with col3:
    st.markdown("<h4 style='color:#10b981;'>⚡ Action Ideas</h4>", unsafe_allow_html=True)
    actions = report.get('actions', [])[:3]
    for i, action in enumerate(actions):
        priority_class = f"priority-{action['priority'].lower()}"
        st.markdown(f"""
        <div class="action-card">
            <div class="action-number">{i+1}</div>
            <div class="action-content">
                <div class="action-title">{action['title']}</div>
                <div class="action-desc">{action['description']}</div>
                <div class="action-meta">
                    <span class="{priority_class}">● {action['priority']}</span>
                    <span style="color:#6b7280;">⚡ {action['effort']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Email section
st.markdown("<div class='section-header'>📧 Send Report via Email</div>", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("email_form", clear_on_submit=False):
            to_email = st.text_input("Recipient Email", placeholder="product-team@company.com")
            subject = st.text_input("Subject", value="Weekly Insight Summary - Negative Reviews")
            
            submitted = st.form_submit_button("📧 Send Email", use_container_width=True, type="primary")
            
            if submitted:
                if to_email:
                    with st.spinner("Sending email..."):
                        try:
                            sys.path.insert(0, str(Path(__file__).parent / "backend"))
                            from app.core.config import get_settings
                            from app.api.email import send_email_via_smtp, generate_email_content
                            
                            settings = get_settings()
                            email_body = generate_email_content(report)
                            
                            send_email_via_smtp(
                                to_email=to_email,
                                subject=subject,
                                html_body=email_body,
                                settings=settings
                            )
                            st.success(f"✅ Email sent successfully to {to_email}")
                        except Exception as e:
                            st.error(f"❌ Failed to send email: {str(e)}")
                else:
                    st.warning("Please enter an email address")
    
    with col2:
        st.markdown("""
        <div style="background:#f9fafb; padding:1rem; border-radius:8px; border:1px solid #e5e7eb;">
            <h5 style="margin-top:0; color:#374151;">Preview Summary</h5>
            <p style="font-size:0.85rem; color:#6b7280; margin-bottom:1rem;">
                This report will be sent as an HTML attachment with a formatted email body.
            </p>
            <div style="font-size:0.8rem; color:#9ca3af;">
                <strong>SUMMARY OVERVIEW</strong><br>
                This week, we analyzed 667 negative reviews. The most critical themes relate to stability and performance.
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<div style='margin-top:3rem; padding:1rem; text-align:center; color:#9ca3af; font-size:0.85rem;'>", unsafe_allow_html=True)
st.markdown("Generated by InsightReviewer AI Tool | © 2024")
