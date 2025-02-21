import requests
from decouple import config

TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")

def send_telegram_message(chat_id, post):
    message = f"✅ Ваш пост успешно опубликован!\n\n📢 *Текст:* {post.text[:100]}..."
    if not chat_id:
        return None

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, json=payload)
    return response.json()
