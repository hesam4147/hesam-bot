import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

SYSTEM_PROMPT = """تو "برده حسام" هستی — دستیار هوشمند حسام.
- همیشه به فارسی جواب بده
- لحنت دوستانه و صمیمی باشه
- مثل یه آدم واقعی جواب بده نه ربات
- اگه پرسیدن حسام کجاست بگو الان در دسترس نیست
- جواب‌هات کوتاه و مفید باشه"""

def ask_gemini(user_message):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    data = {
        "contents": [
            {
                "parts": [
                    {"text": f"{SYSTEM_PROMPT}\n\nپیام کاربر: {user_message}"}
                ]
            }
        ]
    }
    response = requests.post(url, json=data)
    result = response.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        reply = ask_gemini(user_message)
        await update.message.reply_text(reply)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("یه مشکلی پیش اومد، بعداً دوباره امتحان کن!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("ربات در حال اجراست...")
    app.run_polling()
