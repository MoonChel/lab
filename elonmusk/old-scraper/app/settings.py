import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_API_ID = os.environ['TELEGRAM_API_ID']
TELEGRAM_API_HASH = os.environ['TELEGRAM_API_HASH']
LAST_MESSAGE_FILE = os.getenv('LAST_MESSAGE_FILE', "last_message_id.json")
TELEGRAM_SESSION_NAME = os.getenv('TELEGRAM_SESSION_NAME', 'telegram_session')