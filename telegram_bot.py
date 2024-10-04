import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, ConversationHandler
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s', level=logging.INFO)

# Google Sheets configuration
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('rise-and-shine-challenge-1b9588a74d54.json', scope)
client = gspread.authorize(creds)

# Open the spreadsheet by its title (the title you see in Google Sheets)
spreadsheet = client.open('testing')  # Use the name of your spreadsheet here

# Access the specific worksheets (tabs)
form_sheet = spreadsheet.worksheet('Form')  # Accessing the tab named 'Form'
leaderboard_sheet = spreadsheet.worksheet('Leaderboard')  # Accessing the tab named 'Leaderboard'

# Telegram Bot configuration
TOKEN = 'Replace with your bot token'  # Replace with your bot token
app = Application.builder().token(TOKEN).build()

# Conversation states
NAME, EMAIL, PRAYER_STATUS = range(3)

# Command to get the leaderboard
async def leaderboard(update: Update, context: CallbackContext):
    leaderboard_data = leaderboard_sheet.get_all_values()[1:]  # Skip header row
    if not leaderboard_data:  # Check if there is data
        await update.message.reply_text("No data available in the leaderboard.")
        return

    leaderboard_message = "Leaderboard:\n"
    
    # Sort the leaderboard data by points (assuming points are in column B)
    leaderboard_data.sort(key=lambda x: int(x[1]), reverse=True)  # Sort by total points in descending order

    for row in leaderboard_data:
        email = row[0]  # Assuming email is in the first column (index 0)
        points = row[1]  # Assuming points are in the second column (index 1)

        # Append to the leaderboard message
        leaderboard_message += f"{email}: {points} points\n"

    await update.message.reply_text(leaderboard_message)

# Command to send form link or sorry message based on the time
async def form(update: Update, context: CallbackContext):
    now = datetime.datetime.now()
    start_time = datetime.time(5, 0)  # 5:00 AM
    end_time = datetime.time(6, 0)  # 6:00 AM

    if start_time <= now.time() <= end_time:
        # Start the conversation
        await update.message.reply_text("Good Morning! Please enter your name:")
        return NAME
    else:
        # Out of time
        await update.message.reply_text("Sorry, you are out of time. Please submit your form tomorrow.")
        return ConversationHandler.END

# Handle user name input
async def handle_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text  # Store the name
    await update.message.reply_text("Please enter your email:")
    return EMAIL

# Handle user email input
async def handle_email(update: Update, context: CallbackContext):
    context.user_data['email'] = update.message.text  # Store the email
    await update.message.reply_text("Did you complete your prayer? (Yes/No)")
    return PRAYER_STATUS

# Handle prayer status input and prevent multiple submissions in a day
async def handle_prayer_status(update: Update, context: CallbackContext):
    email = context.user_data['email']
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Get all the data from the 'Form' sheet
    form_data = form_sheet.get_all_values()
    
    # Check if the user has already submitted today
    for row in form_data:
        submission_date = row[0].split()[0]  # Extract date part from timestamp
        submitted_email = row[1]  # Assuming email is in the second column (index 1)
        
        if submitted_email == email and submission_date == today:
            # User has already submitted today
            await update.message.reply_text("You have already submitted the form today. Please try again tomorrow.")
            return ConversationHandler.END
    
    # If no submission found for today, proceed with saving the data
    context.user_data['prayer_status'] = update.message.text  # Store prayer status

    # Save to Google Sheets
    form_sheet.append_row([
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Timestamp
        email,
        context.user_data['name'],
        context.user_data['prayer_status']
    ])

    await update.message.reply_text("Thank you for your submission!")
    return ConversationHandler.END

# Function to start the bot and display available commands
async def start(update: Update, context: CallbackContext):
    commands = (
        "/form - Get the form (available between 5 AM and 6 AM)\n"
        "/leaderboard - View the current leaderboard\n"
        "/start - Welcome message and available commands"
    )
    welcome_message = f"Welcome to the Rise and Shine Challenge!\n\nAvailable commands:\n{commands}"
    await update.message.reply_text(welcome_message)

# Main function to add handlers and run the bot
def main():
    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('form', form)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email)],
            PRAYER_STATUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_prayer_status)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('leaderboard', leaderboard))
    app.add_handler(CommandHandler('start', start))
    
    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()
