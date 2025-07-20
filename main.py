from typing import Final

from random import choice
import os

from dotenv import load_dotenv

from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.ext import CallbackQueryHandler

from response import getReply
import json


#Load json data from replies.json
with open('replies.json', 'r', encoding='utf-8') as file:
    replies = json.load(file)

#.env file
load_dotenv()
Bot_Token: Final[str] = os.getenv('Bot_Token')
Bot_Username: Final = '@TabToss_Bot'

#KGC List
kgcList = ['Don', 'Joel', 'Imam', 'Qam']



#Commmands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Ready to pay the bill? (hopefully it\'s not you this time!)')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('use the toss command to see who\'s paying first!')

async def toss_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    personPaying = choice(kgcList)
    reply = getReply(personPaying)
    await update.message.reply_text(reply)



#main function to start the bot
if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(Bot_Token).build()

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('toss', toss_command))

    #Messages

#Polls the text (ensures previous handlers run)
    print('Polling.....')
    app.run_polling(poll_interval=3)
