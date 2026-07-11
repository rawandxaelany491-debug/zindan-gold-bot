async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
👋 بەخێربێیت بۆ SNRZ Assistant Bot

📚 من فێرکارییەکانی ستراتیژی SNRZ وەڵام دەدەم.

━━━━━━━━━━━━━━

📖 تۆپیکەکان

S  → Support
R  → Resistance

VS → Valid Support
VR → Valid Resistance

IVS → Inversion Valid Support
IVR → Inversion Valid Resistance

P → PO2
PI → PO2 Inversion

RB → RBS
SB → SBR

SR → SRR
RS → RSS

LS → Liquidity Sweep
LR → Liquidity Run

PBP → Pump Base Pump
DBD → Dump Base Dump

G → Gap Strategy

FB → False Breakout

T → Trend

TF → Timeframe Confirmation

MM → Money Management

━━━━━━━━━━━━━━

✍️ تەنها کورتکراوەکە بنێرە.

نمونە:

S
R
VS
P
RB
G
MM
"""

    await update.message.reply_text(text)