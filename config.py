"""
config.py
SNRZ Telegram Bot Configuration
"""

import logging
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env file")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("SNRZ")