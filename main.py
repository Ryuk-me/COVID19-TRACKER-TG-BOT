#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards.
"""
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import requests
import json
import os

my_states = ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand',
             'Karnataka', 'Kerala', 'Ladakh', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']

my_new_list = ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Delhi', 'Dadra and Nagar Haveli and Daman and Diu', 'Goa', 'Gujarat', 'Himachal Pradesh', 'Haryana', 'Jharkhand', 'Jammu and Kashmir', 'Karnataka', 'Kerala',
               'Ladakh', 'Lakshadweep', 'Maharashtra', 'Meghalaya', 'Manipur', 'Madhya Pradesh', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Puducherry', 'Rajasthan', 'Sikkim', 'Telangana', 'Tamil Nadu', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']


api2 = "https://api.covid19india.org/v2/state_district_wise.json"
res2 = requests.get(api2).json()


api = "https://api.rootnet.in/covid19-in/stats/latest"
res = requests.get(api).json()

summary = res['data']['unofficial-summary'][0]

total_cases = summary['total']
total_recovered = summary['recovered']
total_deaths = summary['deaths']
total_active = summary['active']
regional_data = res['data']['regional']
total_states = int(len(regional_data))
date = res['lastRefreshed']
date_time = date[0:10].replace('-', '/') + "   "+date[12:19]
last_update = "Last Updated on : "+str(date_time)

stats_all = f"Total Confirmed Cases : {total_cases:,}\nTotal Active Cases : {total_active:,}\nTotal Recovered : {total_recovered:,}\nTotal Deaths : {total_deaths:,}"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        f'Welcome to Covid19 Tracker BOT.\nEnter /help to see Commands ')


def stats(update, context):
    """ It will send Stats On running """
    update.message.reply_text(stats_all+"\n"+last_update)


def state_wise(update, context):
    keyboard = [[InlineKeyboardButton("Andaman & Nicobar", callback_data='Andaman and Nicobar Islands'),
                 InlineKeyboardButton("Andhra Pradesh", callback_data='Andhra Pradesh')],

                [InlineKeyboardButton('Arunachal Pradesh', callback_data='Arunachal Pradesh'),
                 InlineKeyboardButton('Assam', callback_data='Assam')],

                [InlineKeyboardButton('Bihar', callback_data='Bihar'),
                 InlineKeyboardButton('Chandigarh', callback_data='Chandigarh')],

                [InlineKeyboardButton(
                    'Chhattisgarh', callback_data='Chhattisgarh'),
                 InlineKeyboardButton('Delhi', callback_data='Delhi')],

                [InlineKeyboardButton('Dadra and Nagar Haveli and Daman and Diu', callback_data='Dadra and Nagar Haveli and Daman and Diu'),
                 InlineKeyboardButton('Goa', callback_data='Goa')],

                [InlineKeyboardButton('Gujarat', callback_data='Gujarat'),
                 InlineKeyboardButton('Himachal Pradesh', callback_data='Himachal Pradesh')],

                [InlineKeyboardButton('Haryana', callback_data='Haryana'),
                 InlineKeyboardButton('Jharkhand', callback_data='Jharkhand')],

                [InlineKeyboardButton('Jammu and Kashmir', callback_data='Jammu and Kashmir'),
                 InlineKeyboardButton('Karnataka', callback_data='Karnataka')],

                [InlineKeyboardButton('Kerala', callback_data='Kerala'),
                 InlineKeyboardButton('Ladakh', callback_data='Ladakh')],

                [InlineKeyboardButton(
                    'Maharashtra', callback_data='Maharashtra')],

                [InlineKeyboardButton('Meghalaya', callback_data='Meghalaya'),
                 InlineKeyboardButton('Manipur', callback_data='Manipur')],

                [InlineKeyboardButton('Madhya Pradesh', callback_data='Madhya Pradesh'),
                 InlineKeyboardButton('Mizoram', callback_data='Mizoram')],

                [InlineKeyboardButton('Nagaland', callback_data='Nagaland'),
                 InlineKeyboardButton('Odisha', callback_data='Odisha')],

                [InlineKeyboardButton('Punjab', callback_data='Punjab'),
                 InlineKeyboardButton('Puducherry', callback_data='Puducherry')],

                [InlineKeyboardButton('Rajasthan', callback_data='Rajasthan'),
                 InlineKeyboardButton('Sikkim', callback_data='Sikkim')],

                [InlineKeyboardButton('Telangana', callback_data='Telangana'),
                 InlineKeyboardButton('Tamil Nadu', callback_data='Tamil Nadu')],

                [InlineKeyboardButton('Tripura', callback_data='Tripura'),
                 InlineKeyboardButton('Uttar Pradesh', callback_data='Uttar Pradesh')],

                [InlineKeyboardButton('Uttarakhand', callback_data='Uttarakhand'),
                 InlineKeyboardButton('West Bengal', callback_data='West Bengal')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Select State\n", reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    if query.data in my_states:
        # print(my_states.index(query.data))
        index = my_states.index(query.data)

        state_wise_data = f"State / UT : {regional_data[index]['loc']}\n\
Active Indian Cases : {regional_data[index]['confirmedCasesIndian']:,}\n\
Active Foreign Cases : {regional_data[index]['confirmedCasesForeign']:,}\n\
Total : {regional_data[index]['totalConfirmed']:,}\n\
Recovered : {regional_data[index]['discharged']:,}\n\
Deaths : {regional_data[index]['deaths']:,}"

    if query.data in my_new_list:
        new_index = my_new_list.index(query.data)
        # print(new_index)
        district_name_data = []
        for i in range(0, len(res2[new_index+1]["districtData"])):
            district = ("\nDistrict : " + res2[new_index+1]["districtData"][i]["district"] +
                        " \nActive : "+str(res2[new_index+1]["districtData"][i]['active'])+" \nRecovered : "+str(res2[new_index+1]["districtData"][i]['recovered'])+" \nDeaths : "+str(res2[new_index+1]["districtData"][i]['deceased']))

            district_name_data.append(district)

        join = '\n'.join(district_name_data)
        last_data = f"{state_wise_data}\n{join}\n\n{last_update}"
        query.edit_message_text(last_data)


def allstate(update, context):
    """ STATEWISE COVID CASES """
    for data in range(total_states):

        state_wise_data = f"State / UT : {regional_data[data]['loc']}\n\
Active Indian Cases : {regional_data[data]['confirmedCasesIndian']:,}\n\
Active Foreign Cases : {regional_data[data]['confirmedCasesForeign']:,}\n\
Total : {regional_data[data]['totalConfirmed']:,}\n\
Recovered : {regional_data[data]['discharged']:,}\n\
Deaths : {regional_data[data]['deaths']:,}\n\n"

        update.message.reply_text(state_wise_data)

    update.message.reply_text(last_update)


def help_command(update, context):
    update.message.reply_text("/stats - Check Overall Stats\n\
/state - Choose cases States & UT's\n\
/allstate - To Check All state Cases ")


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text("Please Select Only From Commands")


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    updater = Updater(
        BOT_TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(CommandHandler('stats', stats))
    updater.dispatcher.add_handler(CommandHandler('state', state_wise))
    updater.dispatcher.add_handler(CommandHandler('allstate', allstate))

    # on noncommand i.e message - echo the message on Telegram
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
