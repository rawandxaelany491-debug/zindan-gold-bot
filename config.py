"""
config.py

Application configuration for the Gold (XAUUSD) Telegram Bot.
Loads all required environment variables.
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config:
    """
    Global application configuration.
    """

    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv(
        "OPENAI_MODEL",
        "gpt-4.1"
    )

    # Logging
    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )

    # Bot Settings
    SYMBOL = "XAUUSD"
    LANGUAGE = "ku"

    # Strategy
    STRATEGY_NAME = "Zindan Strategy"

    # Risk Management
    DEFAULT_RISK_PERCENT = float(
        os.getenv(
            "DEFAULT_RISK_PERCENT",
            "1.0"
        )
    )

    MIN_RISK_REWARD = float(
        os.getenv(
            "MIN_RISK_REWARD",
            "2.0"
        )
    )

    BREAKOUT_CONFIRMATION = 0.75

    # Allowed image formats
    ALLOWED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }

    MAX_IMAGE_SIZE_MB = int(
        os.getenv(
            "MAX_IMAGE_SIZE_MB",
            "10"
        )
    )

    # Timeouts
    REQUEST_TIMEOUT = int(
        os.getenv(
            "REQUEST_TIMEOUT",
            "60"
        )
    )

    @classmethod
    def validate(cls):
        """
        Validate required environment variables.
        """
        required = {
            "TELEGRAM_BOT_TOKEN": cls.TELEGRAM_BOT_TOKEN,
            "OPENAI_API_KEY": cls.OPENAI_API_KEY,
        }

        missing = [
            key for key, value in required.items()
            if not value
        ]

        if missing:
            raise EnvironmentError(
                f"Missing environment variables: {', '.join(missing)}"
            )