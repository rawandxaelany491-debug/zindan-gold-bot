import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")