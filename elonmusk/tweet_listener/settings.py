import os

from dotenv import load_dotenv

load_dotenv()

TELEGRA_BOT_TOKEN = os.environ['TELEGRA_BOT_TOKEN']
TELEGRAM_CHANNEL_NAME = os.getenv('TELEGRAM_CHANNEL_NAME', 'elon_alerts')
TELEGRAM_SESSION_NAME = os.getenv('TELEGRAM_SESSION_NAME', 'bot_session')
WEBHOOK_URL = os.environ['WEBHOOK_URL']