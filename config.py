import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    @classmethod
    def validate(cls):
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is missing")

        if not cls.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is missing")