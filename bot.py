import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """تو "برده حسام" هستی — دستیار هوشمند حسام.
- همیشه به فارسی جواب بده
- لحنت دوستانه و صمیمی باشه
- مثل یه آدم واقعی جواب بده نه ربات
- اگه پرسیدن حسام کجاست بگو الان در دسترس نیست
- جواب‌هات کوتاه و مفید باشه"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\nپیام کاربر: {user_message}")
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("یه مشکلی پیش اومد، بعداً دوباره امتحان کن!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("ربات در حال اجراست...")
    app.run_polling()
