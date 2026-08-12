import requests
import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

def get_credentials():
    # 1. First check environment variables (ideal for GitHub Actions secrets)
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if token and chat_id:
        return token, chat_id
        
    # 2. Fall back to local config.json
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                config = json.load(f)
                token = config.get("telegram_bot_token")
                chat_id = config.get("telegram_chat_id")
                return token, chat_id
        except Exception:
            pass
            
    return None, None

def send_telegram_alert(message, parse_mode="HTML"):
    """
    Sends a message to the configured Telegram chat.
    """
    token, chat_id = get_credentials()
    
    if not token or token == "YOUR_BOT_TOKEN_HERE":
        print("[Telegram] Alert not sent: Bot Token not configured.")
        return False
    if not chat_id or chat_id == "YOUR_CHAT_ID_HERE":
        print("[Telegram] Alert not sent: Chat ID not configured.")
        return False
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": parse_mode
    }
    
    try:
        response = requests.post(url, json=payload, timeout=8)
        if response.status_code == 200:
            print("[Telegram] Alert sent successfully!")
            return True
        else:
            print(f"[Telegram] Failed to send alert: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[Telegram] Error sending alert: {str(e)}")
        return False

if __name__ == "__main__":
    send_telegram_alert("<b>[Job Monitor]</b> Notifier test successful.")
