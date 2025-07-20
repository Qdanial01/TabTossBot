from random import choice
import json

with open('replies.json', 'r', encoding='utf-8') as file:
    replies = json.load(file)

def getReply(reply: str) -> str:
    return choice(replies).format(reply)