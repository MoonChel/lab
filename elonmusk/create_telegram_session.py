import asyncio
from telethon import TelegramClient
from app import settings

async def get_telegram_me():
    tclient = TelegramClient(
        settings.TELEGRAM_SESSION_NAME,
        settings.TELEGRAM_API_ID,
        settings.TELEGRAM_API_HASH
    )
    await tclient.start()
    await tclient.disconnect()

# To run the async function
if __name__ == "__main__":
    asyncio.run(get_telegram_me())