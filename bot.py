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
    text = (
        "👋 بەخێربێیت بۆ SNRZ Assistant Bot\n\n"
        "📚 ئەم بۆتە تەنها پرسیارەکانی ستراتیژی SNRZ وەڵام دەدات.\n\n"
        "نمونە:\n"
        "• PO2 چییە؟\n"
        "• RBS چییە؟\n"
        "• Liquidity Sweep چییە؟\n"
        "• Gap Strategy چییە؟"
    )

    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "پرسیارەکانت بە زمانی کوردی بنێرە.\n"
        "ئەگەر لە زانیارییەکانی SNRZ هەبێت، بۆتەکە وەڵام دەدات."
    )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    answer = search_snrz(user_text)

    await update.message.reply_text(answer)


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler,
        )
    )

    print("Bot Started...")

    application.run_polling()


if __name__ == "__main__":
    main()