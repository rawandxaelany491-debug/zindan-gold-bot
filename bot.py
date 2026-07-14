# -*- coding: utf-8 -*-
"""
بۆتی تلیگرامی SNRZ Strategy Assistant.
تەنها بۆ خاوەنی بۆتەکە و ئەو کەسانەی خاوەنەکە ڕێگەی پێداون کاردەکات.
دەتوانێت وەڵامی پرسیار بداتەوە، شیکاری چارت (وێنە، تاک یان چەند
تایمفریم بەیەکەوە) بکات، فەرهەنگی کورتکراوەکان نیشان بدات، مێژووی
سیگناڵەکان بپارێزێت، و ئاگادارکردنەوەی ڕۆژانە بنێرێت.
تەنها بەپێی ستراتیژی SNRZ. (بەکارهێنانی Google Gemini API)
"""

import logging
import os
from datetime import time as dtime
from zoneinfo import ZoneInfo

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

from strategies import SNRZ_SYSTEM_PROMPT, GLOSSARY
from access_control import allow_user, deny_user, is_allowed, list_allowed
import journal

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OWNER_TELEGRAM_ID = int(os.getenv("OWNER_TELEGRAM_ID", "0"))
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Baghdad")
DAILY_REMINDER_HOUR = int(os.getenv("DAILY_REMINDER_HOUR", "9"))
DAILY_REMINDER_MINUTE = int(os.getenv("DAILY_REMINDER_MINUTE", "0"))

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

# بیرگەی کۆمەڵە وێنەکان (بۆ چەند تایمفریمی نێردراو بەیەکەوە/album)
# {media_group_id: {"photos": [bytes,...], "caption": str|None, "user_id":, "chat_id":}}
media_groups: dict[str, dict] = {}
MEDIA_GROUP_DELAY_SECONDS = 2.0


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


def _log_signal_from_reply(user_id: int, reply_text: str) -> None:
    signal = journal.extract_signal(reply_text)
    if signal:
        journal.log_signal(user_id, signal)


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
        "• وێنەی چارتێک (یان چەند تایمفریم بەیەکەوە وەک album) بنێرە "
        "تاکو شیکاری بۆ بکەم بەپێی SNRZ\n\n"
        "فەرمانەکان:\n"
        "/reset — پاککردنەوەی مێژووی گفتوگۆ\n"
        "/glossary — فەرهەنگی کورتکراوەکانی SNRZ\n"
        "/journal — مێژووی سیگناڵەکانی خۆت\n"
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


async def glossary_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not _check_access(user_id):
        await _deny_message(update)
        return

    lines = ["📖 *فەرهەنگی کورتکراوەکانی SNRZ*\n"]
    for term, definition in GLOSSARY.items():
        lines.append(f"*{term}*\n{definition}\n")
    text = "\n".join(lines)

    # تلیگرام سنووری ٤٠٩٦ پیت هەیە بۆ هەر پەیامێک، بۆیە پارچە پارچەی دەکەین
    max_len = 3500
    for i in range(0, len(text), max_len):
        await update.message.reply_text(text[i : i + max_len], parse_mode="Markdown")


async def journal_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not _check_access(user_id):
        await _deny_message(update)
        return

    if context.args and context.args[0] == "all" and user_id == OWNER_TELEGRAM_ID:
        stats = journal.get_all_stats()
        title = "📊 مێژووی هەموو سیگناڵەکان (هەموو بەکارهێنەران)"
    else:
        stats = journal.get_user_stats(user_id)
        title = "📊 مێژووی سیگناڵەکانی تۆ"

    total = sum(stats.values())
    if total == 0:
        await update.message.reply_text("هێشتا هیچ سیگناڵێک تۆمار نەکراوە.")
        return

    text = (
        f"{title}\n\n"
        f"🟢 BUY: {stats['BUY']}\n"
        f"🔴 SELL: {stats['SELL']}\n"
        f"🟡 WAIT: {stats['WAIT']}\n"
        f"━━━━━━━━━\n"
        f"کۆی گشتی: {total}"
    )
    await update.message.reply_text(text)


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

