import requests
from config import TOKEN, CHAT_ID

def send_alert(message):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            print(f"[✅] پیام ارسال شد: {message}")
        else:
            print(f"[❌] خطا در ارسال: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"[❌] خطا در ارسال به تلگرام: {e}")
