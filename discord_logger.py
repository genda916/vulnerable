# discord_logger.py

import requests

def log_to_discord(webhook_url: str, message: str):
    """
    Sends a message to a specific Discord channel using a webhook.

    Args:
        webhook_url: The webhook URL for the Discord channel.
        message: The string message to be sent.
    
    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    if not webhook_url or "YOUR_DISCORD" in webhook_url:
        print("ERROR: Discord webhook URL is not configured.")
        return False
    
    try:
        payload = {'content': message}
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()  # Raises an exception for 4xx or 5xx status codes
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Discord: {e}")
        return False
