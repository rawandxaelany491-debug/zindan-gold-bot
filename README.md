# Gold (XAUUSD) Telegram Bot

A Telegram bot that analyzes TradingView charts of XAUUSD (Gold) using OpenAI Vision and the Zindan Strategy.

## Features

- Analyze only XAUUSD charts
- Uses OpenAI Vision
- Detects:
  - Trend
  - Support
  - Resistance
  - Breakout (75% confidence)
  - Pullback
  - Inversion
  - Sideway
- Returns:
  - BUY
  - SELL
  - WAIT
- Provides:
  - Entry Price
  - Stop Loss
  - Take Profit
  - Risk / Reward
- Kurdish responses
- Ready for Render deployment

## Environment Variables

Create a `.env` file based on `.env.example`.

Required variables:

```
TELEGRAM_BOT_TOKEN=
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1
LOG_LEVEL=INFO
DEFAULT_RISK_PERCENT=1.0
REQUEST_TIMEOUT=60
```

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Deploy

Deploy on Render using the included `render.yaml`.