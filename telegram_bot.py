import requests
from config import TOKEN, CHAT_ID

def send_alert(message):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID.strip(),  # حذف فاصله اضافی
        'text': message,
        'parse_mode': 'HTML'  # برای فرمت بهتر
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            print(f"[✅] سیگنال ارسال شد: {message}")
        else:
            print(f"[❌] خطا در ارسال: {response.status_code}")
    except Exception as e:
        print(f"[❌] خطا در ارسال تلگرام: {e}")
