"""
knowledge.py
Knowledge loader for SNRZ Telegram Bot
"""

import json
from pathlib import Path


DATA_FILE = Path("data/knowledge.json")


def load_knowledge():
    """Load knowledge from JSON file."""

    if not DATA_FILE.exists():
        return {}

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


knowledge = load_knowledge()


def get_answer(question: str):
    """Return an answer if the question exists."""

    if not question:
        return None

    return knowledge.get(question.strip().upper())