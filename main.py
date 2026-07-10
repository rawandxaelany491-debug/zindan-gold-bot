"""
analysis.py

Analyze XAUUSD charts using the SNRZ Strategy.
"""

import io

from PIL import Image
import google.generativeai as genai

from config import Config
from prompts import SYSTEM_PROMPT

# Configure Gemini
genai.configure(api_key=Config.GEMINI_API_KEY)

# Load model
model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_chart(image_bytes):
    """
    Analyze a TradingView chart using SNRZ Strategy.
    """

    try:
        # Open image
        image = Image.open(io.BytesIO(image_bytes))

        # Send prompt + image to Gemini
        response = model.generate_content(
            [
                SYSTEM_PROMPT,
                image,
            ]
        )

        # Return response
        if hasattr(response, "text") and response.text:
            return response.text.strip()

        return (
            "❌ هیچ شیکردنەوەیەک نەگەڕایەوە.\n"
            "تکایە وێنەیەکی ڕوونتر بنێرە."
        )

    except Exception as e:
        return (
            "❌ هەڵە لە شیکردنەوەی چارت.\n\n"
            f"{str(e)}"
        )