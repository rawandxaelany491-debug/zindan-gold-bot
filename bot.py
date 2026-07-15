# -*- coding: utf-8 -*-
"""
بۆتی تلیگرامی Trading Strategy Assistant.
تەنها بۆ خاوەنی بۆتەکە و ئەو کەسانەی خاوەنەکە ڕێگەی پێداون کاردەکات.
پشتگیری چەند ستراتیژی دەکات (SNRZ, ICT, SMC) — هەر بەکارهێنەرێک دەتوانێت
بە /strategy یەکێکیان هەڵبژێرێت. دەتوانێت وەڵامی پرسیار بداتەوە، شیکاری
چارت (وێنە، تاک یان چەند تایمفریم بەیەکەوە) بکات، فەرهەنگی کورتکراوەکان
نیشان بدات، مێژووی سیگناڵەکان بپارێزێت، و ئاگادارکردنەوەی ڕۆژانە بنێرێت.
(بەکارهێنانی Claude API ـی Anthropic)
"""

import base64
import logging
import os
from datetime import time as dtime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from anthropic import Anthropic

from strategies import STRATEGIES, DEFAULT_STRATEGY
from access_control import allow_user, deny_user, is_allowed, list_allowed
import journal

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OWNER_TELEGRAM_ID = int(os.getenv("OWNER_TELEGRAM_ID", "0"))
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001")
CLAUDE_MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", "1500"))
TIMEZONE = os.getenv("TIMEZONE", "Asia/Baghdad")
DAILY_REMINDER_HOUR = int(os.getenv("DAILY_REMINDER_HOUR", "9"))
DAILY_REMINDER_MINUTE = int(os.getenv("DAILY_REMINDER_MINUTE", "0"))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

claude_client: "Anthropic" = None  # لە main() پڕدەکرێت

# ستراتیژی چالاکی هەر بەکارهێنەرێک {user_id: strategy_key}
user_strategy: dict[int, str] = {}

# بیرگەی گفتوگۆ بۆ هەر بەکارهێنەرێک، جیاکراوە بەپێی ستراتیژی
# {(user_id, strategy_key): [{"role": "user"/"assistant", "content": ...}, ...]}
conversation_history: dict[tuple, list] = {}
MAX_HISTORY_MESSAGES = 10

# بیرگەی کۆمەڵە وێنەکان (بۆ چەند تایمفریمی نێردراو بەیەکەوە/album)
media_groups: dict[str, dict] = {}
MEDIA_GROUP_DELAY_SECONDS = 2.0


def _get_user_strategy(user_id: int) -> str:
    return user_strategy.get(user_id, DEFAULT_STRATEGY)


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


def _trim_history(key: tuple) -> None:
    history = conversation_history.get(key, [])
    if len(history) > MAX_HISTORY_MESSAGES:
        conversation_history[key] = history[-MAX_HISTORY_MESSAGES:]


def _log_signal_from_reply(user_id: int, reply_text: str) -> None:
    signal = journal.extract_signal(reply_text)
    if signal:
        journal.log_signal(user_id, signal)


def _strategy_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(info["name"], callback_data=f"setstrategy:{key}")]
        for key, info in STRATEGIES.items()
    ]
    return InlineKeyboardMarkup(buttons)


def _generate(strategy_key: str, messages: list) -> str:
    """ناردنی messages بۆ Claude بەپێی system prompt ی ستراتیژیی دیاریکراو."""
    response = claude_client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=CLAUDE_MAX_TOKENS,
        system=STRATEGIES[strategy_key]["system_prompt"],
        messages=messages,
    )
    return "".join(block.text for block in response.content if block.type == "text")


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

    current = STRATEGIES[_get_user_strategy(user_id)]["name"]
    await update.message.reply_text(
        "🦁 بەخێربێیت بۆ بۆتی ستراتیژیەکانی مامەڵەکردن!\n\n"
        f"ستراتیژی چالاکت ئێستا: {current}\n\n"
        "دەتوانیت:\n"
        "• هەر پرسیارێکت هەبێت بمپرسە\n"
        "• وێنەی چارتێک (یان چەند تایمفریم بەیەکەوە وەک album) بنێرە "
        "تاکو شیکاری بۆ بکەم\n\n"
        "فەرمانەکان:\n"
        "/strategy — گۆڕینی ستراتیژی چالاک\n"
        "/reset — پاککردنەوەی مێژووی گفتوگۆ\n"
        "/glossary — فەرهەنگی کورتکراوەکانی ستراتیژی چالاک\n"
        "/journal — مێژووی سیگناڵەکانی خۆت\n"
        "/id — بینینی ئایدی تلیگرامی خۆت",
        parse_mode="Markdown",
    )


async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"ئایدی تلیگرامی تۆ: `{update.effective_user.id}`", parse_mode="Markdown")


async def strategy_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not _check_access(user_id):
        await _deny_message(update)
        return
    current = STRATEGIES[_get_user_strategy(user_id)]["name"]
    await update.message.reply_text(
        f"ستراتیژی چالاکت ئێستا: {current}\n\nستراتیژیەکی نوێ هەڵبژێرە:",
        reply_markup=_strategy_keyboard(),
    )


