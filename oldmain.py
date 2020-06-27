from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
import os


api = "https://api.rootnet.in/covid19-in/stats/latest"
res = requests.get(api).json()

summary = res['data']['unofficial-summary'][0]

total_cases = summary['total']
total_recovered = summary['recovered']
total_deaths = summary['deaths']
total_active = summary['active']
regional_data = res['data']['regional']
total_states = int(len(regional_data))


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        f'Welcome to Covid19 Tracker BOT.\nEnter /help to see Commands ')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("/stats - Check Overall Stats\n\
/state - Check cases of States & UT's ")


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text("Please Select Only From Commands")


def stats(update, context):
    """ COVID CASES UPDATE """
    total_data = f"Total Confirmed Cases : {total_cases:,}\nTotal Active Cases : {total_active:,}\nTotal Recovered : {total_recovered:,}\nTotal Deaths : {total_deaths:,}"
    update.message.reply_text(total_data)


def allstate(update, context):
    """ STATEWISE COVID CASES """
    for data in range(total_states):

        state_wise_data = f"State / UT : {regional_data[data]['loc']}\n\
Active Indian Cases: {regional_data[data]['confirmedCasesIndian']:,}\n\
Active Foreign Cases : {regional_data[data]['confirmedCasesForeign']:,}\n\
Total : {regional_data[data]['totalConfirmed']:,}\n\
Recovered : {regional_data[data]['discharged']:,}\n\
Deaths : {regional_data[data]['deaths']:,}\n\n"

        update.message.reply_text(state_wise_data)

    update.message.reply_text(
        "* * * * * * * * * * * * * *")


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    updater = Updater(
        BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CommandHandler("state", allstate))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
