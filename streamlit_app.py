"""Streamlit Dashboard - Redesigned to Match Reference UI."""

import streamlit as st
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "phase2"))
sys.path.insert(0, str(Path(__file__).parent / "phase3"))

st.set_page_config(page_title="InsightReviewer", layout="wide", initial_sidebar_state="collapsed")

# ── Global CSS ──
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background-color: #f8fafc; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1200px !important; }
.stFormSubmitButton > button {
    background-color: #6366f1 !important;
    color: white !important;
    border: none !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.5rem !important;
}
.stFormSubmitButton > button:hover {
    background-color: #4f46e5 !important;
    color: white !important;
}
.stTextInput > div > div > input {
    border-radius: 8px !important;
    border: 1px solid #e2e8f0 !important;
    font-size: 0.85rem !important;
}
.stTextInput > label {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #374151 !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
    background-color: #6366f1 !important;
    color: white !important;
    border: none !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    background-color: #4f46e5 !important;
    color: white !important;
}
</style>""", unsafe_allow_html=True)


# ── Data Loading ──
def load_report():
    path = Path(__file__).parent / "phase3" / "outputs" / "weekly_pulse.json"
    if path.exists():
        with open(path, 'r') as f:
            return json.load(f)
    return None


report = load_report()
if not report:
    st.error("No data found. Run the pipeline first.")
    st.stop()

week_range = report.get('week_range', 'N/A')
total_reviews = report.get('total_reviews', 0)


# ── Header ──
header_left, header_right = st.columns([3, 1])
with header_left:
    st.markdown(
        f"<h1 style='font-size:1.6rem; font-weight:700; color:#0f172a; margin:0 0 0.25rem 0;'>Weekly Product Insight Summary</h1>"
        f"<p style='font-size:0.85rem; color:#64748b; margin:0;'>Analysis of negative reviews (1-2 stars) for the period {week_range}.</p>",
        unsafe_allow_html=True
    )
with header_right:
    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Analysis", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)


# ── Main Layout ──
left_col, right_col = st.columns([2, 1], gap="large")


# ── LEFT COLUMN ──
with left_col:

    # ── Top 3 Themes Card ──
    themes = report.get('themes', [])[:3]
    cat_labels = ['HIGH IMPACT', 'USABILITY', 'ONBOARDING']
    cat_colors = ['#ef4444', '#f59e0b', '#6366f1']
    cat_bg = ['#fef2f2', '#fffbeb', '#eef2ff']

    theme_items = ""
    for i, theme in enumerate(themes):
        theme_items += (
            f'<div>'
            f'<div style="display:inline-block; font-size:0.6rem; font-weight:700; text-transform:uppercase; '
            f'color:{cat_colors[i]}; letter-spacing:0.05em; margin-bottom:0.6rem; '
            f'background:{cat_bg[i]}; padding:2px 8px; border-radius:4px;">{cat_labels[i]}</div>'
            f'<div style="font-weight:600; color:#0f172a; margin-bottom:0.4rem; font-size:0.95rem;">{theme["name"]}</div>'
            f'<div style="font-size:0.8rem; color:#64748b; line-height:1.6;">{theme["description"]}</div>'
            f'</div>'
        )

    st.markdown(
        '<div style="background:white; border-radius:14px; border:1px solid #e2e8f0; padding:1.5rem 1.75rem; margin-bottom:1.5rem; box-shadow:0 1px 3px rgba(0,0,0,0.04);">'
        '<div style="display:flex; align-items:center; gap:0.5rem; font-weight:600; color:#6366f1; margin-bottom:1.5rem; font-size:0.95rem;">'
        '<span style="font-size:1.1rem;">🔥</span> Top 3 Themes</div>'
        '<div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:1.25rem;">'
        + theme_items +
        '</div></div>',
        unsafe_allow_html=True
    )

    # ── Representative User Quotes Card ──
    quotes = report.get('quotes', [])[:3]
    avatar_colors = ['#f97316', '#3b82f6', '#8b5cf6']
    avatar_initials = ['U1', 'U2', 'U3']
    star_ratings = [1, 2, 1]

    quote_items = ""
    for i, quote in enumerate(quotes):
        bb = "border-bottom:1px solid #f1f5f9;" if i < len(quotes) - 1 else ""
        rating = quote.get('rating', star_ratings[i] if i < len(star_ratings) else 1)
        quote_items += (
            f'<div style="display:flex; gap:1rem; padding:1rem 0; {bb}">'
            f'<div style="width:40px; height:40px; background:{avatar_colors[i]}; color:white; border-radius:50%; '
            f'display:flex; align-items:center; justify-content:center; font-weight:700; font-size:0.75rem; flex-shrink:0; margin-top:2px;">'
            f'{avatar_initials[i]}</div>'
            f'<div style="flex:1;">'
            f'<div style="color:#374151; font-size:0.88rem; line-height:1.65; font-style:italic; margin-bottom:0.4rem;">'
            f'&ldquo;{quote["text"]}&rdquo;</div>'
            f'<div style="font-size:0.72rem; color:#9ca3af;">&mdash; Verified User, {rating} Star Review</div>'
            f'</div></div>'
        )

    st.markdown(
        '<div style="background:white; border-radius:14px; border:1px solid #e2e8f0; padding:1.5rem 1.75rem; margin-bottom:1.5rem; box-shadow:0 1px 3px rgba(0,0,0,0.04);">'
        '<div style="display:flex; align-items:center; gap:0.5rem; font-weight:600; color:#6366f1; margin-bottom:1.5rem; font-size:0.95rem;">'
        '<span style="font-size:1.1rem;">💬</span> Representative User Quotes</div>'
        + quote_items +
        '</div>',
        unsafe_allow_html=True
    )

    # ── Suggested Action Ideas Card ──
    actions = report.get('actions', [])[:3]

    action_items = ""
    for i, action in enumerate(actions):
        bb = "border-bottom:1px solid #f1f5f9;" if i < len(actions) - 1 else ""
        action_items += (
            f'<div style="display:flex; gap:1rem; padding:1rem 0; {bb}">'
            f'<div style="width:32px; height:32px; background:#ede9fe; color:#6366f1; border-radius:50%; '
            f'display:flex; align-items:center; justify-content:center; font-weight:700; font-size:0.85rem; flex-shrink:0;">'
            f'{i + 1}</div>'
            f'<div style="flex:1;">'
            f'<div style="font-weight:600; color:#0f172a; font-size:0.92rem; margin-bottom:0.3rem;">{action["title"]}</div>'
            f'<div style="font-size:0.8rem; color:#64748b; line-height:1.6;">{action["description"]}</div>'
            f'</div></div>'
        )

    st.markdown(
        '<div style="background:white; border-radius:14px; border:1px solid #e2e8f0; padding:1.5rem 1.75rem; margin-bottom:1.5rem; box-shadow:0 1px 3px rgba(0,0,0,0.04);">'
        '<div style="display:flex; align-items:center; gap:0.5rem; font-weight:600; color:#6366f1; margin-bottom:1.5rem; font-size:0.95rem;">'
        '<span style="font-size:1.1rem;">💡</span> Suggested Action Ideas</div>'
        + action_items +
        '</div>',
        unsafe_allow_html=True
    )


# ── RIGHT COLUMN ──
with right_col:

    # ── Send Report Card ──
    with st.form("email"):
        st.markdown(
            '<div style="display:flex; align-items:center; gap:0.6rem; font-weight:700; color:#0f172a; margin-bottom:0.25rem; font-size:1rem;">'
            '<span style="font-size:1.1rem;">✈️</span> Send Report</div>',
            unsafe_allow_html=True
        )
        to_email = st.text_input("Recipient Email", placeholder="product-team@company.com", key="email_to")
        subject = st.text_input("Subject", value=f"Weekly Insight Summary: Negative Reviews ({week_range})", key="email_subject")

        # Preview summary with left purple border accent
        themes_list = "".join([f"<li style='margin-bottom:0.3rem;'>{t['name']} ({t.get('severity', 'High').title()} Impact)</li>" for t in themes])
        st.markdown(
            '<div style="font-weight:600; color:#0f172a; font-size:0.82rem; margin-bottom:0.5rem; margin-top:0.5rem;">Preview Summary</div>'
            '<div style="border-left:3px solid #6366f1; background:#f8fafc; border-radius:0 8px 8px 0; padding:1rem 1rem 1rem 1rem; margin:0 0 1rem 0; font-size:0.78rem; color:#64748b;">'
            '<div>'
            '<strong style="font-size:0.75rem; letter-spacing:0.03em; color:#0f172a;">SUMMARY OVERVIEW</strong><br>'
            f'<span style="line-height:1.7;">This week we analyzed {total_reviews} negative reviews. The core issues remain technical stability and performance.</span><br><br>'
            '<strong style="font-size:0.75rem; letter-spacing:0.03em; color:#0f172a;">KEY THEMES:</strong>'
            f'<ul style="margin:0.4rem 0 0 0; padding-left:1.2rem; line-height:1.8;">{themes_list}</ul>'
            '</div></div>',
            unsafe_allow_html=True
        )

        submitted = st.form_submit_button("📧 Send Email", use_container_width=True)

        if submitted:
            try:
                backend_dir = Path(__file__).parent / "backend"
                sys.path.insert(0, str(backend_dir))
                from app.core.config import Settings
                from app.api.email import send_email_with_attachment, generate_email_content, generate_reviews_csv

                # Load settings from the backend .env (not the project root)
                env_path = backend_dir / ".env"
                settings = Settings(
                    _env_file=str(env_path),
                    data_dir=Path(__file__).parent / "phase2" / "data",
                    reports_dir=Path(__file__).parent / "phase3" / "outputs"
                )
                email_body = generate_email_content(report)
                csv_data = generate_reviews_csv(settings)
                to_email_value = to_email if to_email else 'product-team@company.com'
                subject_value = subject if subject else 'Weekly Insight Summary'
                send_email_with_attachment(
                    to_email=to_email_value,
                    subject=subject_value,
                    html_body=email_body,
                    csv_data=csv_data,
                    settings=settings
                )
                st.success("✅ Email sent successfully with CSV attachment!")
            except Exception as e:
                st.error(f"❌ Failed to send email: {str(e)}")

    st.markdown(
        '<div style="font-size:0.68rem; color:#9ca3af; text-align:center; margin-top:0.75rem;">'
        'The report will be sent as a formatted HTML body with a CSV attachment containing review data.</div></div>',
        unsafe_allow_html=True
    )


# ── Footer ──
st.markdown(
    '<div style="margin-top:2.5rem; padding:1.5rem 0; border-top:1px solid #e2e8f0; display:flex; justify-content:space-between; align-items:center; color:#9ca3af; font-size:0.75rem;">'
    '<div>&copy; 2024 InsightReviewer AI Tool. All rights reserved.</div>'
    '<div style="display:flex; gap:1.5rem;">'
    '<span style="cursor:pointer;">Privacy Policy</span>'
    '<span style="cursor:pointer;">Terms of Service</span>'
    '<span style="cursor:pointer;">Support</span>'
    '</div></div>',
    unsafe_allow_html=True
)
