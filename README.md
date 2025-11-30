# 📱TabTossBot
Stuck on who wants to front the bill first? This Telegram bot helps you decide who pays the bill! No awkward discussion needed. TabToss randomly picks one member of the group so you can focus on chilling, not arguing over checks, but I guess you still have to discuss who’s paying for what 🤷

## 🛠️ Technology
- `Python`
- `botfather`
- `JSON`
- `.env`

## 🚀 Features
- **Randomised bill-payer selection** - choose a “loser” who pays the bill, picked at random from the group
- **Group-friendly interaction** - works in group chats, handles commands or triggers to pick someone
- **Lightweight and easy to customise** - since data (member list, options) are in JSON, you can tweak behaviour without touching core code
- **Easy to deploy** - runs on any machine that supports Python and the Telegram Bot API

## 🧠 The Process
I built TabTossBot because I was tired of having the “who pays?” debate whenever my friends and I hang out. I wanted something simple, a bot that could instantly pick someone randomly and fairly. I chose Python to work with the Telegram Bot API wrapper, as that is the language I am comfortable with. I chose Telegram over other chats such as Discord as it gives a clean API for bot, and it’s widely used, more than Discord.

I opted for storing pre-written reply data in JSON files - that way, it’s easy to add or remove sentences. The bot reads from these JSON files at runtime, picks a random user when triggered, and sends the result as a message. This minimal, data-driven design keeps the bot simple, flexible, and easy to maintain.

## 📦 Running the Project
1. Clone or download the repository
2. Create your `.env` (or config) file and add your Telegram bot token from BotFather
3. Install dependencies
4. Run the bot: main.py
5. On Telegram, add the bot to your group or chat

## 🖼️ Preview
![Image](https://github.com/user-attachments/assets/18ef9c1c-f2dd-4fe0-aadd-8c3a0fca5d1a)
