import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_FILE = BASE_DIR / "data" / "knowledge.json"

def load_knowledge():
    if not KNOWLEDGE_FILE.exists():
        print(f"Knowledge file not found: {KNOWLEDGE_FILE}")
        return {}

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

knowledge = load_knowledge()

def get_answer(question: str):
    if not question:
        return None

    key = question.strip().upper()

    print("Searching:", key)
    print("Available keys:", list(knowledge.keys())[:10])

    return knowledge.get(key)