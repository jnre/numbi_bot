#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                            RegexHandler, ConversationHandler,PicklePersistence)
from uuid import uuid4

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY = range(2)

#reply_keyboard=[['Age','Favourite color'],['Number of siblings','Something else...'],['Done']]
reply_keyboard1=[['/setnum'],['/getnum'],['/donenum']]
markup = ReplyKeyboardMarkup(reply_keyboard1,one_time_keyboard=True)



# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def facts_to_str(chat_data):
    facts = list()

    for key, value in chat_data.items():
        facts.append('{}-{}'.format(key,value))
    return "\n".join(facts).join(['\n','\n'])

# def start(bot, update):
#     reply_keyboard = [['Boy','Girl','Other']]
#     #update.message.reply_text('Hi! use /set to set num')
#     update.message.reply_text(
#         'HI! send /cancel to stop talking t o me.\n\n'
#             'Are you a boy or a girl?',reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True))
#     return GENDER

def start(update,context):
    update.message.reply_text('what u want?',reply_markup=markup)

    return CHOOSING

def set_choice(update,context):
        
    #theres only 1 choice-"Get number" as the key, but good for documentation, can pass in more keys to choice
    #stored from text which is passed thru replykeyboard1
    update.message.reply_text('whats the number?')

    #goes to typing mode to type the number, received_information
    return TYPING_REPLY


def get_choice(update,context):

    #text refers to "Get Number", test to see if Get Number already exist

    text = update.message.text
    if not context.chat_data.get('Get Number'):
        update.message.reply_text('number does not exist!',reply_markup=markup)
    
    else:
        update.message.reply_text('{}'.format(facts_to_str(context.chat_data)),reply_markup=markup)
    
    return CHOOSING


def received_information(update, context):
 
    
    #only 1 category, text here is the number
    text = update.message.text
    #i think lower means lower caps, text(no data) passed into category "Get Number"
    context.chat_data['Get Number'] = text.lower()

    update.message.reply_text("{} " .format(facts_to_str(context.chat_data)),
                              reply_markup=markup)

    return CHOOSING




def done(update, context):
    #if 'choice' in context.chat_data:
        #del context.chat_data['choice']

    update.message.reply_text("Until next time!")
    return ConversationHandler.END

def error(bot,update,error):
    """Log errors by updates"""
    logger.warning('Update "%s" caused error "%s"',update.error)


def main():
    """Start the bot."""
    pp = PicklePersistence(filename='conversationbot')
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("816699585:AAEgE2t4h2kHxqZMVf3vZ8TnT4hG9cW5uOQ",persistence =pp,use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    conv_handler = ConversationHandler(entry_points=[CommandHandler('startnum',start)],
                #states when return from previous function such that its waiting for a response from function def inside it
                    states={

                        CHOOSING: [MessageHandler(Filters.regex('/setnum'),set_choice),
                                    MessageHandler(Filters.regex('/getnum'),get_choice)],
                        

                        TYPING_REPLY: [MessageHandler(Filters.text,received_information)]
                    },

                    

                    fallbacks=[MessageHandler(Filters.regex('/donenum'),done)],
                    name="my_conversation",
                    persistent=True
    
    )
    
    
    
    
    
    
    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
