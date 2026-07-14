# -*- coding: utf-8 -*-
"""
بۆتی تلیگرامی SNRZ Strategy Assistant.
تەنها بۆ خاوەنی بۆتەکە و ئەو کەسانەی خاوەنەکە ڕێگەی پێداون کاردەکات.
دەتوانێت وەڵامی پرسیار بداتەوە و شیکاری چارت (وێنە) بکات، هەردووکیان
تەنها بەپێی ستراتیژی SNRZ. (بەکارهێنانی Google Gemini API)
"""

import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import google.generativeai as genai

from strategies import SNRZ_SYSTEM_PROMPT
from access_control import allow_user, deny_user, is_allowed, list_allowed

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OWNER_TELEGRAM_ID = int(os.getenv("OWNER_TELEGRAM_ID", "0"))
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

gemini_model = None  # لە main() دروست دەکرێت دوای پشکنینی کلیلەکە

# بیرگەی گفتوگۆ بۆ هەر بەکارهێنەرێک (تەنها لە کاتی کارپێکردنی بۆت، لە مێمۆری)
# {user_id: [{"role": "user"/"model", "parts": [text]}, ...]}
conversation_history: dict[int, list] = {}
MAX_HISTORY_MESSAGES = 10  # چەند پەیامی دوایی بیر بهێنرێتەوە


def _check_access(user_id: int) -> bool:
    return is_allowed(user_id, OWNER_TELEGRAM_ID)


async def _deny_message(update: Update) -> None:
    user_id = update.effective_user.id
    await update.message.reply_text(
        f"⛔️ ببورە، تۆ ڕێگەت پێنەدراوە بۆ بەکارهێنانی ئەم بۆتە.\n"
        f"ئایدی تۆ: `{user_id}`\n"
        f"تکایە پەیوەندی بە خاوەنی بۆتەکەوە بکە بۆ وەرگرتنی ڕێگە.",
        parse_mode="Markdown",
    )


def _trim_history(user_id: int) -> None:
    history = conversation_history.get(user_id, [])
    if len(history) > MAX_HISTORY_MESSAGES:
        conversation_history[user_id] = history[-MAX_HISTORY_MESSAGES:]


# ───────────────────────── فەرمانەکان ─────────────────────────

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not _check_access(user_id):
        await update.message.reply_text(
            f"⛔️ ببورە، تۆ ڕێگەت پێنەدراوە بۆ بەکارهێنانی ئەم بۆتە.\n"
            f"ئایدی تۆ: `{user_id}`\n"
            f"تکایە ئەم ئایدییە بنێرە بۆ خاوەنی بۆتەکە بۆ وەرگرتنی ڕێگە.",
            parse_mode="Markdown",
        )
        return

    await update.message.reply_text(
        "🦁 بەخێربێیت بۆ بۆتی ستراتیژی *SNRZ*!\n\n"
        "دەتوانیت:\n"
        "• هەر پرسیارێکت هەبێت لەسەر ستراتیژی SNRZ بمپرسە\n"
        "• وێنەی چارتێک بنێرە تاکو شیکاری بۆ بکەم بەپێی SNRZ\n\n"
        "فەرمانەکان:\n"
        "/reset — پاککردنەوەی مێژووی گفتوگۆ\n"
        "/id — بینینی ئایدی تلیگرامی خۆت",
        parse_mode="Markdown",
    )


async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"ئایدی تلیگرامی تۆ: `{update.effective_user.id}`", parse_mode="Markdown")


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not _check_access(user_id):
        await _deny_message(update)
        return
    conversation_history.pop(user_id, None)
    await update.message.reply_text("✅ مێژووی گفتوگۆ پاک کرایەوە.")


async def allow_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """تەنها خاوەنی بۆت دەتوانێت ڕێگە بە کەسی تر بدات. بەکارهێنان: /allow <user_id>"""
    user_id = update.effective_user.id
    if user_id != OWNER_TELEGRAM_ID:
        await update.message.reply_text("⛔️ تەنها خاوەنی بۆت دەتوانێت ئەم فەرمانە بەکاربهێنێت.")
        return

    if not context.args:
        await update.message.reply_text("بەکارهێنان: /allow <telegram_user_id>")
        return

    try:
        target_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("تکایە ئایدییەکی دروست بنێرە (ژمارە).")
        return

    if allow_user(target_id):
        await update.message.reply_text(f"✅ ئایدی `{target_id}` ڕێگەی پێدرا.", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"ئایدی `{target_id}` پێشتر ڕێگەی پێدراوە.", parse_mode="Markdown")


