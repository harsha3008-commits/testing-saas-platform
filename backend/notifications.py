from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from auth import get_current_user
from database import get_db

router = APIRouter()

# Pydantic Models
class NotificationSettings(BaseModel):
    slack_webhook: Optional[str] = None
    discord_webhook: Optional[str] = None
    email_enabled: bool = False
    whatsapp_enabled: bool = False
    notify_on_failure: bool = True
    notify_on_success: bool = False
    notify_on_completion: bool = True

class NotificationSettingsResponse(BaseModel):
    id: int
    user_id: int
    slack_webhook: Optional[str]
    discord_webhook: Optional[str]
    email_enabled: bool
    whatsapp_enabled: bool
    notify_on_failure: bool
    notify_on_success: bool
    notify_on_completion: bool
    created_at: datetime
    updated_at: datetime

class TestAlert(BaseModel):
    channel: str  # slack, discord, email, whatsapp

# Notification Settings Management
@router.get("/notifications/settings", response_model=NotificationSettingsResponse)
async def get_notification_settings(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's notification settings"""
    cursor = db.execute(
        """
        SELECT id, user_id, slack_webhook, discord_webhook, email_enabled, 
               whatsapp_enabled, notify_on_failure, notify_on_success, 
               notify_on_completion, created_at, updated_at
        FROM notification_settings
        WHERE user_id = %s
        """,
        (current_user["id"],)
    )
    
    settings = cursor.fetchone()
    if not settings:
        # Create default settings
        cursor = db.execute(
            """
            INSERT INTO notification_settings 
            (user_id, email_enabled, notify_on_failure, notify_on_completion, created_at, updated_at)
            VALUES (%s, true, true, true, %s, %s)
            RETURNING id, user_id, slack_webhook, discord_webhook, email_enabled, 
                      whatsapp_enabled, notify_on_failure, notify_on_success, 
                      notify_on_completion, created_at, updated_at
            """,
            (current_user["id"], datetime.utcnow(), datetime.utcnow())
        )
        settings = cursor.fetchone()
        db.commit()
    
    return {
        "id": settings[0],
        "user_id": settings[1],
        "slack_webhook": settings[2],
        "discord_webhook": settings[3],
        "email_enabled": settings[4],
        "whatsapp_enabled": settings[5],
        "notify_on_failure": settings[6],
        "notify_on_success": settings[7],
        "notify_on_completion": settings[8],
        "created_at": settings[9],
        "updated_at": settings[10]
    }

@router.patch("/notifications/settings", response_model=NotificationSettingsResponse)
async def update_notification_settings(
    settings: NotificationSettings,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's notification settings"""
    # Check if settings exist
    existing = db.execute(
        "SELECT id FROM notification_settings WHERE user_id = %s",
        (current_user["id"],)
    ).fetchone()
    
    if existing:
        # Update existing settings
        update_fields = []
        update_values = []
        
        if settings.slack_webhook is not None:
            update_fields.append("slack_webhook = %s")
            update_values.append(settings.slack_webhook)
        
        if settings.discord_webhook is not None:
            update_fields.append("discord_webhook = %s")
            update_values.append(settings.discord_webhook)
        
        update_fields.append("email_enabled = %s")
        update_values.append(settings.email_enabled)
        
        update_fields.append("whatsapp_enabled = %s")
        update_values.append(settings.whatsapp_enabled)
        
        update_fields.append("notify_on_failure = %s")
        update_values.append(settings.notify_on_failure)
        
        update_fields.append("notify_on_success = %s")
        update_values.append(settings.notify_on_success)
        
        update_fields.append("notify_on_completion = %s")
        update_values.append(settings.notify_on_completion)
        
        update_fields.append("updated_at = %s")
        update_values.append(datetime.utcnow())
        
        update_values.append(current_user["id"])
        
        db.execute(
            f"UPDATE notification_settings SET {', '.join(update_fields)} WHERE user_id = %s",
            tuple(update_values)
        )
    else:
        # Create new settings
        db.execute(
            """
            INSERT INTO notification_settings 
            (user_id, slack_webhook, discord_webhook, email_enabled, whatsapp_enabled,
             notify_on_failure, notify_on_success, notify_on_completion, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                current_user["id"],
                settings.slack_webhook,
                settings.discord_webhook,
                settings.email_enabled,
                settings.whatsapp_enabled,
                settings.notify_on_failure,
                settings.notify_on_success,
                settings.notify_on_completion,
                datetime.utcnow(),
                datetime.utcnow()
            )
        )
    
    db.commit()
    return await get_notification_settings(current_user, db)

# Test Notification Endpoints
@router.post("/notifications/test")
async def test_notification(
    alert: TestAlert,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a test notification to verify integration"""
    settings = await get_notification_settings(current_user, db)
    
    message = f"🔔 Test notification from Testing SaaS Platform for {current_user['username']}"
    
    try:
        if alert.channel == "slack":
            if not settings.slack_webhook:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Slack webhook not configured"
                )
            send_slack_notification(settings.slack_webhook, message)
        
        elif alert.channel == "discord":
            if not settings.discord_webhook:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Discord webhook not configured"
                )
            send_discord_notification(settings.discord_webhook, message)
        
        elif alert.channel == "email":
            if not settings.email_enabled:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email notifications not enabled"
                )
            send_email_notification(current_user["email"], "Test Notification", message)
        
        elif alert.channel == "whatsapp":
            if not settings.whatsapp_enabled:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="WhatsApp notifications not enabled"
                )
            # WhatsApp integration would require Twilio or similar service
            return {"message": "WhatsApp integration coming soon"}
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid notification channel"
            )
        
        return {"message": f"Test notification sent successfully to {alert.channel}"}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send notification: {str(e)}"
        )

