"""Email API endpoints."""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, HTTPException

from app.core.config import get_settings

router = APIRouter(prefix="/api/email", tags=["email"])


class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    report_id: str = "latest"


@router.post("/send-report")
async def send_report_email(request: EmailRequest):
    """Send report via email."""
    settings = get_settings()
    
    # Load report
    if request.report_id == "latest":
        report_path = settings.latest_report_path
    else:
        report_path = settings.reports_dir / f"{request.report_id}.json"
    
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    # Generate email content
    email_body = generate_email_content(report)
    
    # Send email via SMTP
    try:
        send_email_via_smtp(
            to_email=request.to_email,
            subject=request.subject,
            html_body=email_body,
            settings=settings
        )
        return {
            "success": True,
            "message": "Email sent successfully via Gmail",
            "to": request.to_email,
            "subject": request.subject,
            "report_summary": {
                "themes": len(report.get("themes", [])),
                "quotes": len(report.get("quotes", [])),
                "actions": len(report.get("actions", [])),
            }
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to send email: {str(e)}",
            "to": request.to_email,
            "subject": request.subject,
        }


def send_email_via_smtp(to_email: str, subject: str, html_body: str, settings):
    """Send email using Gmail SMTP."""
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    # Create message
    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = settings.email_from
    msg['To'] = to_email
    
    # Create HTML part
    html_part = MIMEText(html_body, 'html', 'utf-8')
    msg.attach(html_part)
    
    # Connect to SMTP server and send
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()  # Enable TLS
        server.login(settings.smtp_user, settings.smtp_password)
        server.sendmail(settings.email_from, to_email, msg.as_string())


def generate_email_content(report: dict) -> str:
    """Generate HTML email content with visual dashboard."""
    themes = report.get("themes", [])
    quotes = report.get("quotes", [])
    actions = report.get("actions", [])
    total_reviews = report.get('total_reviews', 1)
    
    # Calculate percentages for top themes
    for theme in themes:
        theme['percentage'] = round((theme.get('review_count', 0) / total_reviews) * 100)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f8f9fa; margin: 0; padding: 20px;">
        <div style="max-width: 900px; margin: 0 auto;">
            
            <!-- Header -->
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #1f2937; font-size: 24px; font-weight: 600; margin: 0 0 8px 0;">Weekly Product Insight Summary</h1>
                <p style="color: #6b7280; font-size: 14px; margin: 0;">Analysis of negative reviews (1-2 stars) for the period {report.get('week_range', 'Oct 24 - Oct 31')}</p>
            </div>
            
            <!-- Top 3 Summary Cards -->
            <div style="display: table; width: 100%; margin-bottom: 24px; border-spacing: 16px 0; margin-left: -16px; margin-right: -16px;">
    """
    
    # Top 3 summary cards
    card_colors = [
        {'bg': '#fef2f2', 'border': '#fecaca', 'icon': '🔥'},
        {'bg': '#fffbeb', 'border': '#fcd34d', 'icon': '⚡'},
        {'bg': '#eff6ff', 'border': '#bfdbfe', 'icon': '💡'}
    ]
    
    for i, theme in enumerate(themes[:3]):
        color = card_colors[i % len(card_colors)]
        html += f"""
                <div style="display: table-cell; width: 33.33%; background-color: {color['bg']}; border: 1px solid {color['border']}; border-radius: 12px; padding: 20px; vertical-align: top;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                        <span style="font-size: 12px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">Theme {i+1}</span>
                        <span style="font-size: 16px;">{color['icon']}</span>
                    </div>
                    <h3 style="color: #1f2937; font-size: 16px; font-weight: 600; margin: 0;">{theme.get('name', '')}</h3>
                </div>
        """
    
    html += """
            </div>
            
            <!-- Three Column Layout -->
            <div style="display: table; width: 100%; border-spacing: 16px 0; margin-left: -16px; margin-right: -16px;">
    """
    
    # Column 1: Top 3 Themes
    html += """
                <!-- Themes Column -->
                <div style="display: table-cell; width: 33.33%; background-color: white; border-radius: 12px; padding: 20px; vertical-align: top; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
                        <span style="color: #6366f1;">☰</span>
                        <h2 style="color: #1f2937; font-size: 14px; font-weight: 600; margin: 0;">Top 3 Themes</h2>
                    </div>
    """
    
    for theme in themes[:3]:
        html += f"""
                    <div style="background-color: #f9fafb; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
                        <h4 style="color: #1f2937; font-size: 13px; font-weight: 600; margin: 0 0 6px 0;">{theme.get('name', '')}</h4>
                        <p style="color: #6b7280; font-size: 12px; line-height: 1.5; margin: 0;">{theme.get('description', '')}</p>
                    </div>
        """
    
    html += """
                </div>
    """
    
    # Column 2: User Quotes
    html += """
                <!-- Quotes Column -->
                <div style="display: table-cell; width: 33.33%; background-color: white; border-radius: 12px; padding: 20px; vertical-align: top; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
                        <span style="color: #6366f1;">❝</span>
                        <h2 style="color: #1f2937; font-size: 14px; font-weight: 600; margin: 0;">User Quotes</h2>
                    </div>
    """
    
    for quote in quotes[:3]:
        html += f"""
                    <div style="border-left: 3px solid #6366f1; padding-left: 12px; margin-bottom: 16px;">
                        <p style="color: #4b5563; font-size: 13px; line-height: 1.6; margin: 0 0 8px 0; font-style: italic;">"{quote.get('text', '')}"</p>
                    </div>
        """
    
    html += """
                </div>
    """
    
    # Column 3: Action Ideas
    html += """
                <!-- Actions Column -->
                <div style="display: table-cell; width: 33.33%; background-color: white; border-radius: 12px; padding: 20px; vertical-align: top; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
                        <span style="color: #10b981;">⚡</span>
                        <h2 style="color: #1f2937; font-size: 14px; font-weight: 600; margin: 0;">Action Ideas</h2>
                    </div>
    """
    
    for i, action in enumerate(actions[:3]):
        html += f"""
                    <table style="width: 100%; margin-bottom: 16px; border-collapse: collapse;">
                        <tr>
                            <td style="width: 28px; vertical-align: top; padding: 0;">
                                <div style="width: 24px; height: 24px; background-color: #6366f1; color: white; border-radius: 50%; text-align: center; line-height: 24px; font-size: 12px; font-weight: 600;">{i+1}</div>
                            </td>
                            <td style="vertical-align: top; padding: 0 0 0 12px;">
                                <h4 style="color: #1f2937; font-size: 13px; font-weight: 600; margin: 0 0 4px 0; line-height: 24px;">{action.get('title', '')}</h4>
                                <p style="color: #6b7280; font-size: 12px; line-height: 1.5; margin: 0;">{action.get('description', '')}</p>
                            </td>
                        </tr>
                    </table>
        """
    
    html += """
                </div>
            </div>
            
            <!-- Footer -->
            <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
                <p style="color: #9ca3af; font-size: 12px; margin: 0;">Generated by GrowwReviews AI Tool</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html
