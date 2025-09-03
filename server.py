from flask import Flask, request, jsonify
import threading, os
from tool_spam import start_spam

app = Flask(__name__)

# Task trạng thái
task = {"running": False, "name": "", "message": "", "threads": 0}
spam_thread = None

@app.route("/start", methods=["POST"])
def start():
    global task, spam_thread
    data = request.json
    if task["running"]:
        return jsonify({"status": "already_running", "task": task})
    task = {
        "running": True,
        "name": data.get("name"),
        "message": data.get("message"),
        "threads": int(data.get("threads", 1))
    }
    spam_thread = threading.Thread(target=start_spam, args=(task,), daemon=True)
    spam_thread.start()
    return jsonify({"status": "started", "task": task})

@app.route("/stop", methods=["POST"])
def stop():
    global task
    task["running"] = False
    return jsonify({"status": "stopped"})

@app.route("/status", methods=["GET"])
def status():
    return jsonify(task)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Server running on port {port}")
    app.run(host="0.0.0.0", port=port)
