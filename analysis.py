import io
from PIL import Image
import google.generativeai as genai

from config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

SYSTEM_PROMPT = """
تۆ شارەزایەکی پیشەیی لە شیکردنەوەی Gold (XAUUSD) ـیت.

هەمیشە تەنها بە زمانی کوردی سۆرانی وەڵام بدە.

لە هەر وێنەیەکی TradingView ئەم شتانە دیاری بکە:

📈 ئاراستە:
- Buy یان Sell
- هۆکاری ئاراستە

🎯 خاڵی چوونە ناو بازاڕ (Entry)

🛑 ستۆپ لۆس (Stop Loss)

🎯 تەیک پرۆفیت:
- TP1
- TP2
- TP3

📊 ئاستی دڵنیایی:
بە شێوەی % (بۆ نموونە 87%)

⚠️ مەترسی:
- کەم
- مامناوەند
- بەرز

📝 شیکردنەوە:
• Market Structure
• Support & Resistance
• Liquidity
• Order Block
• Fair Value Gap
• BOS / CHoCH ئەگەر هەبوو
• هۆکاری Buy یان Sell

یاسا:
- تەنها بە کوردی سۆرانی وەڵام بدە.
- هیچ وشەی ئینگلیزی بەکارمەهێنە جگە لە:
Buy
Sell
TP1
TP2
TP3
XAUUSD
BOS
CHoCH
FVG
Order Block
Liquidity
"""

def analyze_chart(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))

        response = model.generate_content(
            [
                SYSTEM_PROMPT,
                image
            ]
        )

        if hasattr(response, "text") and response.text:
            return response.text

        return "❌ هیچ وەڵامێک لە Gemini وەرنەگیرا."

    except Exception as e:
        return f"❌ هەڵە:\n{str(e)}"