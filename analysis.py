"""
analysis.py

OpenAI Vision analysis module.
"""

import base64
from openai import OpenAI

from config import Config
from prompts import SYSTEM_PROMPT


client = OpenAI(
    api_key=Config.OPENAI_API_KEY
)


def encode_image(image_path: str) -> str:
    """
    Encode image into Base64.
    """

    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


def analyze_chart(image_path: str) -> str:
    """
    Analyze XAUUSD TradingView chart
    using OpenAI Vision.
    """

    image_base64 = encode_image(image_path)

    response = client.responses.create(
        model=Config.OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": SYSTEM_PROMPT,
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "ئەم وێنەیەی TradingView ی XAUUSD شیکاربکە.",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{image_base64}",
                    },
                ],
            },
        ],
    )

    try:
        return response.output_text.strip()

    except AttributeError:
        return (
            response.output[0]
            .content[0]
            .text
            .strip()
        )

    except Exception as e:
        return f"Analysis Error: {e}"