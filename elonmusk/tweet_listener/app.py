import re
import requests
import structlog
from telethon import TelegramClient, events
from telethon.sessions import StringSession

import settings

# Configure structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
logger = structlog.get_logger()

client = TelegramClient(
    StringSession(settings.TELEGRAM_SESSION_TOKEN),
    api_id=settings.TELEGRAM_API_ID,
    api_hash=settings.TELEGRAM_API_HASH,
).start()

pattern = r"https?://(?:twitter\.com|x\.com)/[^\s)\]\.]+"

def classify_message(text):
    if re.search(r"reposted a post from", text, re.IGNORECASE):
        return "repost"
    elif re.search(r"quoted a post from", text, re.IGNORECASE):
        return "quote"
    elif re.search(r"posted", text, re.IGNORECASE):
        return "post"
    elif re.search(r"replied", text, re.IGNORECASE):
        return "reply"
    elif re.search(r"is now following", text, re.IGNORECASE):
        return "follow"
    elif re.search(r"liked", text, re.IGNORECASE):
        return "liked"
    else:
        return "other"

@client.on(events.NewMessage(chats=[settings.TELEGRAM_CHANNEL_NAME, "@test_channel_elon"]))
async def new_message_handler(event):
    event_json = {
        "id": event.message.id,
        "msg_type": classify_message(event.message.message),
        "text": event.message.message,
    }
    logger.info("New message received", **event_json)

    # Send entire event JSON to FastAPI
    response = requests.post(settings.WEBHOOK_URL, json=event_json)
    logger.info("Sent event to FastAPI", status_code=response.status_code, response_text=response.text)


if __name__ == '__main__':
    logger.info("Listener is running...")
    client.run_until_disconnected()