"""
config.py
Production configuration for SNRZ Telegram Bot
Python 3.12
"""

import logging
import os

from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# ===========================
# Telegram
# ===========================

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found inside .env file.")

# ===========================
# Bot Information
# ===========================

BOT_NAME = "SNRZ Assistant"
BOT_VERSION = "1.0.0"
BOT_LANGUAGE = "ku"

# ===========================
# Knowledge Base
# ===========================

KNOWLEDGE_FILE = "data/knowledge.json"

# ===========================
# Logging
# ===========================

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
)

logger = logging.getLogger(BOT_NAME)