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
    text = """
👋 بەخێربێیت بۆ SNRZ Assistant Bot

📚 من تەنها پرسیارەکانی ستراتیژی SNRZ وەڵام دەدەم.

دەتوانیت دەربارەی ئەم بابەتانە پرسیار بکەیت:

• Support (S)
• Resistance (R)
• Valid Support (VS)
• Valid Resistance (VR)
• Inversion VS
• Inversion VR
• RBS
• SBR
• SRR
• RSS
• PO2 (Power Of Second Touch)
• PO2 Inversion
• Liquidity Sweep
• Liquidity Run
• Pump Base Pump
• Dump Base Dump
• Gap Strategy
• False Breakout Area
• Fresh Zones
• Trend
• Trend Ranking
• Timeframe Confirmation
• Valid Zones
• Zone Types
• Money Management

✍️ پرسیارت لە کام بابەتە هەیە؟
"""

    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "پرسیارەکانت دەربارەی SNRZ بنێرە، من وەڵامیان دەدەم."
    )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    answer = search_snrz(user_text)

    await update.message.reply_text(answer)


def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN نەدۆزرایەوە.")

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler,
        )
    )

    print("✅ Bot Started...")

    application.run_polling()


if __name__ == "__main__":
    main()