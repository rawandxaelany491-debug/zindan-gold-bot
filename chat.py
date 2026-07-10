from openai import OpenAI

from config import Config
from prompts import (
    SYSTEM_PROMPT,
    KNOWLEDGE_BASE,
    OUTPUT_RULES,
)

client = OpenAI(
    api_key=Config.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)


def chat_with_ai(message: str) -> str:
    try:
        prompt = f"""
{SYSTEM_PROMPT}

{KNOWLEDGE_BASE}

{OUTPUT_RULES}

User Question:

{message}
"""

        response = client.chat.completions.create(
            model="qwen/qwen2.5-vl-72b-instruct:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ هەڵە:\n{str(e)}"