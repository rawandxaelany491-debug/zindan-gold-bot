"""
config.py
Configuration for SNRZ Telegram Bot
"""

import logging
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env file")

# Logging
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("SNRZ")