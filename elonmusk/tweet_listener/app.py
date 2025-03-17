import requests
import structlog
from telethon import TelegramClient, events
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
    settings.TELEGRAM_SESSION_NAME,
    api_id=settings.TELEGRAM_API_ID,
    api_hash=settings.TELEGRAM_API_HASH,
).start(bot_token=settings.TELEGRAM_BOT_TOKEN)


@client.on(events.NewMessage(chats=settings.TELEGRAM_CHANNEL_NAME))
async def new_message_handler(event):
    event_json = event.to_dict()
    logger.info("New message received", channel=settings.TELEGRAM_CHANNEL_NAME, event=event_json)

    # Send entire event JSON to FastAPI
    response = requests.post(settings.WEBHOOK_URL, json=event_json)
    logger.info("Sent event to FastAPI", status_code=response.status_code, response_text=response.text)


if __name__ == '__main__':
    logger.info("Listener is running...")
    client.run_until_disconnected()