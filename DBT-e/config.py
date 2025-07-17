# config.py

# Discord Webhook URL
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1395138384518844508/riuLCmuUuVfVZECJE-zW75VwARH2p9jd8yP_Z1ndjP4gvNMH08Mf7C9PpXcITM-nmw8B"

# Telegram Bot Credentials
TELEGRAM_TOKEN = "7987532893:AAGvwCj4X83Qr5IFYyk3GeO3synDYR5Xh4Y"
TELEGRAM_CHAT_ID = "7285391034"

# Redis URL for Celery
# This is the default local URL. Update if your Redis server is elsewhere.
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
