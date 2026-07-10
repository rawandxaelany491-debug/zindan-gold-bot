"""
handlers.py
Telegram handlers for SNRZ Bot
"""

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from config import logger
from knowledge import knowledge


WELCOME_MESSAGE = """
👋 Welcome to SNRZ Assistant

Choose one of the services below.
"""


HELP_MESSAGE = """
📖 SNRZ Assistant

/start - Main Menu
/help - Help
"""


CHART_ANALYSIS_MESSAGE = """
━━━━━━━━━━━━━━━━━━━━
📊 SNRZ CHART ANALYSIS
━━━━━━━━━━━━━━━━━━━━

👋 Welcome to the SNRZ Analysis System.

Upload your Gold (XAUUSD) chart and receive a complete technical analysis based exclusively on the official SNRZ Strategy.

━━━━━━━━━━━━━━━━━━━━
📌 WHAT YOU WILL RECEIVE
━━━━━━━━━━━━━━━━━━━━

📈 Market Trend

📍 Valid Support (VS)

📍 Valid Resistance (VR)

📍 I.VS

📍 I.VR

🔄 SBR

🔄 RBS

🔄 SRR

🔄 RSS

⚡ PO2

⚡ PO2 Inversion

⚡ Gap Strategy

⚡ False Breakout Area

⚡ Liquidity Run

⚡ Liquidity Sweep

🎯 Entry Zone

🎯 Confirmation

🎯 Stop Loss

🎯 Take Profit

🎯 Risk / Reward

🎯 Probability

🎯 Money Management

━━━━━━━━━━━━━━━━━━━━
📷 CHART REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━

✅ Gold (XAUUSD)

✅ Clean Screenshot

✅ Timeframe Visible

✅ High Quality Image

━━━━━━━━━━━━━━━━━━━━
📤 READY TO ANALYZE
━━━━━━━━━━━━━━━━━━━━

Please upload your chart to begin the SNRZ analysis.
"""


def main_menu():

    keyboard = [
        [
            InlineKeyboardButton(
                "📚 SNRZ Knowledge",
                callback_data="knowledge",
            )
        ],
        [
            InlineKeyboardButton(
                "📊 SNRZ Chart Analysis",
                callback_data="analysis",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def analysis_menu():

    keyboard = [
        [
            InlineKeyboardButton(
                "📷 Upload Chart",
                callback_data="upload_chart",
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="back",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    logger.info(
        "User %s started the bot.",
        update.effective_user.id,
    )

    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=main_menu(),
        parse_mode=ParseMode.HTML,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        HELP_MESSAGE,
        parse_mode=ParseMode.HTML,
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "knowledge":

        await query.edit_message_text(
            "📚 SNRZ Knowledge\n\n"
            "Write any SNRZ question.\n\n"
            "Examples:\n"
            "• VS\n"
            "• VR\n"
            "• PO2\n"
            "• Gap Strategy\n"
            "• Money Management",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 Back",
                            callback_data="back",
                        )
                    ]
                ]
            ),
        )

    elif query.data == "analysis":

        await query.edit_message_text(
            CHART_ANALYSIS_MESSAGE,
            reply_markup=analysis_menu(),
        )

    elif query.data == "upload_chart":

        await query.edit_message_text(
            "📷 Please upload your Gold (XAUUSD) chart.\n\n"
            "Chart analysis will be available in the next step.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 Back",
                            callback_data="back",
                        )
                    ]
                ]
            ),
        )

    elif query.data == "back":

        await query.edit_message_text(
            WELCOME_MESSAGE,
            reply_markup=main_menu(),
        )
        async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    question = update.message.text.strip()

    logger.info(
        "Question: %s",
        question,
    )

    answer = knowledge.search(question)

    await update.message.reply_text(
        answer,
        parse_mode=ParseMode.HTML,
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "❌ Unknown command.\n\nUse /start"
    )