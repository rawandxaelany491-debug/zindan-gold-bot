from knowledge import SNRZ_DATA

ALIASES = {
    "s": "support",
    "support": "support",
    "پاڵپشتی": "support",
    "سەپۆرت": "support",

    "r": "resistance",
    "resistance": "resistance",
    "بەرگری": "resistance",
    "ڕیزستانس": "resistance",

    "vs": "vs",
    "vr": "vr",

    "ivs": "ivs",
    "ivr": "ivr",

    "p": "po2",
    "po2": "po2",

    "pi": "po2 inversion",

    "rb": "rbs",
    "rbs": "rbs",

    "sb": "sbr",
    "sbr": "sbr",

    "sr": "srr",
    "srr": "srr",

    "rs": "rss",
    "rss": "rss",

    "ls": "liquidity sweep",
    "lr": "liquidity run",

    "pbp": "pump base pump",
    "dbd": "dump base dump",

    "g": "gap",
    "gap": "gap",

    "fb": "false breakout",

    "t": "trend",

    "tf": "timeframe",

    "mm": "money management",
}


def search_snrz(question):
    q = question.strip().lower()

    key = ALIASES.get(q)

    if key and key in SNRZ_DATA:
        return SNRZ_DATA[key]

    return (
        "❌ ئەم بابەتە نەدۆزرایەوە.\n\n"
        "تکایە یەکێک لەم کورتکراوانە بنێرە:\n"
        "S, R, VS, VR, P, RB, SB, LS, G, T, TF, MM"
    )