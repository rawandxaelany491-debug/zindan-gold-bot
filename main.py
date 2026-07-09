import os
import base64
import logging
from io import BytesIO

from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing.")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing.")

client = OpenAI(api_key=OPENAI_API_KEY)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "👋 Welcome to Gold Analyzer Bot\n\n"
        "📷 Send only XAUUSD (Gold) chart.\n"
        "🤖 The bot will analyze the chart using Zendan Strategy."
    )

    await update.message.reply_text(text)
    async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        await update.message.reply_text(
            "📥 Receiving image..."
        )

        photo = update.message.photo[-1]

        telegram_file = await context.bot.get_file(
            photo.file_id
        )

        image_bytes = await telegram_file.download_as_bytearray()

        image = Image.open(BytesIO(image_bytes))

        buffer = BytesIO()

        image.save(buffer, format="PNG")

        encoded_image = base64.b64encode(
            buffer.getvalue()
        ).decode()

        await update.message.reply_text(
            "🧠 AI is analyzing your Gold chart..."
        )

    except Exception as e:

        logger.exception(e)

        await update.message.reply_text(
            f"❌ Error:\n{e}"
        )
        SYSTEM_PROMPT = """
You are a professional Gold (XAUUSD) chart analyzer.

Analyze ONLY what is visible in the chart.

Return:

Trend:
Support:
Resistance:
Breakout:
Pullback:
Market Structure:
Candlestick Pattern:
Sideway:

Do NOT give BUY or SELL.

Do NOT guess.

Only describe what you clearly see.
"""


async def analyze_image(encoded_image: str):

    response = client.responses.create(

        model="gpt-4.1",

        input=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },

            {
                "role": "user",
                "content": [

                    {
                        "type": "input_text",
                        "text": "Analyze this XAUUSD chart."
                    },

                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{encoded_image}"
                    }

                ]
            }

        ]

    )

    return response.output_text
    async def process_analysis(update, analysis):

    await update.message.reply_text(
        "📊 XAUUSD Analysis:\n\n"
        f"{analysis}"
    )


async def run_photo_analysis(update, context):

    try:
        photo = update.message.photo[-1]

        file = await context.bot.get_file(
            photo.file_id
        )

        image_bytes = await file.download_as_bytearray()

        image = Image.open(BytesIO(image_bytes))

        buffer = BytesIO()
        image.save(buffer, format="PNG")

        encoded_image = base64.b64encode(
            buffer.getvalue()
        ).decode()

        await update.message.reply_text(
            "🧠 Chart is being analyzed..."
        )

        result = await analyze_image(encoded_image)

        await process_analysis(
            update,
            result
        )

    except Exception as e:

        logger.exception(e)

        await update.message.reply_text(
            "❌ Error happened while analyzing chart."
        )


def main():

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            run_photo_analysis
        )
    )

    logger.info(
        "Gold Analyzer Bot Started"
    )

    app.run_polling()


if __name__ == "__main__":
    main()