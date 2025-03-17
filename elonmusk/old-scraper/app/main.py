import re
import json
from datetime import datetime
from telethon import TelegramClient
from prometheus_client import Counter

import app.settings as settings

# Define the counter with multiple labels
tweet_counter = Counter(
    "telegram_tweets_total",
    "Total tweets processed",
    ["type"]
)

# Telegram API credentials
channel_username = "elon_alerts"

# Load last message ID (to avoid reprocessing old messages)
def load_last_message_id():
    try:
        with open(settings.LAST_MESSAGE_FILE, "r") as f:
            return json.load(f).get("last_message_id", None)
    except FileNotFoundError:
        return None

def save_last_message_id(message_id):
    data = {"last_message_id": message_id}
    with open(settings.LAST_MESSAGE_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Message classification
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

def cleanup_text(m):
    return m.replace('\n\n[View on 𝕏]()', '')

def scrape_new_messages():
    # Regex pattern to match Twitter/X links
    pattern = r"https?://(?:twitter\.com|x\.com)/[^\s)\]\.]+"

    with TelegramClient(
        settings.TELEGRAM_SESSION_NAME,
        settings.TELEGRAM_API_ID,
        settings.TELEGRAM_API_HASH,
    ) as client:
        last_message_id = load_last_message_id()
        new_messages = []

        all_messages = []

        for message in client.iter_messages(channel_username, reverse=True):
            if last_message_id and message.id <= last_message_id:
                break

            if message.text:
                msg_type = classify_message(message.text)
                links = re.findall(pattern, message.text)
                cleaned_text = re.sub(pattern, "", message.text).strip()
                text, link = cleaned_text, links[0] if links else None

                new_messages.append(message.id)

                all_messages.append({
                    'id': message.id,
                    'text': cleanup_text(text),
                    'link': link,
                    'type': msg_type,
                    'date': datetime.timestamp(message.date),
                    'human_date': str(message.date)
                })

                tweet_counter.labels(type=msg_type).inc()

        if new_messages:
            save_last_message_id(new_messages[0])

        with open('tweets.json', 'r') as tweets_file:
            old_tweets = json.load(tweets_file)

        with open('tweets.json', 'w') as tweets_file:
            json.dump(all_messages + old_tweets, tweets_file, indent=4)

