import os

from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.environ['WEBHOOK_URL']
TELEGRAM_API_ID = os.environ['TELEGRAM_API_ID']
TELEGRAM_API_HASH = os.environ['TELEGRAM_API_HASH']
TELEGRAM_CHANNEL_NAME = os.getenv('TELEGRAM_CHANNEL_NAME', '@elon_alerts')
TELEGRAM_SESSION_TOKEN=os.environ['TELEGRAM_SESSION_TOKEN']