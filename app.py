from flask import Flask, jsonify
import threading
import time
import os
from config import SYMBOLS
from scalper_signals import analyze_symbol
from telegram_bot import send_alert

app = Flask(__name__)
history_data = {}
bot_running = False

def signal_bot():
    """ربات سیگنال‌دهنده که در پس‌زمینه اجرا می‌شود"""
    global bot_running
    bot_running = True
    print("📡 ربات سیگنال‌دهنده شروع شد...")
    
    while bot_running:
        try:
            for symbol in SYMBOLS:
                signal = analyze_symbol(symbol, history_data)
                if signal:
                    send_alert(signal)
            time.sleep(30)  # هر 30 ثانیه یکبار
        except Exception as e:
            print(f"❌ خطا در ربات: {e}")
            time.sleep(5)

@app.route('/')
def home():
    return jsonify({
        "status": "✅ ربات فعال است",
        "symbols": SYMBOLS,
        "bot_running": bot_running
    })

@app.route('/status')
def status():
    return jsonify({
        "bot_running": bot_running,
        "symbols_count": len(SYMBOLS),
        "history_length": {symbol: len(history_data.get(symbol, [])) for symbol in SYMBOLS}
    })

@app.route('/start_bot')
def start_bot():
    global bot_running
    if not bot_running:
        threading.Thread(target=signal_bot, daemon=True).start()
        return jsonify({"message": "🚀 ربات شروع شد"})
    return jsonify({"message": "⚠️ ربات در حال اجراست"})

@app.route('/stop_bot')
def stop_bot():
    global bot_running
    bot_running = False
    return jsonify({"message": "🛑 ربات متوقف شد"})

if __name__ == '__main__':
    # شروع خودکار ربات
    threading.Thread(target=signal_bot, daemon=True).start()
    
    # اجرای Flask
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
