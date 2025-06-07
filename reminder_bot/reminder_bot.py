import asyncio
from datetime import timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Dictionary to store reminders per user
reminders = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Use /remind <minutes> <message> to set a reminder."
    )

async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /remind <minutes> <message>")
        return

    try:
        minutes = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Minutes must be a number.")
        return

    message = ' '.join(context.args[1:])
    chat_id = update.effective_chat.id
    job = context.job_queue.run_once(
        send_reminder,
        when=timedelta(minutes=minutes),
        data={'chat_id': chat_id, 'text': message}
    )
    reminders.setdefault(chat_id, []).append(job)
    await update.message.reply_text(f"Reminder set in {minutes} minutes.")

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    await context.bot.send_message(job_data['chat_id'], text=job_data['text'])

async def list_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    jobs = reminders.get(chat_id, [])
    if not jobs:
        await update.message.reply_text("No active reminders.")
        return
    msgs = [f"{i+1}. {job.data['text']}" for i, job in enumerate(jobs)]
    await update.message.reply_text('\n'.join(msgs))

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    jobs = reminders.get(chat_id, [])
    for job in jobs:
        job.schedule_removal()
    reminders[chat_id] = []
    await update.message.reply_text("Canceled all reminders.")

async def main():
    import os
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("Please set the TELEGRAM_TOKEN environment variable.")
        return
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("remind", remind))
    application.add_handler(CommandHandler("list", list_reminders))
    application.add_handler(CommandHandler("cancel", cancel))

    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
