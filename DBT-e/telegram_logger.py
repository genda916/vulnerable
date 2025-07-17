# telegram_logger.py

import requests

def log_to_telegram(token: str, chat_id: str, message: str):
    """
    Sends a message to a specific Telegram chat using a bot token.

    Args:
        token: The bot token provided by BotFather.
        chat_id: The unique identifier for the target chat.
        message: The string message to be sent.
    
    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    if not token or "YOUR_TELEGRAM_BOT" in token:
        print("ERROR: Telegram token is not configured.")
        return False
    if not chat_id or "YOUR_CHAT_ID" in chat_id:
        print("ERROR: Telegram chat ID is not configured.")
        return False

    api_url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    try:
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'  # Allows for simple formatting
        }
        response = requests.post(api_url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")
        return False
