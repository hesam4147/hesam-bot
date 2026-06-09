import os
import logging
import requests
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

SYSTEM_PROMPT = """تو "برده حسام" هستی.
- فارسی جواب بده
- دوستانه و صمیمی باش
- اگه پرسیدن حسام کجاست بگو الان در دسترس نیست"""

def ask_gemini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    r = requests.post(url, json={"contents":[{"parts":[{"text":f"{SYSTEM_PROMPT}\nپیام: {text}"}]}]})
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]

def handle(update, context):
    try:
        reply = ask_gemini(update.message.text)
        update.message.reply_text(reply)
    except Exception as e:
        update.message.reply_text("مشکلی پیش اومد!")

updater = Updater(TELEGRAM_TOKEN)
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle))
updater.start_polling()
updater.idle()
