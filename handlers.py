"""
handlers.py
Telegram message handlers for SNRZ Bot
"""

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from config import logger


WELCOME_MESSAGE = """
👋 بەخێربێیت بۆ SNRZ Assistant

ئەم بۆتە تەنها لەسەر ستراتیژی SNRZ وەڵام دەدات.

دەتوانیت پرسیار بکەیت، وەک:

• SBR چییە؟
• RBS چییە؟
• Gap Strategy چییە؟
• Money Management چییە؟

✍️ پرسیارەکەت بنووسە.
"""


HELP_MESSAGE = """
📚 فەرمانەکان

/start
دەستپێکردنی بۆت

/help
پیشاندانی یارمەتی

✍️ هەر پرسیارێکی SNRZ بنووسە.
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        WELCOME_MESSAGE,
        parse_mode=ParseMode.HTML
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        HELP_MESSAGE,
        parse_mode=ParseMode.HTML
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    logger.info(f"Message: {text}")

    await update.message.reply_text(
        "🚧 ئەم بەشە لە فایلەکانی داهاتوو بە Knowledge Base پەیوەست دەکرێت."
    )