"""
analysis.py

Gemini Vision analysis module.
"""

import google.generativeai as genai

from config import Config
from prompts import SYSTEM_PROMPT


genai.configure(api_key=Config.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_chart(image_path: str) -> str:
    """
    Analyze XAUUSD TradingView chart using Gemini Vision.
    """

    with open(image_path, "rb") as img:
        image_data = img.read()

    response = model.generate_content(
        [
            SYSTEM_PROMPT,
            "ئەم وێنەیەی TradingView ی XAUUSD شیکاربکە.",
            {
                "mime_type": "image/png",
                "data": image_data,
            },
        ]
    )

    return response.text