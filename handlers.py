"""
handlers.py
SNRZ Telegram Bot Handlers
"""

from telegram import Update
from telegram.ext import ContextTypes

from knowledge import get_answer


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "👋 بەخێربێیت بۆ SNRZ Telegram Bot\n\n"
        "📚 هەر بابەتێکی SNRZ بنووسە.\n\n"
        "نمونە:\n"
        "• VS\n"
        "• VR\n"
        "• PO2\n"
        "• SBR\n"
        "• RBS\n"
        "• SRR\n"
        "• RSS\n"
        "• GAP\n"
        "• Liquidity Run"
    )

    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📖 تەنها ناوی بابەتەکە بنێرە.\n\n"
        "بۆ نموونە:\n"
        "VS\n"
        "VR\n"
        "PO2"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    question = update.message.text

    answer = get_answer(question)

    if answer:

        if isinstance(answer, dict):
            title = answer.get("title", "")
            content = answer.get("content", "")

            if isinstance(content, list):
                content = "\n".join(f"• {item}" for item in content)

            text = f"📚 {title}\n\n{content}"

        else:
            text = str(answer)

    else:

        text = (
            "❌ ببورە، ئەم بابەتە لە Knowledge Base نەدۆزرایەوە."
        )

    await update.message.reply_text(text)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "❌ ئەم فرمانە ناسراو نییە."
    )