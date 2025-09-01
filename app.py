import os
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Flask server is running!"

@app.route("/log", methods=["GET"])
def log_ip():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    print("Visitor IP:", ip)
    return {"ip": ip}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)