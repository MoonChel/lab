import requests
from telethon import TelegramClient, events

import settings

client = TelegramClient(
    settings.TELEGRAM_SESSION_NAME,
    api_id=settings.TELEGRAM_API_ID,
    api_hash=settings.TELEGRAM_API_HASH,
).start(bot_token=settings.TELEGRAM_BOT_TOKEN)


@client.on(events.NewMessage(chats=settings.TELEGRAM_CHANNEL_NAME))
async def new_message_handler(event):
    event_json = event.to_dict()
    print(f"New message in {settings.TELEGRAM_CHANNEL_NAME}: {event_json}")

    # Send entire event JSON to FastAPI
    requests.post(settings.WEBHOOK_URL, json=event_json)


if (__name__ == '__main__'):
    client.run_until_disconnected()