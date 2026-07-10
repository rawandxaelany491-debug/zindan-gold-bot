"""
main.py
SNRZ Telegram Bot
"""

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN, logger
from handlers import (
    start,
    help_command,
    handle_message,
    unknown,
)


def main():

    logger.info("Starting SNRZ Bot...")

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

    # Text Messages
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    # Unknown Commands
    application.add_handler(
        MessageHandler(
            filters.COMMAND,
            unknown,
        )
    )

    logger.info("Bot Started Successfully.")

    application.run_polling(
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()