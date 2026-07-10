import io
from PIL import Image
import google.generativeai as genai

from config import Config
from prompts import SYSTEM_PROMPT

genai.configure(api_key=Config.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_chart(image_bytes):

    image = Image.open(io.BytesIO(image_bytes))

    response = model.generate_content(
        [
            SYSTEM_PROMPT,
            image,
        ]
    )

    return response.text