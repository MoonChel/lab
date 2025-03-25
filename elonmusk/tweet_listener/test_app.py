import asyncio
import settings

from telethon import TelegramClient, events
from telethon.sessions import StringSession

client = TelegramClient(
    StringSession(settings.TELEGRAM_SESSION_TOKEN),
    api_id=settings.TELEGRAM_API_ID,
    api_hash=settings.TELEGRAM_API_HASH,
).start()


async def get_channel_id():
    entity = await client.get_entity(settings.TELEGRAM_CHANNEL_NAME)
    print(f"Channel ID: {entity.id}")

@client.on(events.NewMessage(chats=["@elon_alerts", "@test_channel_elon"]))
async def new_message_handler(event):
    print(client.session.save())
    print(event)

# loop = asyncio.new_event_loop()
# loop.run_until_complete(get_channel_id())
client.run_until_disconnected()
