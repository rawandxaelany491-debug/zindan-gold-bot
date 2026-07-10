import json
from pathlib import Path

KNOWLEDGE_FILE = Path("data/knowledge.json")


class SNRZKnowledge:
    def __init__(self):
        self.data = self.load_knowledge()

    def load_knowledge(self):
        try:
            with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print("ERROR: knowledge.json is invalid.")
            return {}

    def search(self, question: str):
        question = question.lower().strip()

        for topic in self.data.values():
            keywords = topic.get("keywords", [])

            for keyword in keywords:
                if keyword.lower() in question:
                    return topic.get("answer")

        return (
            "ببورە، وەڵامێک بۆ ئەم پرسیارە لە زانیارییەکانی SNRZ نەدۆزرایەوە.\n\n"
            "تکایە پرسیارەکەت بە شێوەیەکی تر بنووسە."
        )


knowledge = SNRZKnowledge()


def get_answer(message: str) -> str:
    return knowledge.search(message)