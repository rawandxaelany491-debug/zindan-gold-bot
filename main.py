import os
import logging
from dotenv import load_dotenv

from telegram import Update, InputFile
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

📚 من فێرکارییەکانی ستراتیژی SNRZ وەڵام دەدەم.

━━━━━━━━━━━━━━

📖 تۆپیکەکان

S   → Support
R   → Resistance

VS  → Valid Support
VR  → Valid Resistance

IVS → Inversion Valid Support
IVR → Inversion Valid Resistance

P   → PO2
PI  → PO2 Inversion

RB  → RBS
SB  → SBR

SR  → SRR
RS  → RSS

LS  → Liquidity Sweep
LR  → Liquidity Run

PBP → Pump Base Pump
DBD → Dump Base Dump

G   → Gap Strategy

FB  → False Breakout

T   → Trend

TF  → Timeframe Confirmation

MM  → Money Management

━━━━━━━━━━━━━━

✍️ تەنها کورتکراوەکە بنێرە.

نمونە:

S
R
VS
P
RB
G
MM
"""

    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "پرسیارەکانت لەسەر SNRZ بنێرە.\n"
        "نموونە: S، R، VS، PO2، RB، MM"
    )
    async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    result = search_snrz(user_text)

    if isinstance(result, dict):

        image_name = result.get("image")
        text = result.get("text")

        if image_name:

            image_path = os.path.join("images", image_name)

            if os.path.exists(image_path):

                await update.message.reply_photo(
                    photo=InputFile(image_path),
                    caption=text
                )
                return

        await update.message.reply_text(text)
        return

    await update.message.reply_text(result)


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

    print("✅ SNRZ Bot Started...")

    application.run_polling()


if __name__ == "__main__":
    main()