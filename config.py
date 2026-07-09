"""
config.py

Application configuration for the Gold (XAUUSD) Telegram Bot.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    # Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Bot Settings
    SYMBOL = "XAUUSD"
    LANGUAGE = "ku"

    STRATEGY_NAME = "Zindan Strategy"

    DEFAULT_RISK_PERCENT = float(
        os.getenv("DEFAULT_RISK_PERCENT", "1.0")
    )

    MIN_RISK_REWARD = float(
        os.getenv("MIN_RISK_REWARD", "2.0")
    )

    BREAKOUT_CONFIRMATION = 0.75

    ALLOWED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }

    MAX_IMAGE_SIZE_MB = int(
        os.getenv("MAX_IMAGE_SIZE_MB", "10")
    )

    REQUEST_TIMEOUT = int(
        os.getenv("REQUEST_TIMEOUT", "60")
    )

    @classmethod
    def validate(cls):
        required = {
            "TELEGRAM_BOT_TOKEN": cls.TELEGRAM_BOT_TOKEN,
            "GEMINI_API_KEY": cls.GEMINI_API_KEY,
        }

        missing = [
            key for key, value in required.items()
            if not value
        ]

        if missing:
            raise EnvironmentError(
                f"Missing environment variables: {', '.join(missing)}"
            )