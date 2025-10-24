#!/bin/bash

# Start Flask web app in background
echo "Starting Flask web interface..."
gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 app:app &

# Wait a moment for Flask to start
sleep 2

# Start Telegram bot
echo "Starting Telegram bot..."
python main.py
