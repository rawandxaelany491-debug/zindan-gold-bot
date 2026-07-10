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

    logger.info("Starting SNRZ Telegram Bot...")

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Messages
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    # Unknown Commands
    app.add_handler(
        MessageHandler(
            filters.COMMAND,
            unknown,
        )
    )

    logger.info("Bot Started Successfully.")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()