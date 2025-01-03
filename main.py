import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from datetime import datetime, timedelta

# Replace with your bot token and chat ID
BOT_TOKEN = '7656848916:AAHW9pt1dy3n_GwxP50vsK6RVWElccv0EhA'
CHAT_ID = '1957863650'

# Dictionary to store user click status (In-memory)
clicked_users = {}


# Function to send the message (asynchronous)
async def send_message():
    bot = Bot(token=BOT_TOKEN)
    message = "Hier finden Sie den täglichen Link: [Click here](https://example.com)"

    # Await the send_message method
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
    print(f"Message sent at {datetime.now()}")


# Function to schedule messages for 20 days
async def schedule_messages():
    start_time = datetime.now().replace(second=0, microsecond=0)  # Start now
    daily_time = start_time.replace(hour=9, minute=00)  # Schedule for 00:18 daily

    for day in range(20):  # Loop for 20 days
        now = datetime.now()
        # If the current time is past the daily_time, schedule it for tomorrow
        if now > daily_time:
            daily_time += timedelta(days=1)

        # Calculate the delay until the next scheduled time
        delay = (daily_time - now).total_seconds()
        print(f"Scheduling message {day + 1} for {daily_time}. Waiting for {delay} seconds...")

        # Await the sleep until it's time to send the next message
        await asyncio.sleep(delay)

        # Send the message asynchronously
        await send_message()

        # Move to the next day
        daily_time += timedelta(days=1)


# Function to send a message with a link and track if a user clicks it
async def start(update, context):
    # Inline button with a URL
    keyboard = [
        [InlineKeyboardButton("Click here!", url="https://example.com")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Here is your daily link, click it!", reply_markup=reply_markup)


# Callback function to track when a user clicks the button
async def button(update, context):
    user_id = update.callback_query.from_user.id

    # Mark the user as having clicked the link
    clicked_users[user_id] = True

    # Acknowledge the callback query
    await update.callback_query.answer(text="You clicked the link!")

    # Send a message confirming the action
    await context.bot.send_message(chat_id=user_id, text="Thanks for clicking the link!")


# Command to check if the user has clicked the link
async def status(update, context):
    user_id = update.message.from_user.id
    if clicked_users.get(user_id):
        await update.message.reply_text("You have already clicked the link!")
    else:
        await update.message.reply_text("You haven't clicked the link yet. Use /start to click!")


# Start the scheduling in an asynchronous event loop
async def start_bot():
    print("Bot started. Scheduling messages for 20 days...")
    await asyncio.gather(
        schedule_messages()
    )


# Set up the Application and Dispatcher for status and start commands
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers for /start, /status, and button press callback
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('status', status))
    application.add_handler(CallbackQueryHandler(button))

    # Start scheduling and running the bot asynchronously
    asyncio.run(start_bot())

    # Start the bot and polling for updates
    application.run_polling()


if __name__ == "__main__":
    main()
