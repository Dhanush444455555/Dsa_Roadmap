import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

logger = logging.getLogger(__name__)

def send_reminder_email(
    to_email: str,
    user_name: str,
    problem_header: str,
    problem_hint: str,
    cheatsheet_url: str,
    is_blocked: bool = False
) -> bool:
    """
    Sends daily reminder email via SMTP.
    If is_blocked is True: "Finish yesterday's problem first (the problem does NOT change)".
    """
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.info(f"[DEV MOCK EMAIL] To: {to_email} | Subject: Daily DSA Pathfinder Reminder | Blocked: {is_blocked} | Problem: {problem_header}")
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = settings.EMAILS_FROM
        msg["To"] = to_email

        if is_blocked:
            msg["Subject"] = f"Action Required: Finish yesterday's DSA problem first!"
            html_content = f"""
            <div style="font-family: Arial, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 24px; border-radius: 8px;">
                <h2 style="color: #f59e0b;">DSA Pathfinder Daily Reminder</h2>
                <p>Hi {user_name},</p>
                <div style="background-color: #1e293b; padding: 16px; border-left: 4px solid #f59e0b; margin: 16px 0; border-radius: 4px;">
                    <p style="font-size: 16px; margin: 0; color: #fef3c7;"><strong>Finish yesterday's problem first!</strong></p>
                    <p style="margin: 8px 0 0 0; color: #cbd5e1;">Your roadmap does not advance automatically until you respond to the current problem.</p>
                </div>
                <h3>Current Problem:</h3>
                <p style="font-size: 18px; font-weight: bold; color: #38bdf8;">{problem_header}</p>
                <p style="color: #94a3b8; font-style: italic;">{problem_hint}</p>
                <p style="margin-top: 20px;">
                    <a href="{cheatsheet_url}" style="background-color: #2563eb; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 6px; display: inline-block;">Open Problem & Cheat Sheet</a>
                </p>
            </div>
            """
        else:
            msg["Subject"] = f"Your Daily DSA Challenge: {problem_header}"
            html_content = f"""
            <div style="font-family: Arial, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 24px; border-radius: 8px;">
                <h2 style="color: #3b82f6;">DSA Pathfinder Daily Reminder</h2>
                <p>Hi {user_name},</p>
                <p>Here is your scheduled problem for today:</p>
                <div style="background-color: #1e293b; padding: 16px; border-left: 4px solid #3b82f6; margin: 16px 0; border-radius: 4px;">
                    <p style="font-size: 20px; font-weight: bold; margin: 0; color: #38bdf8;">{problem_header}</p>
                    <p style="font-size: 14px; color: #94a3b8; margin: 8px 0 0 0;">{problem_hint}</p>
                </div>
                <p style="margin-top: 20px;">
                    <a href="{cheatsheet_url}" style="background-color: #2563eb; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 6px; display: inline-block;">View Problem & Open Cheat Sheet</a>
                </p>
            </div>
            """

        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.EMAILS_FROM, [to_email], msg.as_string())

        logger.info(f"Successfully sent reminder email to {to_email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False
