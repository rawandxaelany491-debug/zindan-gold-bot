from telegram import Update
from telegram.ext import ContextTypes

from knowledge import get_answer
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    question = update.message.text.strip()

    answer = get_answer(question)

    if answer:

        title = answer.get("title", "")

        content = answer.get("content", "")

        if isinstance(content, list):
            content = "\n".join(f"• {line}" for line in content)

        text = (
            f"📚 {title}\n"
            f"{'─'*25}\n\n"
            f"{content}"
        )

    else:

        text = (
            "❌ ئەم بابەتە لە Knowledge Base نەدۆزرایەوە.\n\n"
            "نمونە:\n"
            "• VS\n"
            "• VR\n"
            "• PO2\n"
            "• GAP\n"
            "• Money Management"
        )

    if len(text) > 4000:
        for i in range(0, len(text), 4000):
            await update.message.reply_text(text[i:i+4000])
    else:
        await update.message.reply_text(text)