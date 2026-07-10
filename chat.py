"""
chat.py

Chat with Gemini using only the SNRZ Strategy.
"""

import google.generativeai as genai

from config import Config
from prompts import (
    SYSTEM_PROMPT,
    KNOWLEDGE_BASE,
    OUTPUT_RULES,
)

genai.configure(api_key=Config.GEMINI_API_KEY)


genai.configure(api_key=Config.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

def chat_with_ai(message: str) -> str:
    """
    Answer user questions using ONLY the SNRZ Strategy.
    """

    try:
        full_prompt = f"""
{SYSTEM_PROMPT}

{KNOWLEDGE_BASE}

{OUTPUT_RULES}

User Question:

{message}
"""

        response = model.generate_content(full_prompt)

        text = getattr(response, "text", "").strip()

        if text:
            return text

        return "❌ هیچ وەڵامێک لە Gemini وەرنەگیرا."

    except Exception as e:
        return f"❌ هەڵە:\n{str(e)}"