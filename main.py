"""
main.py

Telegram Bot for XAUUSD (Gold) chart analysis.
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


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=Config.LOG_LEVEL,
)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Start command.
    """

    await update.message.reply_text(
        "👋 بەخێربێیت.\n\n"
        "تکایە تەنها وێنەی TradingView ـی XAUUSD (Gold) بنێرە بۆ شیکردنەوە."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Help command.
    """

    await update.message.reply_text(
        "📌 ئەم بۆتە تەنها چارتی XAUUSD شیدەکاتەوە.\n"
        "وێنەی TradingView بنێرە، من بە ستراتیژی زیندان شیکاری دەکەم."
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle incoming chart image.
    """

    photo = update.message.photo[-1]

    await update.message.reply_text(
        "⏳ چاوەڕێبە...\n"
        "شیکردنەوەی چارت دەکرێت."
    )

    file = await context.bot.get_file(photo.file_id)

    image_path = "chart.png"

    await file.download_to_drive(image_path)

    try:
        with open(image_path, "rb") as f:
    image_bytes = f.read()

result = analyze_chart(image_bytes)

        await update.message.reply_text(result)

    except Exception as e:
        logger.exception(e)

        await update.message.reply_text(
            "❌ هەڵەیەک ڕوویدا لە شیکردنەوەی چارت."
        )

    finally:
        if os.path.exists(image_path):
            os.remove(image_path)

def main():
    """
    Start the Telegram bot.
    """

    Config.validate()

    application = Application.builder().token(
        Config.TELEGRAM_BOT_TOKEN
    ).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            handle_photo,
        )
    )

    logger.info("Bot started...")

    application.run_polling()


if __name__ == "__main__":
    main()