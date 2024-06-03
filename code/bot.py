#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.


MYTOKEN = "7279938443:AAEtnngk3-sVJi5S4GqS5f2b76zq5kmPvss"
INTERVAL_MINUTE = 1

import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import datetime
import os
import re

def check_time_for_syntax(chosen_time):
    pattern = r"\b\d{4}-\d{2}-\d{2}_\d{1,2}_\d{1,2}\b"
    res = re.search(pattern,chosen_time)
    if res:
        return True
    else:
        return False

def get_current_time():
    global INTERVAL_MINUTE
    current_day = str(datetime.date.today())
    temp_time_obj = datetime.datetime.now()
    current_time = str(temp_time_obj.hour) + "_" + str(temp_time_obj.minute - temp_time_obj.minute % INTERVAL_MINUTE)
    final_string = current_day + "_" + current_time
    return final_string 

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def water_off_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    water_command_exists = os.path.isfile(f"../data/command/water.txt")
    if water_command_exists:
        os.remove(f"../data/command/water.txt")

    # os.mknod(f"../command/water.txt")
    with open(f"../data/command/water.txt",'a') as file:
        file.write('0')

    await update.message.reply_text("water turned off!")


async def water_on_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    water_command_exists = os.path.isfile(f"../data/command/water.txt")
    if water_command_exists:
        os.remove(f"../data/command/water.txt")

    # os.mknod(f"../command/water.txt")
    with open(f"../data/command/water.txt",'a') as file:
        file.write('1')

    await update.message.reply_text("water activated!")

async def log_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    argsProvided = False # we can check whether the user provided us with a time
    # as an input or not
    try:
        args = context.args[0]
        argsProvided = True
        print(f'args: {args}')
    except IndexError:
        argsProvided = False
    

    current_time = get_current_time()
    if argsProvided:
        chosen_time = args
    else:
        chosen_time = current_time

    print(f"chosen time for log: {chosen_time}")
    syntax_check = check_time_for_syntax(chosen_time)
    if syntax_check:
        moisture_exists = os.path.isfile(f"../data/moisture/{chosen_time}.txt")
        temperature_exists = os.path.isfile(f"../data/temperature/{chosen_time}.txt")
        print(f"moisture_exists: {moisture_exists}\ntemperature_exists: {temperature_exists}")

        final_string = ""

        if moisture_exists:
            with open(f"../data/moisture/{chosen_time}.txt") as moisture_text_file:
                last_moisture = moisture_text_file.read()
                print(f"last_moisture: {last_moisture}")
                final_string += f"last recorded moisture: {last_moisture}\n"

        if temperature_exists:
            with open(f"../data/temperature/{chosen_time}.txt") as temperature_text_file:
                last_temperature = temperature_text_file.read()
                print(f'last_temperature: {last_temperature}')
                final_string += f"last recorded temperature: {last_temperature}\n"

        if temperature_exists == False and moisture_exists == False:
            final_string = "No data exists yet..."
        
        await update.message.reply_text(final_string)

    else:
        await update.message.reply_text("pattern isn't right, you input must be in form of 'year-month-day_hour_minute'")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    global MYTOKEN
    application = Application.builder().token(MYTOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("log", log_command))
    application.add_handler(CommandHandler("water_on", water_on_command))
    application.add_handler(CommandHandler("water_off", water_off_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()