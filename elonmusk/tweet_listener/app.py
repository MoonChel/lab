from telethon import TelegramClient, events

# Get these from https://my.telegram.org
api_id = "your_api_id"
api_hash = "your_api_hash"
channel_username = "your_channel_name"  # Example: "t.me/examplechannel" -> "examplechannel"

client = TelegramClient("session_name", api_id, api_hash)

@client.on(events.NewMessage(chats=channel_username))
async def new_message_handler(event):
    print(f"New message in {channel_username}: {event.text}")

    # You can send this message to FastAPI here
    import requests
    requests.post("http://127.0.0.1:8000/telegram-webhook/", json={"message": event.text})

client.start()
client.run_until_disconnected()