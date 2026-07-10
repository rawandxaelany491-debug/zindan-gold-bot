"""
analysis.py

Analyze TradingView charts using Gemini + SNRZ Strategy.
"""

import io
from PIL import Image
import google.generativeai as genai

from config import Config
from prompts import (
    SYSTEM_PROMPT,
    KNOWLEDGE_BASE,
    OUTPUT_RULES,
    IMAGE_ANALYSIS_RULES,
)

genai.configure(api_key=Config.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_chart(image_bytes: bytes) -> str:
    """
    Analyze an uploaded TradingView chart using SNRZ Strategy.
    """

    try:
        image = Image.open(io.BytesIO(image_bytes))

        full_prompt = f"""
{SYSTEM_PROMPT}

{KNOWLEDGE_BASE}

{OUTPUT_RULES}

{IMAGE_ANALYSIS_RULES}
"""

        response = model.generate_content(
            [
                full_prompt,
                image,
            ]
        )

        text = getattr(response, "text", "").strip()

        if text:
            return text

        return "❌ هیچ وەڵامێک لە Gemini وەرنەگیرا."

    except Exception as e:
        return f"❌ هەڵە لە شیکردنەوە:\n{str(e)}"