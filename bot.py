from config import BOT_TOKEN
from analysis import answer_snrz_question, analyze_chart

def start_command():
    return "SNRZ Bot is ready. Send me a question about SNRZ or a chart image."

def help_command():
    return "Commands: /start, /help, /rules, /analyze"

def rules_command():
    return answer_snrz_question("show all snrz rules")

def text_command(text: str):
    return answer_snrz_question(text)

def analyze_command(image_path: str):
    return analyze_chart(image_path)

def run_bot():
    print("SNRZ Telegram Bot started.")
    print(f"Token loaded: {BOT_TOKEN[:6]}...")
    # Telegram handlers will be added here.
