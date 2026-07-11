# knowledge.py

SNRZ_DATA = {

    "support": """
Support (S):
ناوچەیەکە کە نرخ لێی بەرزدەبێتەوە.
Support بە تەنها بەس نییە، دەبێت Confirmation هەبێت.
""",

    "resistance": """
Resistance (R):
ناوچەیەکە کە نرخ لێی دادەبەزێت.
Resistance بە تەنها بەس نییە، دەبێت Confirmation هەبێت.
""",

    "vs": """
Valid Support (VS):
Support ـێکی ڕاستەقینەیە.
خاوەنی First Movement و Second Movement ـە.
لە Buy Confirmation بەکاردێت.
""",

    "vr": """
Valid Resistance (VR):
Resistance ـێکی ڕاستەقینەیە.
خاوەنی First Movement و Second Movement ـە.
لە Sell Confirmation بەکاردێت.
""",

    "rbs": """
RBS
Resistance Breakout To Support

کاتێک Resistance دەشکێت،
دەبێتە Support.

لە SNRZ ئەمە یەکێکە لە Buy Confirmation.
""",

    "sbr": """
SBR
Support Breakout To Resistance

کاتێک Support دەشکێت،
دەبێتە Resistance.

لە SNRZ ئەمە یەکێکە لە Sell Confirmation.
""",

    "srr": """
SRR

دوو Support دەشکێت.
دوای ئەوە Pullback.
پاشان Confirmation.
""",

    "rss": """
RSS

دوو Resistance دەشکێت.
دوای ئەوە Pullback.
پاشان Confirmation.
""",

    "po2": """
PO2
Power Of Second Touch

یەکێکە لە بەهێزترین تۆپیکەکانی SNRZ.
لە ڕیزبەندی هێزدا دوای Trend دێت.
""",

    "liquidity sweep": """
Liquidity Sweep

مارکێت بە Shadow
Liquidity دەسووپێت
و دووبارە دەگەڕێتەوە.
""",

    "liquidity run": """
Liquidity Run

مارکێت بە Full Body
Zone دەبڕێت.
""",

    "gap": """
Gap Strategy

ئەگەر Gap دروست بوو،
مارکێت زۆرجار دەگەڕێتەوە بۆ پڕکردنەوەی.
""",

    "trend": """
Trend Ranking

1. Trend
2. PO2
3. PO2 Inversion
4. VS/VR Inversion
5. GAP
6. Fresh VS/VR
7. SBR / RBS
""",

    "timeframe": """
Timeframe Confirmation

Weekly → Daily → 4H

Daily → 4H → 1H

4H → 1H → 30M

1H → 30M → 15M

15M → 5M
""",

    "money management": """
Money Management

• سەرمایە پارێزە.
• Target1 کە گەیشت، Capital دەرکێشە.
• بە قازانجەکە Trade بکە.
• بۆ دەستپێک Cent Account باشترە.
""",

}