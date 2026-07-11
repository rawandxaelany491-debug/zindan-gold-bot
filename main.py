async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
👋 بەخێربێیت بۆ SNRZ Assistant Bot

📚 من تەنها پرسیارەکانی ستراتیژی SNRZ وەڵام دەدەم.

دەتوانیت دەربارەی ئەم بابەتانە پرسیار بکەیت:

• Support (S)
• Resistance (R)
• Valid Support (VS)
• Valid Resistance (VR)
• Inversion VS
• Inversion VR
• RBS
• SBR
• SRR
• RSS
• PO2 (Power Of Second Touch)
• PO2 Inversion
• Liquidity Sweep
• Liquidity Run
• Pump Base Pump
• Dump Base Dump
• Gap Strategy
• False Breakout Area
• Fresh Zones
• Trend
• Trend Ranking
• Timeframe Confirmation
• Valid Zones
• Zone Types
• Money Management

✍️ پرسیارت لە کام بابەتە هەیە؟
"""

    await update.message.reply_text(text)