# Notification Helper Functions
def send_slack_notification(webhook_url: str, message: str, test_run_data: dict = None):
    """Send notification to Slack"""
    if test_run_data:
        status_emoji = "✅" if test_run_data["status"] == "passed" else "❌"
        color = "#36a64f" if test_run_data["status"] == "passed" else "#ff0000"
        
        payload = {
            "attachments": [{
                "color": color,
                "title": f"{status_emoji} Test Run {test_run_data['status'].upper()}",
                "fields": [
                    {
                        "title": "Project",
                        "value": test_run_data["project_name"],
                        "short": True
                    },
                    {
                        "title": "Status",
                        "value": test_run_data["status"],
                        "short": True
                    },
                    {
                        "title": "Tests Passed",
                        "value": f"{test_run_data['tests_passed']}/{test_run_data['total_tests']}",
                        "short": True
                    },
                    {
                        "title": "Duration",
                        "value": f"{test_run_data['duration']}s",
                        "short": True
                    }
                ],
                "footer": "Testing SaaS Platform",
                "ts": int(datetime.utcnow().timestamp())
            }]
        }
    else:
        payload = {"text": message}
    
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()

def send_discord_notification(webhook_url: str, message: str, test_run_data: dict = None):
    """Send notification to Discord"""
    if test_run_data:
        status_emoji = "✅" if test_run_data["status"] == "passed" else "❌"
        color = 0x36a64f if test_run_data["status"] == "passed" else 0xff0000
        
        payload = {
            "embeds": [{
                "title": f"{status_emoji} Test Run {test_run_data['status'].upper()}",
                "color": color,
                "fields": [
                    {
                        "name": "Project",
                        "value": test_run_data["project_name"],
                        "inline": True
                    },
                    {
                        "name": "Status",
                        "value": test_run_data["status"],
                        "inline": True
                    },
                    {
                        "name": "Tests Passed",
                        "value": f"{test_run_data['tests_passed']}/{test_run_data['total_tests']}",
                        "inline": True
                    },
                    {
                        "name": "Duration",
                        "value": f"{test_run_data['duration']}s",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "Testing SaaS Platform"
                },
                "timestamp": datetime.utcnow().isoformat()
            }]
        }
    else:
        payload = {"content": message}
    
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()

def send_email_notification(to_email: str, subject: str, body: str, test_run_data: dict = None):
    """Send email notification"""
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL", smtp_username)
    
    if not smtp_username or not smtp_password:
        raise ValueError("SMTP credentials not configured")
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    
    if test_run_data:
        status_icon = "✅" if test_run_data["status"] == "passed" else "❌"
        html_body = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; }}
                    .status {{ font-size: 24px; font-weight: bold; margin: 20px 0; }}
                    .details {{ background-color: #ffffff; padding: 20px; border: 1px solid #dee2e6; border-radius: 5px; }}
                    .detail-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f1f3f5; }}
                    .footer {{ margin-top: 20px; text-align: center; color: #6c757d; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>Testing SaaS Platform</h2>
                        <div class="status">{status_icon} Test Run {test_run_data["status"].upper()}</div>
                    </div>
                    <div class="details">
                        <div class="detail-row">
                            <span><strong>Project:</strong></span>
                            <span>{test_run_data["project_name"]}</span>
                        </div>
                        <div class="detail-row">
                            <span><strong>Status:</strong></span>
                            <span>{test_run_data["status"]}</span>
                        </div>
                        <div class="detail-row">
                            <span><strong>Tests Passed:</strong></span>
                            <span>{test_run_data["tests_passed"]}/{test_run_data["total_tests"]}</span>
                        </div>
                        <div class="detail-row">
                            <span><strong>Duration:</strong></span>
                            <span>{test_run_data["duration"]}s</span>
                        </div>
                    </div>
                    <div class="footer">
                        <p>This is an automated notification from Testing SaaS Platform</p>
                    </div>
                </div>
            </body>
        </html>
        """
        text_body = f"""
        Testing SaaS Platform
        
        {status_icon} Test Run {test_run_data["status"].upper()}
        
        Project: {test_run_data["project_name"]}
        Status: {test_run_data["status"]}
        Tests Passed: {test_run_data["tests_passed"]}/{test_run_data["total_tests"]}
        Duration: {test_run_data["duration"]}s
        
        This is an automated notification from Testing SaaS Platform
        """
    else:
        html_body = f"""
        <html>
            <body>
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <p>{body}</p>
                    <p style="margin-top: 20px; color: #6c757d; font-size: 12px;">
                        This is an automated notification from Testing SaaS Platform
                    </p>
                </div>
            </body>
        </html>
        """
        text_body = f"{body}\n\nThis is an automated notification from Testing SaaS Platform"
    
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

async def send_test_run_notifications(test_run_id: int, db: Session):
    """Send notifications for a test run based on user settings"""
    # Get test run details
    cursor = db.execute(
        """
        SELECT tr.id, tr.status, tr.tests_passed, tr.total_tests, tr.duration,
               p.name as project_name, p.user_id
        FROM test_runs tr
        JOIN projects p ON tr.project_id = p.id
        WHERE tr.id = %s
        """,
        (test_run_id,)
    )
    
    test_run = cursor.fetchone()
    if not test_run:
        return
    
    test_run_data = {
        "id": test_run[0],
        "status": test_run[1],
        "tests_passed": test_run[2],
        "total_tests": test_run[3],
        "duration": test_run[4],
        "project_name": test_run[5]
    }
    
    # Get user's notification settings
    settings_cursor = db.execute(
        """
        SELECT slack_webhook, discord_webhook, email_enabled, whatsapp_enabled,
               notify_on_failure, notify_on_success, notify_on_completion
        FROM notification_settings
        WHERE user_id = %s
        """,
        (test_run[6],)
    )
    
    settings = settings_cursor.fetchone()
    if not settings:
        return
    
    # Check if we should notify based on status
    should_notify = False
    if test_run_data["status"] == "failed" and settings[4]:  # notify_on_failure
        should_notify = True
    elif test_run_data["status"] == "passed" and settings[5]:  # notify_on_success
        should_notify = True
    elif settings[6]:  # notify_on_completion
        should_notify = True
    
    if not should_notify:
        return
    
    # Get user email
    user_cursor = db.execute(
        "SELECT email FROM users WHERE id = %s",
        (test_run[6],)
    )
    user = user_cursor.fetchone()
    
    # Send notifications to configured channels
    try:
        if settings[0]:  # slack_webhook
            send_slack_notification(settings[0], "", test_run_data)
        
        if settings[1]:  # discord_webhook
            send_discord_notification(settings[1], "", test_run_data)
        
        if settings[2] and user:  # email_enabled
            status_emoji = "✅" if test_run_data["status"] == "passed" else "❌"
            subject = f"{status_emoji} Test Run {test_run_data['status'].upper()} - {test_run_data['project_name']}"
            send_email_notification(user[0], subject, "", test_run_data)
        
        # WhatsApp integration would go here
        
    except Exception as e:
        # Log error but don't fail the test run
        print(f"Error sending notifications for test run {test_run_id}: {str(e)}")