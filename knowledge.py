"""
knowledge.py
Knowledge Base loader and search engine
"""

import json
from pathlib import Path

from config import KNOWLEDGE_FILE, logger


class KnowledgeBase:
    def __init__(self):
        self.data = {}
        self.load()

    def load(self):
        path = Path(KNOWLEDGE_FILE)

        if not path.exists():
            logger.warning("Knowledge file not found.")
            self.data = {}
            return

        with open(path, "r", encoding="utf-8") as file:
            self.data = json.load(file)

        logger.info("Knowledge Base Loaded.")

    def search(self, question: str):

        question = question.lower().strip()

        for key, value in self.data.items():

            keywords = value.get("keywords", [])

            if key.lower() in question:
                return value["answer"]

            for word in keywords:
                if word.lower() in question:
                    return value["answer"]

        return (
            "❌ وەڵامێک بۆ ئەم پرسیارە لە زانیارییەکانی "
            "SNRZ نەدۆزرایەوە."
        )


knowledge = KnowledgeBase()