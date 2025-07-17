from celery import Celery
from config import DISCORD_WEBHOOK, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from discord_logger import log_to_discord
from telegram_logger import log_to_telegram

# Assume Celery is configured to connect to Redis
celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def log_submission_task(message):
    """Sends the main submission log to both services."""
    log_to_discord(DISCORD_WEBHOOK, message)
    log_to_telegram(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, message)

@celery.task
def log_generic_task(message):
    """For logging visitors or other events."""
    # Maybe only log visitors to one place to reduce noise
    log_to_telegram(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, message)

