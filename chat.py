import google.generativeai as genai

from config import Config
from prompts import SYSTEM_PROMPT

genai.configure(api_key=Config.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-pro")


def chat_with_ai(message: str) -> str:
    try:
        response = model.generate_content(
            [
                SYSTEM_PROMPT,
                f"User message:\n{message}"
            ]
        )

        if hasattr(response, "text") and response.text:
            return response.text.strip()

        return "❌ هیچ وەڵامێک نەگەڕایەوە."

    except Exception as e:
        return f"❌ هەڵە:\n{e}"