async def _analyze_and_reply(chat_id: int, user_id: int, contents: list, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ناردنی وێنە(کان) بۆ Gemini، وەڵامدانەوە، و تۆمارکردنی سیگناڵ."""
    try:
        response = gemini_model.generate_content(contents)
        reply_text = response.text
    except Exception as e:
        logger.exception("Gemini API vision error")
        await context.bot.send_message(chat_id=chat_id, text=f"⚠️ هەڵەیەک ڕوویدا لە شیکاریکردنی وێنەکە: {e}")
        return

    _log_signal_from_reply(user_id, reply_text)
    await context.bot.send_message(chat_id=chat_id, text=reply_text)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not _check_access(user_id):
        await _deny_message(update)
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    photo = update.message.photo[-1]  # هەرزاترین کوالیتی
    file = await context.bot.get_file(photo.file_id)
    photo_bytes = bytes(await file.download_as_bytearray())

    # ئەگەر ئەم وێنەیە بەشێکە لە album (چەند تایمفریم بەیەکەوە نێردراوە)
    group_id = update.message.media_group_id
    if group_id:
        if group_id not in media_groups:
            media_groups[group_id] = {
                "photos": [],
                "caption": None,
                "user_id": user_id,
                "chat_id": update.effective_chat.id,
            }
            context.job_queue.run_once(
                _process_media_group,
                when=MEDIA_GROUP_DELAY_SECONDS,
                data=group_id,
                name=group_id,
            )
        media_groups[group_id]["photos"].append(photo_bytes)
        if update.message.caption:
            media_groups[group_id]["caption"] = update.message.caption
        return

    caption = update.message.caption or "تکایە ئەم چارتە بەپێی ستراتیژی SNRZ شیکاری بکە."
    contents = [caption, {"mime_type": "image/jpeg", "data": photo_bytes}]
    await _analyze_and_reply(update.effective_chat.id, user_id, contents, context)


async def _process_media_group(context: ContextTypes.DEFAULT_TYPE) -> None:
    """کارپێکردن دوای وەرگرتنی هەموو وێنەکانی album (چەند تایمفریم)."""
    group_id = context.job.data
    data = media_groups.pop(group_id, None)
    if not data or not data["photos"]:
        return

    caption = (
        data["caption"]
        or "ئەمانە چەند تایمفریمی هەمان چارتن. تکایە شیکاریی Multi-Timeframe "
        "بەپێی ستراتیژی SNRZ بکە: یەکەم لە تایمفریمی شیکاری وردببەوە، "
        "دواتر بڕوانە تایمفریمی Confirmation."
    )
    contents = [caption] + [
        {"mime_type": "image/jpeg", "data": p} for p in data["photos"]
    ]
    await _analyze_and_reply(data["chat_id"], data["user_id"], contents, context)


# ───────────────────────── ئاگادارکردنەوەی ڕۆژانە ─────────────────────────

async def _send_daily_reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    recipients = list_allowed() + [OWNER_TELEGRAM_ID]
    text = (
        "🌅 بیرخستنەوەی ڕۆژانە — SNRZ\n\n"
        "کاتی شیکاریکردنی چارتەکانتە! پێش دەستپێکردن بیر لەمانە بکەرەوە:\n"
        "• تایمفریمی شیکاری (Analysis) و Confirmation بەپێی خشتەکە دیاری بکە\n"
        "• ئاگاداری False Breakout Area بە\n"
        "• هەرگیز لە دەرەوەی توانای دارایی خۆت مامەڵە مەکە\n\n"
        "وێنەی چارتێک بنێرە بۆم هەر کاتێک ئامادەیت بۆ شیکاریکردن. 🦁"
    )
    for uid in recipients:
        try:
            await context.bot.send_message(chat_id=uid, text=text)
        except Exception:
            logger.warning("Could not send daily reminder to %s", uid)


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
    app.add_handler(CommandHandler("glossary", glossary_command))
    app.add_handler(CommandHandler("journal", journal_command))
    app.add_handler(CommandHandler("allow", allow_command))
    app.add_handler(CommandHandler("deny", deny_command))
    app.add_handler(CommandHandler("users", users_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    if app.job_queue is not None:
        app.job_queue.run_daily(
            _send_daily_reminder,
            time=dtime(hour=DAILY_REMINDER_HOUR, minute=DAILY_REMINDER_MINUTE, tzinfo=ZoneInfo(TIMEZONE)),
            name="daily_reminder",
        )
    else:
        logger.warning(
            "JobQueue بەردەست نییە — پاکیجی python-telegram-bot[job-queue] دابمەزرێنە "
            "بۆ چالاککردنی ئاگادارکردنەوەی ڕۆژانە."
        )

    logger.info("بۆتی SNRZ دەستیپێکرد...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()