"""
handlers.py
Telegram handlers for SNRZ Bot
"""

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from config import logger
from chat import get_answer


WELCOME_MESSAGE = """
👋 بەخێربێیت بۆ SNRZ Assistant

📚 ئەم بۆتە تەنها لەسەر ستراتیژی SNRZ کار دەکات.

دەتوانیت پرسیار بکەیت، وەک:

• VS چییە؟
• VR چییە؟
• PO2 چییە؟
• SBR چییە؟
• RBS چییە؟
• SRR چییە؟
• RSS چییە؟
• Gap Strategy چییە؟
• False Breakout Area چییە؟
• Money Management چییە؟

✍️ پرسیارەکەت بنووسە.
"""


HELP_MESSAGE = """
📖 SNRZ Assistant Help

/start
دەستپێکردنی بۆت

/help
پیشاندانی یارمەتی

📝 تەنها پرسیارەکانی SNRZ بنووسە.

نمونە:

VS چییە؟
VR چییە؟
PO2 چییە؟
Gap Strategy چییە؟
Money Management چییە؟
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    logger.info(
        "User %s started the bot.",
        update.effective_user.id
    )

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

    if not update.message:
        return

    question = update.message.text.strip()

    logger.info(
        "Question: %s",
        question
    )

    answer = knowledge.search(question)

    await update.message.reply_text(
        answer,
        parse_mode=ParseMode.HTML
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "❌ ئەم فەرمانە ناسراو نییە.\n\n/help"
    )