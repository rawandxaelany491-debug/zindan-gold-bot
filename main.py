"""
main.py

Telegram Bot for SNRZ AI
"""

import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from analysis import analyze_chart
from chat import chat_with_ai
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 بەخێربێیت بۆ SNRZ AI Bot\n\n"
        "📷 وێنەی چارتی XAUUSD لە TradingView بنێرە.\n"
        "💬 یان پرسیارێکت لەسەر SNRZ بنووسە."
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            "⏳ شیکردنەوە دەکرێت..."
        )

        photo = update.message.photo[-1]

        file = await context.bot.get_file(photo.file_id)

        image_bytes = await file.download_as_bytearray()

        result = analyze_chart(bytes(image_bytes))

        await update.message.reply_text(result)

    except Exception as e:
        logger.exception(e)

        await update.message.reply_text(
            "❌ هەڵەیەک ڕوویدا."
        )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            "💬 چاوەڕێبە..."
        )

        result = chat_with_ai(update.message.text)

        await update.message.reply_text(result)

    except Exception as e:
        logger.exception(e)

        await update.message.reply_text(
            "❌ هەڵەیەک ڕوویدا."
        )


def main():

    Config.validate()

    app = (
        Application.builder()
        .token(Config.TELEGRAM_BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

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

    logger.info("✅ SNRZ Bot Started")

    app.run_polling()


if __name__ == "__main__":
    main()