async def strategy_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    if not _check_access(user_id):
        await query.answer("⛔️ ڕێگەت پێنەدراوە.", show_alert=True)
        return

    strategy_key = query.data.split(":", 1)[1]
    if strategy_key not in STRATEGIES:
        await query.answer("ستراتیژی نەناسراو.", show_alert=True)
        return

    user_strategy[user_id] = strategy_key
    await query.answer(f"✅ گۆڕدرا بۆ {STRATEGIES[strategy_key]['name']}")
    await query.edit_message_text(f"✅ ستراتیژی چالاک ئێستا: {STRATEGIES[strategy_key]['name']}")


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not _check_access(user_id):
        await _deny_message(update)
        return
    strategy_key = _get_user_strategy(user_id)
    conversation_history.pop((user_id, strategy_key), None)
    await update.message.reply_text("✅ مێژووی گفتوگۆ پاک کرایەوە.")


async def glossary_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not _check_access(user_id):
        await _deny_message(update)
        return

    strategy_key = _get_user_strategy(user_id)
    strategy = STRATEGIES[strategy_key]
    lines = [f"📖 *فەرهەنگی کورتکراوەکانی {strategy['name']}*\n"]
    for term, definition in strategy["glossary"].items():
        lines.append(f"*{term}*\n{definition}\n")
    text = "\n".join(lines)

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

    strategy_key = _get_user_strategy(user_id)
    user_text = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    history_key = (user_id, strategy_key)
    history = conversation_history.get(history_key, [])
    history.append({"role": "user", "content": user_text})

    try:
        reply_text = _generate(strategy_key, history)
    except Exception as e:
        logger.exception("Claude API error")
        await update.message.reply_text(f"⚠️ هەڵەیەک ڕوویدا لە پەیوەندیکردن بە Claude: {e}")
        return

    history.append({"role": "assistant", "content": reply_text})
    conversation_history[history_key] = history
    _trim_history(history_key)

    await update.message.reply_text(reply_text)


# ───────────────────────── وێنە (شیکاری چارت) ─────────────────────────

async def _analyze_and_reply(chat_id: int, user_id: int, strategy_key: str, messages: list, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        reply_text = _generate(strategy_key, messages)
    except Exception as e:
        logger.exception("Claude API vision error")
        await context.bot.send_message(chat_id=chat_id, text=f"⚠️ هەڵەیەک ڕوویدا لە شیکاریکردنی وێنەکە: {e}")
        return

    _log_signal_from_reply(user_id, reply_text)
    await context.bot.send_message(chat_id=chat_id, text=reply_text)


def _image_block(photo_bytes: bytes) -> dict:
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/jpeg",
            "data": base64.b64encode(photo_bytes).decode("utf-8"),
        },
    }


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not _check_access(user_id):
        await _deny_message(update)
        return

    strategy_key = _get_user_strategy(user_id)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    photo_bytes = bytes(await file.download_as_bytearray())

    group_id = update.message.media_group_id
    if group_id:
        if group_id not in media_groups:
            media_groups[group_id] = {
                "photos": [],
                "caption": None,
                "user_id": user_id,
                "chat_id": update.effective_chat.id,
                "strategy_key": strategy_key,
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

    caption = update.message.caption or "تکایە ئەم چارتە شیکاری بکە."
    messages = [
        {
            "role": "user",
            "content": [_image_block(photo_bytes), {"type": "text", "text": caption}],
        }
    ]
    await _analyze_and_reply(update.effective_chat.id, user_id, strategy_key, messages, context)


async def _process_media_group(context: ContextTypes.DEFAULT_TYPE) -> None:
    group_id = context.job.data
    data = media_groups.pop(group_id, None)
    if not data or not data["photos"]:
        return

    caption = (
        data["caption"]
        or "ئەمانە چەند تایمفریمی هەمان چارتن. تکایە شیکاریی Multi-Timeframe بکە."
    )
    content = [_image_block(p) for p in data["photos"]] + [{"type": "text", "text": caption}]
    messages = [{"role": "user", "content": content}]
    await _analyze_and_reply(data["chat_id"], data["user_id"], data["strategy_key"], messages, context)


# ───────────────────────── ئاگادارکردنەوەی ڕۆژانە ─────────────────────────

async def _send_daily_reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    recipients = list_allowed() + [OWNER_TELEGRAM_ID]
    text = (
        "🌅 بیرخستنەوەی ڕۆژانە\n\n"
        "کاتی شیکاریکردنی چارتەکانتە! پێش دەستپێکردن:\n"
        "• ستراتیژی چالاکت بپشکنە بە /strategy\n"
        "• هەرگیز لە دەرەوەی توانای دارایی خۆت مامەڵە مەکە\n\n"
        "وێنەی چارتێک بنێرە بۆم هەر کاتێک ئامادەیت بۆ شیکاریکردن. 🦁"
    )
    for uid in recipients:
        try:
            await context.bot.send_message(chat_id=uid, text=text)
        except Exception:
            logger.warning("Could not send daily reminder to %s", uid)


def main() -> None:
    global claude_client

    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN لە .env دیاری نەکراوە.")
    if not ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY لە .env دیاری نەکراوە.")
    if not OWNER_TELEGRAM_ID:
        raise RuntimeError("OWNER_TELEGRAM_ID لە .env دیاری نەکراوە.")

    claude_client = Anthropic(api_key=ANTHROPIC_API_KEY)

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("id", id_command))
    app.add_handler(CommandHandler("strategy", strategy_command))
    app.add_handler(CallbackQueryHandler(strategy_callback, pattern=r"^setstrategy:"))
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
            "JobQueue بەردەست نییە — پاکیجی python-telegram-bot[job-queue] دابمەزرێنە."
        )

    logger.info("بۆت دەستیپێکرد...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()