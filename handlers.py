"""
handlers.py
Telegram handlers for SNRZ Bot
"""

from telegram import Update
from telegram.ext import ContextTypes

from knowledge import get_answer


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to SNRZ Bot!\n\n"
        "Type a keyword like:\n"
        "- VS\n"
        "- VR\n"
        "- PO2\n"
        "- SBR\n"
        "- RBS"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 SNRZ Bot Help\n\n"
        "Use /start to begin.\n"
        "Send any SNRZ keyword to get its explanation."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    answer = get_answer(text)

    if answer:
        await update.message.reply_text(answer)
    else:
        await update.message.reply_text(
            "❌ Sorry, I don't know that SNRZ term yet."
        )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Unknown command."
    )