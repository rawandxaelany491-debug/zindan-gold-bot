import io
from PIL import Image
import google.generativeai as genai

from config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

SYSTEM_PROMPT = """
You are a professional Gold (XAUUSD) trading analyst.

Analyze the uploaded chart and return:

📈 Trend:
🎯 Entry:
🛑 Stop Loss:
🎯 Take Profit:
- TP1
- TP2
- TP3

📊 Confidence:
⚠️ Risk:

📝 Analysis:
- Market Structure
- Support & Resistance
- Liquidity
- Order Block
- Fair Value Gap
- Reason for the trade

Keep the answer concise.
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

        if response.text:
            return response.text

        return "❌ Gemini returned an empty response."

    except Exception as e:
        return f"❌ Analysis failed:\n{e}"