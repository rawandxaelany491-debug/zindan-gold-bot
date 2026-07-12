import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import Config
from snrz_analyzer import SNRZAnalyzer
from image_processor import ImageProcessor
from github_manager import GitHubManager
import os
import json

# ڕێکخستنی لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SNRZBot:
    def __init__(self):
        self.analyzer = SNRZAnalyzer()
        self.image_processor = ImageProcessor()
        self.github = GitHubManager(Config.GITHUB_TOKEN, Config.GITHUB_REPO)
        self.user_sessions = {}
        self.bot = None
        
    def run(self):
        """ڕانکردنی بۆتەکە"""
        application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        self.bot = application.bot
        
        # کۆماندەکان
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("analyze", self.analyze_command))
        application.add_handler(CommandHandler("history", self.history_command))
        application.add_handler(CommandHandler("topics", self.topics_command))
        application.add_handler(CommandHandler("signal", self.signal_command))
        
        # هەڵگرتنی وێنە
        application.add_handler(MessageHandler(filters.PHOTO, self.handle_image))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        
        # کۆماندەکانی کلیلە
        application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # ڕانکردن
        print("🚀 بۆتی SNRZ ڕان دەکرێت...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """کۆماندی /start"""
        user = update.effective_user
        welcome_text = f"""
👋 **بەخێربێیت {user.first_name}!**

من **بۆتی SNRZ**ـم، بۆتێکی تایبەت بە شیکاری ستراتیژی **ZiNDAN THE GOLD CHASER**.

📚 **تواناکانم:**
• شیکاری چارت و زۆنەکان (VS, VR, SBR, RBS, SRR, RSS, PO2, GAP)
• وەڵامدانەوەی پرسیارە تایبەتییەکانی SNRZ
• ناسینی شێوەکانی SNRZ لە وێنەکان
• پاشکەوتکردنی شیکاریەکان لە GitHub

📌 **بەکارهێنان:**
• وێنەی چارتی خۆت بنێرە بۆ شیکاری
• /analyze - شیکاری چارت
• /topics - هەموو تۆپیکەکانی SNRZ
• /signal - دۆزینەوەی سیگناڵ
• /history - مێژووی شیکاریەکان

✨ **ئامانج**: یارمەتیدانی تەرەیدەرانی SNRZ بۆ باشتر تێگەیشتن و شیکاری بازاڕ!
"""
        keyboard = [
            [InlineKeyboardButton("📊 شیکاری چارت", callback_data="analyze")],
            [InlineKeyboardButton("📚 تۆپیکەکان", callback_data="topics")],
            [InlineKeyboardButton("📈 سیگناڵ", callback_data="signal")],
            [InlineKeyboardButton("📖 ڕاهێنان", callback_data="tutorial")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """کۆماندی /help"""
        help_text = """
❓ **چۆن بۆتەکە بەکاربهێنم؟**

**1. شیکاری وێنە:**
وێنەی چارتی خۆت بنێرە، من هەموو زۆن و شێوەکانی SNRZ دەناسێنم.

**2. کۆماندەکان:**
• /start - دەستپێکردن
• /help - یارمەتی
• /analyze - شیکاری چارت
• /topics - پێرستی تۆپیکەکان
• /signal - دۆزینەوەی سیگناڵ
• /history - مێژووی خۆت

**3. پرسیار:**
هەر پرسیارێکت هەیە دەربارەی SNRZ، تەنها بینووسە.

**4. تۆپیکە سەرەکییەکان:**
• S = سەپۆرت (Support)
• R = ڕیسرستانس (Resistance)
• SBR = سەپۆرت شکێنراوە بۆ ڕیسرستانس
• RBS = ڕیسرستانس شکێنراوە بۆ سەپۆرت
• VS = ڤالید سەپۆرت
• VR = ڤالید ڕیسرستانس
• IVS = ئینڤێرژن ڤالید سەپۆرت
• IVR = ئینڤێرژن ڤالید ڕیسرستانس
• PO2 = پاوەر ئۆف سێکەند تاچ
• SRR = سەپۆرت شکێنراوە ٢ ڕیسرستانس
• RSS = ڕیسرستانس شکێنراوە ٢ سەپۆرت
• GAP = ستراتیژی بۆشایی

**5. ڕێنمایی تەرەید:**
تارکێت یەکەم = 5 دەقە، تارکێت دووەم = 1 سەعات
"""
        await update.message.reply_text(help_text, parse_mode="Markdown")
    
    async def topics_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """کۆماندی /topics"""
        topics_text = """
📚 **تۆپیکەکانی SNRZ (بە ڕیزبەندی بەهێزی):**

1️⃣ **Trend** - ڕەوتی بازاڕ (بەهێزترین)
2️⃣ **PO2** - پاوەر ئۆف سێکەند تاچ
3️⃣ **PO2 Inversion** - ئینڤێرژنی PO2
4️⃣ **VS/VR Inversion** - ئینڤێرژنی ڤالید سەپۆرت و ڕیسرستانس
5️⃣ **GAP** - ستراتیژی بۆشایی
6️⃣ **VS/VR Fresh** - ڤالید سەپۆرت و ڕیسرستانسی تازە
7️⃣ **SBR/RBS** - شکێنراوەکان

📊 **جۆرەکانی ئۆردەر:**
• **BUY**: VS, IVR, RBS, SRR
• **SELL**: VR, IVS, SBR, RSS

⏰ **تایم فرەیمەکان:**
• دیاریکردنی زۆن: Weekly → Daily → 4H → 1H
• کۆنفیرمەیشن: 15m → 5m → 1m
• تارکێتی یەکەم: 5m
• تارکێتی دووەم: 1H

🎯 **False Breakout Area:**
ناوچەیەک کە مارکێت دوو جار برەیکاوتی کردووە و دواتر ڕیسپێکتی دەکاتەوە.
"""
        await update.message.reply_text(topics_text, parse_mode="Markdown")
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """کۆماندی /analyze"""
        await update.message.reply_text(
            "📊 **تکایە وێنەی چارتەکەت بنێرە بۆ شیکاری.**",
            parse_mode="Markdown"
        )
    
    async def history_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """کۆماندی /history"""
        user_id = str(update.effective_user.id)
        history = self.github.get_user_history(user_id)
        
        if not history:
            await update.message.reply_text("📭 **هیچ مێژوویەکت نیە.**")
            return
        
        text = "📜 **مێژووی شیکاریەکان:**\n\n"
        for i, item in enumerate(history[-5:]):  # 5 دوایین
            text += f"*{i+1}.* {item.get('timestamp', 'نادیار')}\n"
            analysis = item.get('analysis', {})
            text += f"   سیگناڵ: {analysis.get('signal', 'نادیار')}\n"
            text += f"   متمانە: {analysis.get('confidence', 0)*100:.0f}%\n\n"
        
        await update.message.reply_text(text, parse_mode="Markdown")
    
    async def signal_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """کۆماندی /signal"""
        keyboard = [
            [InlineKeyboardButton("📊 سیگناڵی BUY", callback_data="signal_buy")],
            [InlineKeyboardButton("📊 سیگناڵی SELL", callback_data="signal_sell")],
            [InlineKeyboardButton("🔄 دۆزینەوەی هەموو سیگناڵەکان", callback_data="signal_all")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "📈 **جۆری سیگناڵەکەت دیاری بکە:**",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    
    async def handle_image(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """هەڵگرتنی وێنە و شیکاری"""
        user_id = str(update.effective_user.id)
        
        # وەرگرتنی وێنە
        photo = update.message.photo[-1]
        file = await photo.get_file()
        file_path = f"temp_{user_id}.jpg"
        await file.download_to_drive(file_path)
        
        await update.message.reply_text("🔍 **شیکاری وێنە دەکرێت...**")
        
        try:
            # شیکاری وێنە
            analysis = self.image_processor.analyze_image(file_path)
            
            # شیکاری SNRZ
            snrz_result = self.analyzer.analyze_chart(analysis.get("zones", {}))
            
            # بارکردنی وێنە بۆ GitHub
            with open(file_path, 'rb') as f:
                image_data = f.read()
            image_url = self.github.upload_image(image_data, "chart.jpg", user_id)
            
            # پاشکەوتکردنی شیکاری
            full_analysis = {**analysis, **snrz_result}
            self.github.save_analysis(user_id, full_analysis, image_url)
            
            # ئامادەکردنی وەڵام
            result_text = self._format_analysis_result(full_analysis, image_url)
            await update.message.reply_text(result_text, parse_mode="Markdown")
            
            # پاککردنەوەی فایلی کاتی
            os.remove(file_path)
            
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            await update.message.reply_text(f"❌ **هەڵە لە شیکاری وێنە:** {str(e)}")
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """هەڵگرتنی تێکست و وەڵامدانەوە"""
        user_id = str(update.effective_user.id)
        text = update.message.text
        
        # گەڕان لە بنکەی زانیاری SNRZ
        response = self._find_answer_in_knowledge_base(text)
        
        if response:
            await update.message.reply_text(response, parse_mode="Markdown")
        else:
            await update.message.reply_text(
                "🤔 **ببورە، من تەنها ستراتیژی SNRZ تێدەگەم.**\n\n"
                "تکایە پرسیارەکەت زیاتر ڕوون بکەرەوە یان ئەم کۆماندانە بەکاربهێنە:\n"
                "/help - یارمەتی\n"
                "/topics - تۆپیکەکان\n"
                "/analyze - شیکاری وێنە"
            )
    
    def _find_answer_in_knowledge_base(self, question: str) -> str:
        """دۆزینەوەی وەڵام لە بنکەی زانیاری"""
        question_lower = question.lower()
        
        # کلیلە وشەکان و وەڵامەکان
        responses = {
            "سەپۆرت": "📊 **سەپۆرت (Support)**\nئەو شوێنەیە کە نرخ بەرز دەکاتەوە. ناوچەی پاڵپشتی بازاڕ.",
            "ڕیسرستانس": "📊 **ڕیسرستانس (Resistance)**\nئەو شوێنەیە کە نرخ دابەزێنێت. ناوچەی بەرگری بازاڕ.",
            "sbr": "📊 **SBR** (Support Breakout to Resistance)\nکاتێک سەپۆرت شکێنراوە بۆ ڕیسرستانس، سیگناڵی SELL.",
            "rbs": "📊 **RBS** (Resistance Breakout to Support)\nکاتێک ڕیسرستانس شکێنراوە بۆ سەپۆرت، سیگناڵی BUY.",
            "vs": "📊 **VS** (Valid Support)\nسەپۆرتی پەسەندکراو کە بەهێزە.",
            "vr": "📊 **VR** (Valid Resistance)\nڕیسرستانسی پەسەندکراو کە بەهێزە.",
            "po2": "📊 **PO2** (Power Of Second Touch)\nدووەم تەج - بەهێزترین تۆپیکەکان. کاتێک مارکێت دووەم جار زۆنەکە دەگرێتەوە.",
            "srr": "📊 **SRR** (Support Breakout 2 Resistance)\nسەپۆرتیک کە دوو ڕیسرستانسی شکاندبێت. سیگناڵی SELL.",
            "rss": "📊 **RSS** (Resistance Breakout 2 Support)\nڕیسرستانسیک کە دوو سەپۆرتی شکاندبێت. سیگناڵی BUY.",
            "gap": "📊 **GAP**\nناوچەی بۆشایی - کاتێک مارکێت بۆشایەک دروست دەکات و 80% پڕی دەکاتەوە.",
            "تایم فرەیم": "⏰ **تایم فرەیمەکان:**\n• دیاریکردنی زۆن: W→D→4H→1H\n• کۆنفیرمەیشن: 15m→5m→1m",
            "تارکێت": "🎯 **تارکێتەکان:**\n• یەکەم تارکێت: 5 دەقە\n• دووەم تارکێت: 1 سەعات",
            "خراپ": "❌ **False Breakout Area**\nناوچەیەک کە مارکێت دوو جار برەیکاوتی کردووە و دواتر ڕیسپێکتی دەکاتەوە."
        }
        
        for key, response in responses.items():
            if key in question_lower:
                return response
        
        return None
    
    def _format_analysis_result(self, analysis: Dict, image_url: str) -> str:
        """ڕێکخستنی ئەنجامی شیکاری بۆ نیشاندان"""
        signal = analysis.get("signal", "NEUTRAL")
        confidence = analysis.get("confidence", 0) * 100
        entry = analysis.get("entry_zone", "نادیار")
        targets = analysis.get("targets", [])
        stop_loss = analysis.get("stop_loss", "نادیار")
        
        # ئەمۆجی بۆ سیگناڵ
        signal_emoji = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "⚪"
        
        text = f"""
📊 **ئەنجامی شیکاری SNRZ**

{signal_emoji} **سیگناڵ:** {signal}
📈 **متمانە:** {confidence:.0f}%

🎯 **ناوچەی داخڵبوون:** {entry}
🛑 **ستۆپ لۆس:** {stop_loss}
📈 **تارکێتەکان:** {', '.join([str(t) for t in targets])}

📌 **شیکاری:** {analysis.get("analysis", "نادیار")}

📸 **وێنە:** [بینینی چارت]({image_url})

📝 **تۆپیکە دۆزراوەکان:** {', '.join(analysis.get("patterns", []))}

---
💡 پێشنیار: هەمیشە ڕێنمایی مەنیجمنێت بەکاربهێنە!
"""
        return text
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """کارلێککردن لەگەڵ دوگمەکان"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "analyze":
            await query.edit_message_text("📊 **تکایە وێنەی چارتەکەت بنێرە.**")
        
        elif data == "topics":
            await self.topics_command(update, context)
            await query.delete_message()
        
        elif data == "signal":
            await self.signal_command(update, context)
            await query.delete_message()
        
        elif data == "signal_buy":
            text = """
📈 **سیگناڵی BUY**

ئەم تۆپیکانە سیگناڵی کڕین دەدەن:
• VS (Valid Support)
• IVR (Inversion Valid Resistance)
• RBS (Resistance Breakout to Support)
• SRR (Support Breakout 2 Resistance)

📌 **ڕێنمایی:**
1. زۆن لە تایمفرەیمی گەورە دیاری بکە
2. کۆنفیرمەیشن لە تایمفرەیمی بچوک وەرگرە
3. ئۆردەری BUY بکەرەوە

🎯 تارکێتەکان: 5m → 1H
"""
            await query.edit_message_text(text, parse_mode="Markdown")
        
        elif data == "signal_sell":
            text = """
📉 **سیگناڵی SELL**

ئەم تۆپیکانە سیگناڵی فرۆشتن دەدەن:
• VR (Valid Resistance)
• IVS (Inversion Valid Support)
• SBR (Support Breakout to Resistance)
• RSS (Resistance Breakout 2 Support)

📌 **ڕێنمایی:**
1. زۆن لە تایمفرەیمی گەورە دیاری بکە
2. کۆنفیرمەیشن لە تایمفرەیمی بچوک وەرگرە
3. ئۆردەری SELL بکەرەوە

🎯 تارکێتەکان: 5m → 1H
"""
            await query.edit_message_text(text, parse_mode="Markdown")
        
        elif data == "signal_all":
            text = """
📊 **هەموو سیگناڵەکان**

🟢 **سیگناڵی BUY:**
• VS - ڤالید سەپۆرت
• IVR - ئینڤێرژن ڤالید ڕیسرستانس
• RBS - ڕیسرستانس شکێنراوە بۆ سەپۆرت
• SRR - سەپۆرت شکێنراوە ٢ ڕیسرستانس

🔴 **سیگناڵی SELL:**
• VR - ڤالید ڕیسرستانس
• IVS - ئینڤێرژن ڤالید سەپۆرت
• SBR - سەپۆرت شکێنراوە بۆ ڕیسرستانس
• RSS - ڕیسرستانس شکێنراوە ٢ سەپۆرت

📊 **ڕیزبەندی بەهێزی تۆپیکەکان:**
1️⃣ Trend
2️⃣ PO2
3️⃣ PO2 Inversion
4️⃣ VS/VR Inversion
5️⃣ GAP
6️⃣ VS/VR Fresh
7️⃣ SBR/RBS
"""
            await query.edit_message_text(text, parse_mode="Markdown")
        
        elif data == "tutorial":
            text = """
📖 **ڕاهێنانی SNRZ**

**بەشی 1: تیۆری (Theory)**
• چۆن سەپۆرت و ڕیسرستانس دیاری بکەین
• چۆن VS و VR بدۆزینەوە
• شێوازی SBR و RBS

**بەشی 2: پراکتیک (Practical)**
• شیکاری وێنەی چارت
• دیاریکردنی زۆنەکان
• دۆزینەوەی پاوەر ئۆف سێکەند تاچ

**بەشی 3: مەنیجمنێت**
• ڕێگای دابەشکردنی سەرمایە
• ستۆپ لۆس و تارکێت
• برەیک ئیڤن

📚 **پێشنیار:** کتێبەکە چەندین جار بخوێنەرەوە!
"""
            await query.edit_message_text(text, parse_mode="Markdown")

# دەستپێکردنی بۆت
if __name__ == "__main__":
    bot = SNRZBot()
    bot.run()