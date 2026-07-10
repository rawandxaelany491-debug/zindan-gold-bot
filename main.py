"""
main.py
SNRZ Telegram Bot
Production Ready
"""

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from config import BOT_TOKEN, logger
from handlers import (
    start,
    help_command,
    button_handler,
)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):

    logger.exception(
        "Unhandled Exception:",
        exc_info=context.error,
    )

    if isinstance(update, Update):
        if update.effective_message:
            await update.effective_message.reply_text(
                "❌ هەڵەیەک ڕوویدا، تکایە دووبارە هەوڵ بدە."
            )


def main():

    logger.info("Starting SNRZ Telegram Bot...")

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # Commands
    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    # Inline Buttons
    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    # Errors
    application.add_error_handler(
        error_handler
    )

    logger.info("Bot Started Successfully.")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()