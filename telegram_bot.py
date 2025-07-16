import requests
import os

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

def send_message(chat_id, text):
    if not BOT_TOKEN:
        print("❌ Bot token not set.")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    try:
        resp = requests.post(url, data=data)
        print(f"[📤] Sent to {chat_id}: {text} -> {resp.text}")
    except Exception as e:
        print(f"[❌] Telegram send error: {e}")

def handle_update(update):
    msg = update.get("message", {})
    text = msg.get("text", "").strip()
    chat_id = msg.get("chat", {}).get("id")

    print(f"[📥] Received: {text} from {chat_id}")

    if text == "/start":
        send_message(chat_id, "👋 خوش آمدید!")
    elif text == "/subscribe":
        send_message(chat_id, "✅ شما مشترک سیگنال‌ها شدید.")
    elif text == "/unsubscribe":
        send_message(chat_id, "❌ عضویت لغو شد.")
    elif text == "/status":
        send_message(chat_id, "📡 شما در حال حاضر عضو هستید.")
    elif text == "/help":
        send_message(chat_id, "/start\n/subscribe\n/unsubscribe\n/status")
    else:
        send_message(chat_id, "🤖 دستور معتبر نیست. از /help استفاده کنید.")