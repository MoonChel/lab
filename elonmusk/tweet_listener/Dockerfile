# Use an official Python image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Telethon script
COPY app.py .

# Expose no ports as this runs as a client
CMD ["python", "app.py"]