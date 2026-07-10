"""
handlers.py
"""

from telegram import Update
from telegram.ext import ContextTypes

from knowledge import get_answer


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 بەخێربێیت بۆ SNRZ Bot\n\n"
        "هەر بابەتێکی SNRZ بنووسە.\n\n"
        "بۆ نموونە:\n"
        "VS\n"
        "VR\n"
        "PO2\n"
        "SBR\n"
        "RBS\n"
        "RSS\n"
        "SRR\n"
        "Gap\n"
        "Liquidity Run"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📚 تەنها ناوی بابەتەکە بنێرە."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    answer = get_answer(text)

    await update.message.reply_text(answer)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "❌ فرمانەکە ناسراو نییە."
    )