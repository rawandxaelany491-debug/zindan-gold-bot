import base64
from openai import OpenAI

from config import Config
from prompts import (
    SYSTEM_PROMPT,
    KNOWLEDGE_BASE,
    OUTPUT_RULES,
    IMAGE_ANALYSIS_RULES,
)

client = OpenAI(
    api_key=Config.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)


def analyze_chart(image_bytes: bytes) -> str:
    try:
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

        prompt = f"""
{SYSTEM_PROMPT}

{KNOWLEDGE_BASE}

{OUTPUT_RULES}

{IMAGE_ANALYSIS_RULES}
"""

        response = client.chat.completions.create(
            model="qwen/qwen2.5-vl-72b-instruct:free",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}"
                            },
                        },
                    ],
                }
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ هەڵە لە شیکردنەوە:\n{str(e)}"