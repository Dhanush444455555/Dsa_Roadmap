import datetime
import logging
from zoneinfo import ZoneInfo
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, UserSettings, Roadmap, RoadmapItem, Notification
from app.services.email import send_reminder_email
from app.ai.nodes import HintNode

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()

def check_and_send_daily_reminders():
    """
    Periodic job that checks users whose scheduled reminder time matches current local time in their timezone.
    Idempotent: will not send multiple reminders to the same user on the same date.
    """
    db: Session = SessionLocal()
    try:
        now_utc = datetime.datetime.utcnow()
        users_with_settings = db.query(User).join(UserSettings).filter(
            User.is_active == True,
            UserSettings.paused == False
        ).all()

        for user in users_with_settings:
            settings = user.settings
            if not settings or settings.paused:
                continue

            # Convert UTC now to user's timezone
            user_tz_str = settings.timezone or "UTC"
            try:
                user_tz = ZoneInfo(user_tz_str)
            except Exception:
                user_tz = ZoneInfo("UTC")

            user_now = datetime.datetime.now(user_tz)
            user_today_date = user_now.date()
            user_time_str = user_now.strftime("%H:%M")

            target_reminder_time = settings.reminder_time or "09:00"

            # Check if within reminder window (same hour & minute)
            if user_time_str != target_reminder_time:
                continue

            # Check if reminder already sent today
            today_start = datetime.datetime.combine(user_today_date, datetime.time.min, tzinfo=user_tz).astimezone(datetime.timezone.utc).replace(tzinfo=None)
            already_sent = db.query(Notification).filter(
                Notification.user_id == user.id,
                Notification.type == "reminder",
                Notification.created_at >= today_start
            ).first()

            if already_sent:
                continue

            # Get user's active roadmap
            roadmap = db.query(Roadmap).filter(
                Roadmap.user_id == user.id,
                Roadmap.status == "active"
            ).first()

            if not roadmap:
                continue

            # Check today's problem items
            current_day = roadmap.current_day_index
            today_items = db.query(RoadmapItem).filter(
                RoadmapItem.roadmap_id == roadmap.id,
                RoadmapItem.day_index == current_day
            ).all()

            if not today_items:
                continue

            first_item = today_items[0]
            prob = first_item.problem
            display = HintNode.format_problem_display({
                "number": prob.number,
                "title": prob.title,
                "difficulty": prob.difficulty,
                "topic": prob.topic,
                "pattern": prob.pattern,
                "similar_to": prob.similar_to,
                "url": prob.url
            })

            # Check if user responded to previous problem
            is_blocked = first_item.status == "pending" and current_day > 1 and roadmap.last_response_at is not None and (now_utc - roadmap.last_response_at).total_seconds() > 86400

            title = "Finish yesterday's problem first!" if is_blocked else f"Daily DSA Problem: {display['display_header']}"
            msg_body = (
                f"You haven't finished yesterday's problem yet. {display['display_header']} ({display['display_hint']}). Finish it before advancing!"
                if is_blocked
                else f"Today's problem: {display['display_header']} ({display['display_hint']}). Tip: {display['tip']}"
            )

            # Insert in-app notification
            notification = Notification(
                user_id=user.id,
                title=title,
                message=msg_body,
                type="reminder",
                is_read=False,
                created_at=now_utc
            )
            db.add(notification)
            db.commit()

            # Send Email
            cheatsheet_url = f"http://localhost:5173/today"
            send_reminder_email(
                to_email=user.email,
                user_name=user.name or "Coder",
                problem_header=display["display_header"],
                problem_hint=display["display_hint"],
                cheatsheet_url=cheatsheet_url,
                is_blocked=is_blocked
            )

            logger.info(f"Dispatched daily reminder to user {user.id} ({user.email}).")

    except Exception as e:
        logger.error(f"Error in daily reminder scheduler: {e}")
    finally:
        db.close()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            check_and_send_daily_reminders,
            "interval",
            minutes=1,
            id="daily_dsa_reminders",
            replace_existing=True
        )
        scheduler.start()
        logger.info("APScheduler initialized and running for daily reminders.")

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("APScheduler shut down.")
