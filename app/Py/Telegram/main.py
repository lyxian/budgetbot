from cryptography.fernet import Fernet
import requests
import telebot
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def getToken():
    key = bytes(os.getenv("KEY"), "utf-8")
    encrypted = bytes(os.getenv("SECRET_TELEGRAM"), "utf-8")
    return json.loads(Fernet(key).decrypt(encrypted))["api_key"]

def createBot():
    TOKEN = getToken()

    bot = telebot.TeleBot(token=TOKEN)

    @bot.message_handler(commands=["join"])
    def _join(message):
        # Add user to Redis DB (pk = username)
        pass

    @bot.message_handler(commands=["quit"])
    def _quit(message):
        # Remove user from Redis DB
        pass

    @bot.message_handler(commands=['add'])
    def _add(message):
        # Provide custom keyboard for category
        # Input: Time, Type, Cost
        pass

    return bot

if __name__ == "__main__":
    bot = createBot()