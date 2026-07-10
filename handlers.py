"""
handlers.py
Telegram handlers for SNRZ Bot
"""

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
)

from config import logger
from knowledge import get_knowledge


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "📚 SNRZ Knowledge",
                callback_data="knowledge"
            )
        ],
        [
            InlineKeyboardButton(
                "📊 SNRZ Chart Analysis",
                callback_data="chart"
            )
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🤖 Welcome to SNRZ Bot\n\n"
        "Choose a section:",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n\n"
        "/start - Start bot\n"
        "/help - Help menu"
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "knowledge":
        keyboard = [
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="back"
                )
            ]
        ]

        await query.edit_message_text(
            "📚 SNRZ Knowledge\n\n"
            "VS\n"
            "VR\n"
            "PO2\n"
            "More SNRZ concepts coming...",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    elif query.data == "chart":
        keyboard = [
            [
                InlineKeyboardButton(
                    "📷 Upload Chart",
                    callback_data="upload_chart"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="back"
                )
            ]
        ]

        await query.edit_message_text(
            "📊 SNRZ Chart Analysis\n\n"
            "Upload your chart for analysis.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    elif query.data == "back":
        keyboard = [
            [
                InlineKeyboardButton(
                    "📚 SNRZ Knowledge",
                    callback_data="knowledge"
                )
            ],
            [
                InlineKeyboardButton(
                    "📊 SNRZ Chart Analysis",
                    callback_data="chart"
                )
            ],
        ]

        await query.edit_message_text(
            "🤖 SNRZ Bot Menu",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    elif query.data == "upload_chart":
        await query.edit_message_text(
            "📷 Please upload your chart image.\n\n"
            "Chart analysis module will be connected soon."
        )


def register_handlers(application):

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    logger.info("Handlers registered successfully")