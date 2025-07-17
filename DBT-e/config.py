# config.py

# Discord Webhook URL
DISCORD_WEBHOOK = "YOUR_DISCORD_WEBHOOK_URL_HERE"

# Telegram Bot Credentials
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID_HERE"

# Redis URL for Celery
# This is the default local URL. Update if your Redis server is elsewhere.
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
