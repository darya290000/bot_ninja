from flask import Flask, request, jsonify
from telegram_bot import handle_update

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Signal Bot is running."

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    if update:
        handle_update(update)
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)