async def deny_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """تەنها خاوەنی بۆت دەتوانێت ڕێگە لە کەسێک بسەنێتەوە. بەکارهێنان: /deny <user_id>"""
    user_id = update.effective_user.id
    if user_id != OWNER_TELEGRAM_ID:
        await update.message.reply_text("⛔️ تەنها خاوەنی بۆت دەتوانێت ئەم فەرمانە بەکاربهێنێت.")
        return

    if not context.args:
        await update.message.reply_text("بەکارهێنان: /deny <telegram_user_id>")
        return

    try:
        target_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("تکایە ئایدییەکی دروست بنێرە (ژمارە).")
        return

    if deny_user(target_id):
        await update.message.reply_text(f"✅ ڕێگەی ئایدی `{target_id}` سەنرایەوە.", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"ئایدی `{target_id}` لە لیستدا نەبوو.", parse_mode="Markdown")


async def users_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """تەنها خاوەنی بۆت دەتوانێت لیستی ڕێگەپێدراوان ببینێت."""
    user_id = update.effective_user.id
    if user_id != OWNER_TELEGRAM_ID:
        await update.message.reply_text("⛔️ تەنها خاوەنی بۆت دەتوانێت ئەم فەرمانە بەکاربهێنێت.")
        return

    allowed = list_allowed()
    if not allowed:
        await update.message.reply_text("هیچ کەسێک ڕێگەی پێنەدراوە جگە لە خۆت (خاوەن).")
        return

    text = "👥 ئایدییە ڕێگەپێدراوەکان:\n" + "\n".join(f"• `{uid}`" for uid in allowed)
    await update.message.reply_text(text, parse_mode="Markdown")


# ───────────────────────── پەیامی نووسراو ─────────────────────────

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not _check_access(user_id):
        await _deny_message(update)
        return

    user_text = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    history = conversation_history.get(user_id, [])
    history.append({"role": "user", "parts": [user_text]})

    try:
        response = gemini_model.generate_content(history)
        reply_text = response.text
    except Exception as e:
        logger.exception("Gemini API error")
        await update.message.reply_text(f"⚠️ هەڵەیەک ڕوویدا لە پەیوەندیکردن بە Gemini: {e}")
        return

    history.append({"role": "model", "parts": [reply_text]})
    conversation_history[user_id] = history
    _trim_history(user_id)

    await update.message.reply_text(reply_text)


# ───────────────────────── وێنە (شیکاری چارت) ─────────────────────────

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not _check_access(user_id):
        await _deny_message(update)
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    photo = update.message.photo[-1]  # هەرزاترین کوالیتی
    file = await context.bot.get_file(photo.file_id)
    photo_bytes = bytes(await file.download_as_bytearray())

    caption = update.message.caption or "تکایە ئەم چارتە بەپێی ستراتیژی SNRZ شیکاری بکە."

    try:
        response = gemini_model.generate_content(
            [caption, {"mime_type": "image/jpeg", "data": photo_bytes}]
        )
        reply_text = response.text
    except Exception as e:
        logger.exception("Gemini API vision error")
        await update.message.reply_text(f"⚠️ هەڵەیەک ڕوویدا لە شیکاریکردنی وێنەکە: {e}")
        return

    await update.message.reply_text(reply_text)


def main() -> None:
    global gemini_model

    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN لە .env دیاری نەکراوە.")
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY لە .env دیاری نەکراوە.")
    if not OWNER_TELEGRAM_ID:
        raise RuntimeError("OWNER_TELEGRAM_ID لە .env دیاری نەکراوە.")

    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=SNRZ_SYSTEM_PROMPT,
    )

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("id", id_command))
    app.add_handler(CommandHandler("reset", reset_command))
    app.add_handler(CommandHandler("allow", allow_command))
    app.add_handler(CommandHandler("deny", deny_command))
    app.add_handler(CommandHandler("users", users_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("بۆتی SNRZ دەستیپێکرد...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()