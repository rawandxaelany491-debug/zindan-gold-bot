import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # تۆکینی بۆتی تێلیگرام
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")
    
    # GitHub
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "YOUR_GITHUB_TOKEN")
    GITHUB_REPO = os.getenv("GITHUB_REPO", "your-username/snrz-bot-data")
    
    # ڕێڕەوەکان
    DATA_PATH = "data/"
    IMAGE_PATH = "data/images/"
    MODEL_PATH = "models/"
    
    # ڕێکخستنەکانی تایم فرەیم
    TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h", "1d", "1w"]
    
    # تۆپیکەکانی SNRZ
    SNRZ_TOPICS = {
        "support": "S",
        "resistance": "R",
        "sbr": "Support Breakout to Resistance",
        "rbs": "Resistance Breakout to Support",
        "vs": "Valid Support",
        "vr": "Valid Resistance",
        "ivs": "Inversion Valid Support",
        "ivr": "Inversion Valid Resistance",
        "po2": "Power Of Second Touch",
        "srr": "Support Breakout 2 Resistance",
        "rss": "Resistance Breakout 2 Support",
        "gap": "GAP STRATEGY"
    }
    
    # پێناسەی جۆری ئۆردەر
    BUY_SIGNALS = ["VS", "IVR", "RBS", "SRR"]
    SELL_SIGNALS = ["VR", "IVS", "SBR", "RSS"]