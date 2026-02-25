#!/bin/bash
# Start the Flask Server in the background
gunicorn shapeshift_server:app --bind 0.0.0.0:$PORT &

# Start the Telegram Bot
python shapeshift_bot.py
