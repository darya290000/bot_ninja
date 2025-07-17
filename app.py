from flask import Flask, request, jsonify
from telegram_bot import handle_update

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Signal Bot is running."

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json(force=True)  # با force مشکل header رو رد می‌کنیم
    if update:
        handle_update(update)
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "Invalid update"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
