from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import os

# Thay bằng token bot của bạn
TOKEN = "8404713686:AAF2SmOuGZwu-jcdwNr3ewCTAr-WgCrAbV0"
# Thay bằng URL server Flask
SERVER_URL = "http://127.0.0.1:8080"

def start_command(update, context):
    update.message.reply_text("Bot sẵn sàng. Gửi lệnh theo dạng:\n<name> <message> <threads>")

def spam_command(update, context):
    try:
        text = update.message.text.strip()
        parts = text.split(" ", 2)
        if len(parts) != 3:
            update.message.reply_text("Sai định dạng! Dùng: <name> <message> <threads>")
            return
        name, message, threads = parts
        threads = int(threads)
        r = requests.post(f"{SERVER_URL}/start", json={"name": name, "message": message, "threads": threads})
        update.message.reply_text(f"Server response: {r.json()}")
    except Exception as e:
        update.message.reply_text(f"Lỗi: {e}")

def stop_command(update, context):
    try:
        r = requests.post(f"{SERVER_URL}/stop")
        update.message.reply_text(f"Server response: {r.json()}")
    except Exception as e:
        update.message.reply_text(f"Lỗi: {e}")

def status_command(update, context):
    try:
        r = requests.get(f"{SERVER_URL}/status")
        update.message.reply_text(f"Server status: {r.json()}")
    except Exception as e:
        update.message.reply_text(f"Lỗi: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("stop", stop_command))
    dp.add_handler(CommandHandler("status", status_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, spam_command))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()