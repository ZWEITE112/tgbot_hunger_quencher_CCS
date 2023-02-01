from aiogram import bot

def send_message(chat_id, text):
    bot.send_message(chat_id, text)