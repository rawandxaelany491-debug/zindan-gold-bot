import google.generativeai as genai
from PIL import Image
import io
from config import Config
# Configure Gemini
genai.configure(api_key=Config.GEMINI_API_KEY)
# Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")
SYSTEM_PROMPT = """
You are Gold AI, a professional trading analyst.
Analyze the uploaded trading chart carefully.
Return your answer in exactly this format:
📈 Trend:
(Bullish / Bearish / Sideways)
🎯 Entry:
(price or zone)
🛑 Stop Loss:
(price)
🎯 Take Profit:
TP1:
TP2:
TP3:
📊 Confidence:
(%)
⚠️ Risk:
(Low / Medium / High)
📝 Analysis:
Explain briefly:
- Market structure
- Support & Resistance
- Liquidity
- Order Block (if any)
- Fair Value Gap (if any)
- Reason for the trade
Keep the answer clear and concise.
"""
def analyze_chart(image_bytes):
    """
    Analyze a chart image using Gemini.
    """
    try:
        response = model.generate_content(
            [
                SYSTEM_PROMPT,
                {
                    "mime_type": "image/jpeg",
                    "data": image_bytes,
                },
            ]
        )
        if hasattr(response, "text") and response.text:
            return response.text
        return "❌ Gemini returned an empty response."
    except Exception as e:
        return f"❌ Analysis failed:\n{str(e)}"