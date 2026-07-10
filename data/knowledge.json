"""
knowledge.py
SNRZ Knowledge Loader
"""

import json
from pathlib import Path

# Path to knowledge file
KNOWLEDGE_FILE = Path("data/knowledge.json")


def load_knowledge():
    """Load knowledge from JSON file."""

    if not KNOWLEDGE_FILE.exists():
        return {}

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


knowledge = load_knowledge()


def get_answer(question: str):
    """
    Search for a topic in the knowledge base.
    """

    if not question:
        return None

    key = question.strip().upper()

    return knowledge.get(key)