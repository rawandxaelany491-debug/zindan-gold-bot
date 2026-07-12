from rules import SNRZ_RULES, BUY_SETUPS, SELL_SETUPS, TIMEFRAME_FLOW

def answer_snrz_question(question: str):
    q = question.lower()

    if "vs" in q:
        return "VS = Valid Support. It is a strong support zone in SNRZ."
    if "vr" in q:
        return "VR = Valid Resistance. It is a strong resistance zone in SNRZ."
    if "ivs" in q:
        return "IVS = Inversion Valid Support."
    if "ivr" in q:
        return "IVR = Inversion Valid Resistance."
    if "rbs" in q:
        return "RBS = Resistance Breakout to Support."
    if "sbr" in q:
        return "SBR = Support Breakout to Resistance."
    if "po2" in q:
        return "PO2 = Power Of Second Touch."
    if "srr" in q:
        return "SRR = Support Breakout 2 Resistance."
    if "rss" in q:
        return "RSS = Resistance Breakout 2 Support."
    if "gap" in q:
        return "GAP Strategy = price gap zone that may be filled later."
    return {
        "rules": SNRZ_RULES,
        "buy_setups": BUY_SETUPS,
        "sell_setups": SELL_SETUPS,
        "timeframes": TIMEFRAME_FLOW
    }

def analyze_chart(image_path: str):
    return {
        "signal": "wait",
        "market_state": "neutral",
        "detected_rules": list(SNRZ_RULES.keys()),
        "buy_setups": BUY_SETUPS,
        "sell_setups": SELL_SETUPS,
        "notes": [
            "Check higher timeframe first.",
            "Mark support and resistance.",
            "Look for breakout and retest.",
            "Watch for false breakout and liquidity sweep.",
            "Confirm with SNRZ rules before entry."
        ],
        "image_path": image_path
    }
