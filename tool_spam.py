import requests
import uuid
import threading
import time
import random

stop_event = threading.Event()

USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 9; Infinix X604) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; PIC-LX9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.101 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G965U1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.141 Mobile Safari/537.36",
]

def spam_once(name, message):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://ngl.link',
        'referer': f'https://ngl.link/{name}',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': random.choice(USER_AGENTS),
    }

    data = {
        'username': str(name),
        'question': str(message),
        'deviceId': str(uuid.uuid4()),
        'gameSlug': '',
        'referrer': '',
    }

    try:
        r = requests.post("https://ngl.link/api/submit", data=data, headers=headers, timeout=10)
        if r.status_code == 200:
            print(f"[SUCCESS] Sent to {name} | UA: {headers['user-agent']}")
        elif r.status_code == 429:
            print("[LIMIT] Hit rate limit, sleeping 20s")
            time.sleep(20)
        else:
            print(f"[FAIL] Status code: {r.status_code}")
    except Exception as e:
        print(f"[ERROR] {e}")

def start_spam(task):
    threads = []
    for i in range(task["threads"]):
        t = threading.Thread(target=worker, args=(task,), daemon=True)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

def worker(task):
    while task["running"]:
        try:
            spam_once(task["name"], task["message"])
        except Exception as e:
            print(f"[Worker Error] {e}")
        time.sleep(0.1)