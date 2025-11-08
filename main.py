from __future__ import annotations

from typing import Final, List

from random import choice

from dotenv import load_dotenv

from telegram import Update, BotCommand
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.ext import PicklePersistence #file based persistance
from telegram.ext import CallbackQueryHandler

from response import getReply

import os
import re

#.env file
load_dotenv()
Bot_Token: Final[str] = os.getenv('Bot_Token')
Bot_Username: Final = '@TabToss_Bot'

#.env error notice
if not Bot_Token:
    raise RuntimeError("Bot_Token not found.")

def _names_store(context: ContextTypes.DEFAULT_TYPE) -> List[str]:
    return context.chat_data.setdefault("names",[])

#Map lowercase name -> original index (first occurance).
def _case_index(names: List[str]) -> dict:
    idx = {}
    for i, n in enumerate(names):
        lower = n.casefold()
        if lower not in idx:
            idx[lower] = i
    return idx

#Collapse internal whitespace to a single space and strip ends.
def _normalize_spaces(s: str) -> str:
    return re.sub(r'\s+', " ", s).strip()

#Extract current name list from command message text
def _parse_names_args(raw_text: str) -> List[str]:
    parts = raw_text.split(maxsplit=1) #split off leading /command
    if len(parts) < 2:
        return[]
    payload = parts[1].strip()

    if "," in payload:
        tokens = [t.strip().strip(",") for t in payload.split(",")]
    else:
        tokens = [t.strip().strip(",") for t in payload.split()]
    
    #Clean space between token
    tokens = [_normalize_spaces(t) for t in tokens if t]
    return [t for t in tokens if t]


#Commmands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Hello! Ready to pay the bill? (hopefully it\'s not you this time!) \n' 
        'Use /help if this is you\'re unsure on how to toss.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'TabToss Commands:\n'
        '• /add Name1, Name2, Name3 - Add names into the list (commas support multi-word).\n'
        '• /list - View current names saved.\n'
        '• /remove Name1 - remove selected name (case-insensitive).\n'
        '• /clear - Empties current list. \n'
        '• /toss - Begin tossing and see who pays from the current list.')
    
async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    names = _names_store(context)
    tokens = _parse_names_args(update.message.text)
    if not tokens:
        await update.message.reply_text(
            "Usage: /add Name1, Name2, Name3 - Tip: use commas for multi-word"
        )
        return
    
    existing_lower = {n.casefold() for n in names}
    added, skipped = [], []

    for raw in tokens:
        name = re.sub(r"\s+", " ", raw).strip()
        if not name:
            continue
        key = name.casefold()
        if key in existing_lower:
            skipped.append(name)
        else:
            names.append(name)
            existing_lower.add(key)
            added.append(name)
    
    msg_lines = []
    if added:
        msg_lines.append(f"Added: {', '.join(added)}")
    if skipped:
        msg_lines.append(f"Skipped (already present): {', '.join(skipped)}")
    msg_lines.append(f"Total names: {len(names)}. Use /list to view")

    await update.message.reply_text("\n".join(msg_lines))

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    names = _names_store(context)
    if not names:
        await update.message.reply_text("The list is empty. Add some with the command /add ....")
        return
    lines = [f"{i+1}. {n}" for i, n in enumerate(names)]
    await update.message.reply_text("Current list:\n" + "\n".join(lines))

async def remove_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    names = _names_store(context)
    if not names:
        await update.message.reply_text("Nothing to remove - current list is empty")
        return
    
    #Parse names for /remove, payloads without commas are treated as a single name
    tokens = _parse_names_args(update.message.text)
    if not tokens:
        await update.message.reply_text(
            "Usage: /remove Name1 - pass one or more names (comma or space separated)."
        )
        return
    
    removed = []
    missing = []

    for nm in tokens:
        key = nm.casefold()
        found_index = next((i for i, val in enumerate(names) if val.casefold() == key), None)
        if found_index is not None:
            removed.append(names.pop(found_index))
        else:
            missing.append(nm)
    
    if removed:
        lines = [f"Removed: {', '.join(removed)}", f" Total names now: {len(names)}."]
        if missing:
            lines.append(f"Not found: {', '.join(missing)}")
        await update.message.reply_text("".join(lines))
    else:
        await update.message.reply_text("No matching names were found.")

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    names = _names_store(context)
    if not names:
        await update.message.reply_text("The list is already empty.")
        return
    count = len(names)
    names.clear()
    await update.message.reply_text(f"Cleared {count} name(s). The list is now empty.")


async def toss_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    names = _names_store(context)
    if not names:
        await update.message.reply_text(
            "You don't have any names yet! Add some with the /add command (/add Name1, Name2 ...)"
        )
        return
    
    personPaying = choice(names)
    reply = getReply(personPaying)
    await update.message.reply_text(reply)


#main function to start the bot
if __name__ == '__main__':
    print('Starting bot...')

    #Pickle storage for file-based persistance
    #Survive restarts
    try:
        from telegram.ext import PicklePersistence
    except Exception:
        from telegram.ext import persistence as PicklePersistence
    
    persistence = PicklePersistence(filepath='tabtoss.pickle')

    app = ( Application.builder()
           .token(Bot_Token)
           .persistence(persistence)
           .build()) 

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('add', add_command))
    app.add_handler(CommandHandler('list', list_command))
    app.add_handler(CommandHandler('names', list_command)) #alias
    app.add_handler(CommandHandler('remove', remove_command))
    app.add_handler(CommandHandler('clear', clear_command))
    app.add_handler(CommandHandler('toss', toss_command))


#Polls the text (ensures previous handlers run)
    print('Polling.....')
    app.run_polling(poll_interval=3)
