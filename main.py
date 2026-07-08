import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import OpenAI

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# -----------------------------
# Environment Variables
# -----------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# -----------------------------
# Start Command
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 بەخێربێیت بۆ Zindan Gold Bot\n\n"
        "📷 تەنها وێنەی چارت بنێرە.\n\n"
        "من چارتەکە بە ستراتیژی زیندان شیدەکەمەوە و:\n\n"
        "✅ BUY\n"
        "🔴 SELL\n"
        "🟡 WAIT\n\n"
        "هەروەها هۆکارەکەشی بە کوردی ڕوون دەکەمەوە."
    )

    await update.message.reply_text(text)
    # -----------------------------
# Strategy Prompt
# -----------------------------
SYSTEM_PROMPT = """
تۆ شیکارکەرێکی پڕۆفیشناڵی Gold Chartیت.

تەنها بە ستراتیژی زیندان کار بکە.

یاساکان:

1- Trend دیاری بکە.
2- Support دیاری بکە.
3- Resistance دیاری بکە.
4- Sideway ئەگەر هەبوو WAIT.
5- Breakout تەنها ئەگەر 75% یان زیاتر لە دەرەوەی زۆنەکە داخستبوو.
6- Pullback چاوەڕوان بکە.
7- Inversion بناسەوە.
8- ئەگەر هەموو مەرجەکان تەواو بوون BUY یان SELL بدە.

وەڵامەکەت تەنها بە زمانی کوردی بێت.

بەم شێوەیە:

📈 Trend:
...

🟩 Support:
...

🟥 Resistance:
...

🔄 Breakout:
...

♻️ Pullback:
...

📊 Inversion:
...

🎯 Decision:
BUY / SELL / WAIT

📝 هۆکار:
...
"""
# -----------------------------
# Image Message Handler
# -----------------------------
import base64
import tempfile


async def analyze_chart(update: Update, context: ContextTypes.DEFAULT_TYPE):

    photo = update.message.photo[-1]

    telegram_file = await photo.get_file()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
        await telegram_file.download_to_drive(temp.name)
        image_path = temp.name

    with open(image_path, "rb") as img:
        image_base64 = base64.b64encode(img.read()).decode("utf-8")

    await update.message.reply_text("⏳ چارتەکە شیدەکرێتەوە...")

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
                        "text": "Analyze this Gold chart using Zindan strategy only."
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_base64}"
                    }
                ]
            }
        ]
    )

    result = response.output_text

    await update.message.reply_text(result)