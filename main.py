import os
import base64
import logging
from io import BytesIO

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from openai import OpenAI
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found")

client = OpenAI(api_key=OPENAI_API_KEY)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 بەخێربێیت بۆ Gold Analyzer Bot\n\n"
        "📷 تکایە وێنەی چارتی XAUUSD (Gold) بنێرە.\n"
        "🤖 بۆتەکە بە ستراتیژی زیندان شیکاری دەکات.\n"
        "📊 وەڵام: BUY / SELL / NO TRADE"
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("📥 وێنەکەت وەرگیرا...")

        photo = update.message.photo[-1]

        file = await context.bot.get_file(photo.file_id)

        image_bytes = await file.download_as_bytearray()

        image = Image.open(BytesIO(image_bytes))

        buffered = BytesIO()

        image.save(buffered, format="PNG")

        encoded_image = base64.b64encode(
            buffered.getvalue()
        ).decode("utf-8")

        await update.message.reply_text(
            "✅ وێنەکە ئامادەی شیکارییە..."
        )

    except Exception as e:
        logger.exception(e)

        await update.message.reply_text(
            f"❌ هەڵە ڕوویدا:\n{e}"
        )
        async def analyze_chart(encoded_image: str):

    response = client.responses.create(

        model="gpt-4.1",

        input=[

            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "You are an expert XAUUSD chart analyst. "
                            "Describe ONLY what you see in the chart. "
                            "Do not give BUY or SELL signals. "
                            "Extract trend, support, resistance, "
                            "breakout, pullback, candles and market structure."
                        )
                    }
                ]
            },

            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{encoded_image}"
                    }
                ]
            }

        ]

    )

    return response.output_text