import json
import os

DB_FILE = "data/snrz_knowledge.json"


def load_knowledge():
    if not os.path.exists(DB_FILE):
        return {
            "version": "1.0",
            "strategy": "SNRZ",
            "knowledge": []
        }

    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_knowledge(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def add_rule(title, content):
    data = load_knowledge()

    data["knowledge"].append({
        "title": title,
        "content": content
    })

    save_knowledge(data)


def get_all_rules():
    return load_knowledge()["knowledge"]