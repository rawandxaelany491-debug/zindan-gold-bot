# -*- coding: utf-8 -*-
"""
بەردەوامی ڕۆژانە (Streaks).
هەر جارێک بەکارهێنەرێک پرسیارێک بکات یان وێنەیەک بنێرێت، ئەم ڕۆژە وەک
"چالاک" تۆمار دەکرێت. streak ـی ئێستای بەکارهێنەر ژمارەی ڕۆژە بەردەوامەکانە
کە تێیدا چالاکی هەبووە (بەبێ بڕین)، بۆ هاندانی بەردەوامیی ڕۆژانە.
"""

import json
import os
from datetime import datetime, timedelta, timezone

STREAKS_FILE = "streaks.json"


def _today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _yesterday_str() -> str:
    return (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")


def _load() -> dict:
    if not os.path.exists(STREAKS_FILE):
        return {}
    try:
        with open(STREAKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save(data: dict) -> None:
    with open(STREAKS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def record_activity(user_id: int) -> int:
    """تۆمارکردنی چالاکی بۆ ئەمڕۆ. streak ـی نوێ دەگەڕێنێتەوە."""
    data = _load()
    entry = data.get(str(user_id))
    today = _today_str()
    yesterday = _yesterday_str()

    if not entry:
        entry = {"last_active": today, "streak": 1}
    elif entry.get("last_active") == today:
        pass  # پێشتر ئەمڕۆ چالاک بووە، هیچ نەگۆڕدرێت
    elif entry.get("last_active") == yesterday:
        entry["streak"] = entry.get("streak", 0) + 1
        entry["last_active"] = today
    else:
        entry = {"last_active": today, "streak": 1}

    data[str(user_id)] = entry
    _save(data)
    return entry["streak"]


def get_streak(user_id: int) -> int:
    """گەڕاندنەوەی streak ـی ئێستای بەکارهێنەر. ئەگەر پچڕاوە، 0 دەگەڕێنێتەوە."""
    data = _load()
    entry = data.get(str(user_id))
    if not entry:
        return 0

    today = _today_str()
    yesterday = _yesterday_str()
    if entry.get("last_active") not in (today, yesterday):
        return 0  # streak پچڕاوە (زیاتر لە ڕۆژێک بەبێ چالاکی تێپەڕیوە)

    return entry.get("streak", 0)