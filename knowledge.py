"""
knowledge.py
SNRZ Knowledge Loader
"""

import json
from pathlib import Path

KNOWLEDGE_FILE = Path("data/knowledge.json")


def load_knowledge():
    if not KNOWLEDGE_FILE.exists():
        print("knowledge.json not found.")
        return {}

    try:
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Knowledge loading error: {e}")
        return {}


knowledge = load_knowledge()


def get_answer(question: str):
    if not question:
        return None

    q = question.strip().upper()

    # Exact match
    if q in knowledge:
        return knowledge[q]

    # Search by title
    for item in knowledge.values():
        title = item.get("title", "").upper()

        if q == title:
            return item

    # Keyword search
    for key, item in knowledge.items():
        if q in key.upper():
            return item

        title = item.get("title", "").upper()

        if q in title:
            return item

    return None