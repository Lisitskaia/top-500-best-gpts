# Telegram Reminder Bot

This directory contains a simple Telegram bot for creating reminders using the
`python-telegram-bot` library.

## Setup
1. Install dependencies:
   ```bash
   pip install python-telegram-bot
   ```
2. Set the `TELEGRAM_TOKEN` environment variable with your bot token.
3. Run the bot:
   ```bash
   python reminder_bot.py
   ```

## Commands
- `/start` – Display instructions.
- `/remind <minutes> <message>` – Schedule a reminder after the given minutes.
- `/list` – Show active reminders.
- `/cancel` – Cancel all active reminders.
