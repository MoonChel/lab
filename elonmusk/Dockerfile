# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary files to the container
COPY requirements.txt /app/requirements.txt
COPY app /app/app
COPY create_telegram_session.py /app/create_telegram_session.py
COPY last_message_id.json /app/last_message_id.json
COPY scrape_telegram_tweets.py /app/scrape_telegram_tweets.py

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set environment variables (optional, depending on your needs)
# ENV VARIABLE_NAME value

# Command to run the application
CMD ["python", "app/scrape_telegram_tweets.py"]