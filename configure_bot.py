import requests
import json
import os
import sys

TOKEN = "8594154641:AAGsUN128K9Yem-OjmsCQgjmxOkmQFGxwbE"
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

def configure():
    print("Checking for messages sent to the bot...")
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Error checking updates: {response.status_code} - {response.text}")
            return False
            
        data = response.json()
        results = data.get("result", [])
        if not results:
            print("\n[Action Required] No messages found!")
            print("Please follow these steps:")
            print("1. Open Telegram and search for @Dddeerick_bot (or go to t.me/Dddeerick_bot)")
            print("2. Click 'Start' or send any message to the bot.")
            print("3. Re-run this script.")
            return False
            
        # Get chat ID of the latest message sender
        latest_message = results[-1]
        chat_id = None
        if "message" in latest_message:
            chat_id = latest_message["message"]["chat"]["id"]
            username = latest_message["message"]["chat"].get("first_name", "User")
        elif "my_chat_member" in latest_message:
            chat_id = latest_message["my_chat_member"]["chat"]["id"]
            username = latest_message["my_chat_member"]["chat"].get("first_name", "User")
            
        if not chat_id:
            print("Could not retrieve Chat ID from updates.")
            return False
            
        print(f"Found Chat ID: {chat_id} for user: {username}")
        
        # Save to config.json
        config = {
            "telegram_bot_token": TOKEN,
            "telegram_chat_id": str(chat_id)
        }
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)
        print("Successfully updated config.json!")
        
        # Send confirmation message
        send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        confirm_text = f"🎉 <b>Success!</b>\n\nHi {username}, your Job Monitor is now successfully configured and running. You will receive alerts here when new matching jobs are found."
        requests.post(send_url, json={"chat_id": chat_id, "text": confirm_text, "parse_mode": "HTML"}, timeout=10)
        print("Sent confirmation alert via Telegram bot.")
        return True
    except Exception as e:
        print(f"Error configuring bot: {str(e)}")
        return False

if __name__ == "__main__":
    configure()
