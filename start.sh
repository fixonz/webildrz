#!/bin/bash
# Start the Flask Server in the background
gunicorn shapeshift_server:app --bind 0.0.0.0:$PORT --timeout 120 &

# Wait a second for gunicorn
sleep 2

# Start the Telegram Bot
python3 shapeshift_bot.py
