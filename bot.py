from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import Config
from analysis import analyze_chart


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 بەخێربێیت.\n\n"
        "تکایە تەنها وێنەی TradingView بۆ XAUUSD (Gold) بنێرە."
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]

        telegram_file = await context.bot.get_file(photo.file_id)

        image_bytes = await telegram_file.download_as_bytearray()

        await update.message.reply_text("⏳ چاوەڕێبە... شیکردنەوەی چارت دەکرێت.")

        result = analyze_chart(bytes(image_bytes))

        await update.message.reply_text(result)

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error:\n{str(e)}"
        )


def main():
    app = Application.builder().token(
        Config.TELEGRAM_BOT_TOKEN
    ).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            handle_photo,
        )
    )

    print("✅ Bot Started")

    app.run_polling()


if __name__ == "__main__":
    main()