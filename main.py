import os
import logging
import io
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# بارکردنی کلیلەکان لە ژینگە (Environment Variables)
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ڕێکخستنی لۆگ بۆ بینینی هەڵەکان لە کۆنسۆل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- پێکهێنانی Gemini (تەنها ئەگەر کلیلی هەبێت) ---
GEMINI_AVAILABLE = False
if GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        GEMINI_AVAILABLE = True
        logger.info("✅ Gemini پێکهێنرا و ئامادەیە!")
    except Exception as e:
        logger.error(f"❌ هەڵە لە پێکهێنانی Gemini: {e}")
else:
    logger.warning("⚠️ کلیلی Gemini نەدۆزرایەوە. شیکاری وێنە ناکارێت.")

# --- فەرمانی /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = (
        "🎯 **بەخێربێیت بۆ بۆتی پێشکەوتووی SNRZ!**\n\n"
        "📊 **فەرمانەکان:**\n"
        "/sbr - شکاندنی پاڵپشتی بۆ بەرگری (ئاماژەی فرۆشتن)\n"
        "/rbs - شکاندنی بەرگری بۆ پاڵپشتی (ئاماژەی کڕین)\n"
        "/po2 - هێزی دەست لێدانی دووەم\n"
        "/gap - ستراتیژی بۆشایی (Gap)\n"
        "/risk - بەڕێوەبردنی مەترسی\n\n"
        "🖼️ **تایبەتمەندیی نوێ:** وێنەی چارتێک بنێرە بۆم، ئەوا Gemini AI شیکاری دەکات و پێت دەڵێت کە شێوازی SNRZ تیا هەیە!"
    )
    await update.message.reply_text(welcome, parse_mode="Markdown")

# --- فەرمانی /help ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 **ڕێنمایی:**\n\n"
        "1. فەرمانەکان بەکاربهێنە بۆ زانینی پێناسەی هەر تۆپیکێک.\n"
        "2. وێنەیەکی چارت (لە تریڤیو یان MT5) بۆ بۆتەکە بنێرە.\n"
        "3. بۆتەکە بە Gemini شیکاری دەکات و پێت دەڵێت: SBR، RBS، PO2، GAP یان هیچ.",
        parse_mode="Markdown"
    )

# --- فەرمانە ڕاستەوخۆکانی SNRZ ---
async def sbr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📉 **SBR (Support Breakout to Resistance)**\n\nپاڵپشتی شکا → بوو بە بەرگری\nئاماژە: فرۆشتن (SELL)\nچاوەڕێی پاشەکشە بکە.",
        parse_mode="Markdown"
    )

async def rbs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📈 **RBS (Resistance Breakout to Support)**\n\nبەرگری شکا → بوو بە پاڵپشتی\nئاماژە: کڕین (BUY)\nچاوەڕێی پاشەکشە بکە.",
        parse_mode="Markdown"
    )

async def po2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚡ **PO2 (Power Of Second Touch)**\n\nبەهێزترین تۆپیک! دووەم دەست لێدان بە مارکێتدا زۆر بەهێزە.",
        parse_mode="Markdown"
    )

async def gap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🕳️ **Gap Strategy**\n\nمارکێت ٨٠٪ مەیلی پڕکردنەوەی بۆشایی (Gap) هەیە.",
        parse_mode="Markdown"
    )

async def risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡️ **بەڕێوەبردنی مەترسی**\n\nسەرمایە بپارێزە! ئەکاونتی سەنت بەکاربهێنە و بە قازانجەکەت بۆ تارگێتی دووەم ڕیسک بکە.",
        parse_mode="Markdown"
    )

# --- مامەڵەکردن لەگەڵ وێنەکان (Gemini Integration) ---
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not GEMINI_AVAILABLE:
        await update.message.reply_text("⚠️ ببورە، کلیلی Gemini دیاری نەکراوە. تکایە GEMINI_API_KEY لە Variablesـی Railway دابنێ.")
        return

    # ناردنی پەیامی چاوەڕوانی
    await update.message.reply_text("🔄 تکایە چاوەڕێ بکە، وێنەکە دەگوازینەوە بۆ Gemini بۆ شیکاری...")

    try:
        # وەرگرتنی وێنەی باڵاترین کوالیتی
        photo_file = await update.message.photo[-1].get_file()
        # دابەزاندنی وێنە بۆ بیرگە
        image_bytes = await photo_file.download_as_bytearray()

        # پێکهێنانی مۆدێلی Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # پرۆمپتەکە بە زمانی کوردی و تایبەت بە SNRZ
        prompt = """
        تۆ پسپۆڕی ستراتیژی SNRZ ی. ئەم وێنەیە چارتێکی بازرگانییە.
        تکایە وردبینی بکە و بە کوردی (سۆرانی) پێم بڵێ:
        1. ئایا شێوازی SBR (شکاندنی پاڵپشتی) تیادایە؟
        2. ئایا شێوازی RBS (شکاندنی بەرگری) تیادایە؟
        3. ئایا شێوازی PO2 (دەست لێدانی دووەم) یان GAP (بۆشایی) تیادایە؟
        4. ئاستی پاڵپشتی و بەرگرییە سەرەکییەکان دەستنیشان بکە.

        وەڵامەکەت کورت و پوخت بێت، تەنها خاڵە گرنگەکان بنووسە، لە ٥ ڕستە زیاتر مەبە.
        """

        # ناردنی داواکاری بۆ Gemini
        response = model.generate_content([prompt, image_bytes])
        
        # دەرهێنانی وەڵام
        analysis = response.text
        
        # ناردنی وەڵامەکە بۆ بەکارهێنەر
        await update.message.reply_text(
            f"🤖 **شیکاری Gemini:**\n\n{analysis}",
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logger.error(f"هەڵەی Gemini: {e}")
        await update.message.reply_text("❌ ببورە، لە شیکاری وێنەکەدا کێشە ڕوویدا. تکایە دووبارە هەوڵبدەرەوە یان وێنەیەکی تر بنێرە.")

# --- وەڵامدانەوەی پەیامی ئاسایی (ئەگەر فەرمان نەبێت) ---
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📩 پەیامەکەت: {update.message.text}\n"
        "تکایە فەرمانێک بنێرە، یان وێنەیەکی چارت بنێرە بۆ شیکاری."
    )

# --- فەرمانی سەرەکی بۆ جێبەجێکردن ---
def main():
    if not BOT_TOKEN:
        logger.error("❌ تۆکنی بۆت نەدۆزرایەوە! لە Variablesـی Railwayدا BOT_TOKEN دابنێ.")
        return

    logger.info("🚀 بۆتەکە دەستپێدەکات...")
    app = Application.builder().token(BOT_TOKEN).build()

    # زیادکردنی هەموو فەرمانەکان
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("sbr", sbr))
    app.add_handler(CommandHandler("rbs", rbs))
    app.add_handler(CommandHandler("po2", po2))
    app.add_handler(CommandHandler("gap", gap))
    app.add_handler(CommandHandler("risk", risk))
    
    # زیادکردنی مامەڵەکەر بۆ وێنەکان
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    # زیادکردنی مامەڵەکەر بۆ تێکست (دوای هەموو فەرمانەکان)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("✅ بۆتی SNRZ بە Gemini کاردەکات! چاوەڕێی پەیام بن.")
    app.run_polling()

if __name__ == "__main__":
    main()