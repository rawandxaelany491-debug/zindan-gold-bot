import os
import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from search import search_snrz

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 بەخێربێیت بۆ SNRZ Assistant Bot.\n\n"
        "پرسیارەکانت دەربارەی ستراتیژی SNRZ بنێرە."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "نمونەی پرسیار:\n"
        "• PO2 چییە؟\n"
        "• RBS چییە؟\n"
        "• Gap Strategy چییە؟"
    )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    answer = search_snrz(update.message.text)
    await update.message.reply_text(answer)


def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN not found!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)
    )

    print("✅ Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()