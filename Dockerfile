FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install OS dependencies (optional but safe for some packages)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy everything to the container
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "DiscordingWebsiteTestingBot.py"]
