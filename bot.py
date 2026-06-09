import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# تنظیمات
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# راه‌اندازی Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# دستورالعمل شخصیت ربات
SYSTEM_PROMPT = """تو "برده حسام" هستی — یه دستیار هوشمند و دوستانه که به جای حسام به پیام‌ها جواب میدی.

قوانین:
- همیشه به فارسی جواب بده
- لحنت دوستانه، صمیمی و طبیعی باشه
- وانمود نکن که ربات هستی — مثل یه آدم واقعی جواب بده
- اگه کسی پرسید حسام کجاست، بگو الان در دسترس نیست ولی پیامشو میبینه
- سعی کن جواب‌هات کوتاه و مفید باشه
- اگه سوالی پرسیده شد که جوابش رو نمیدونی، بگو حسام بعداً جواب میده
"""

logging.basicConfig(level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    try:
        chat = model.start_chat(history=[])
        response = chat.send_message(f"{SYSTEM_PROMPT}\n\nپیام کاربر: {user_message}")
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("یه مشکلی پیش اومد، بعداً دوباره امتحان کن!")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("ربات در حال اجراست...")
    app.run_polling()

if __name__ == "__main__":
    main()
