"""
main.py
"""

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

from config import Config
from analysis import analyze_chart
from chat import chat_with_ai

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 بەخێربێیت بۆ SNRZ AI Bot.\n\n"
        "📷 وێنەی TradingView ـی XAUUSD بنێرە بۆ شیکردنەوە.\n"
        "💬 یان هەر پرسیارێکت لەسەر SNRZ هەیە بنووسە."
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]

        telegram_file = await context.bot.get_file(photo.file_id)

        image_path = "chart.png"

        await telegram_file.download_to_drive(image_path)

        with open(image_path, "rb") as f:
            image_bytes = f.read()

        os.remove(image_path)

        await update.message.reply_text(
            "⏳ چاوەڕێبە... شیکردنەوە دەکرێت."
        )

        result = analyze_chart(image_bytes)

        await update.message.reply_text(result)

    except Exception as e:
        logger.exception(e)

        await update.message.reply_text(
            f"❌ Error:\n{e}"
        )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_message = update.message.text

        await update.message.reply_text(
            "💬 چاوەڕێبە..."
        )

        result = chat_with_ai(user_message)

        await update.message.reply_text(result)

    except Exception as e:
        logger.exception(e)

        await update.message.reply_text(
            f"❌ Error:\n{e}"
        )


def main():

    Config.validate()

    app = (
        Application.builder()
        .token(Config.TELEGRAM_BOT_TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            handle_photo,
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text,
        )
    )

    logger.info("Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()