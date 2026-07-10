"""
knowledge.py
"""

import json

with open(
    "data/knowledge.json",
    "r",
    encoding="utf-8"
) as f:
    knowledge = json.load(f)


def get_answer(question: str):

    question = question.strip().upper()

    return knowledge.get(
        question,
        "❌ ئەم بابەتە لە Knowledge Base نییە."
    )