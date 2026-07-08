import os
import base64
import tempfile
import logging

from openai import OpenAI

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# -----------------------------
# Logging
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# -----------------------------
# Environment Variables
# -----------------------------

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# -----------------------------
# AI Prompt
# -----------------------------

SYSTEM_PROMPT = """
تۆ Professional Gold Analystیت.

تەنها ستراتیژی زیندان بەکاربهێنە.

یاساکان:

1- Trend بناسەوە.
2- Support بناسەوە.
3- Resistance بناسەوە.
4- Sideway بناسەوە.
5- Breakout تەنها ئەگەر 75% داخستبێت.
6- Pullback چاوەڕوان بکە.
7- Inversion بناسەوە.
8- BUY / SELL / WAIT دیاری بکە.

وەڵام تەنها بە زمانی کوردی.

ئەم شێوازە بەکاربهێنە:

📈 Trend

🟢 Support

🔴 Resistance

🔄 Breakout

♻️ Pullback

📊 Inversion

🎯 Decision

📝 هۆکار
"""

# -----------------------------
# /start
# -----------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 بەخێربێیت بۆ Zindan Gold Bot\n\n"
        "📷 وێنەی چارت بنێرە بۆ شیکردنەوە."
    )# -----------------------------
# Analyze Image
# -----------------------------

async def analyze_chart(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.photo:
        await update.message.reply_text(
            "تکایە تەنها وێنەی چارت بنێرە."
        )
        return

    photo = update.message.photo[-1]

    telegram_file = await photo.get_file()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:

        await telegram_file.download_to_drive(temp.name)

        image_path = temp.name

    with open(image_path, "rb") as image:

        image_base64 = base64.b64encode(
            image.read()
        ).decode("utf-8")

    await update.message.reply_text(
        "⏳ چارتەکە شیدەکرێتەوە..."
    )

    response = client.responses.create(

        model="gpt-4.1",

        input=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": [

                    {
                        "type": "input_text",
                        "text": "Analyze this Gold chart only
                        # -----------------------------
# Main Function
# -----------------------------

def main():

    if BOT_TOKEN is None:
        raise ValueError("BOT_TOKEN not found")

    if OPENAI_API_KEY is None:
        raise ValueError("OPENAI_API_KEY not found")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            analyze_chart
        )
    )

    print("✅ Zindan Gold Bot Started...")

    application.run_polling()


if __name__ == "__main__":
    main()