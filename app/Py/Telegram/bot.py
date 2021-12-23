from cryptography.fernet import Fernet
import telebot
import json
import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pendulum
import logging

from Database.main import pushToDb
from markups import createMarkupCalendar, createMarkupCategory, createMarkupPrice, ForceReply
from utils import TEXT_PRICE, TEXT_DONE

DEBUG_MODE = eval(os.getenv("DEBUG_MODE"))

def getToken():
    key = bytes(os.getenv("KEY"), "utf-8")
    encrypted = bytes(os.getenv("SECRET_TELEGRAM"), "utf-8")
    return json.loads(Fernet(key).decrypt(encrypted))["api_key"]

def createBot():
    TOKEN = getToken()

    bot = telebot.TeleBot(token=TOKEN)
    telebot.logger.setLevel(logging.DEBUG)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if call.data == "Ignore":
            bot.answer_callback_query(call.id, "Please select date")
        elif "Back" in call.data:
            bot.edit_message_text(
                text=call.message.text,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=createMarkupCalendar(eval(f"{call.data.split()[-1]}-1"))
            )
        elif "Next" in call.data:
            bot.edit_message_text(
                text=call.message.text,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=createMarkupCalendar(eval(f"{call.data.split()[-1]}+1"))
            )
        elif call.data == "Cancel":
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
        elif re.search(r'^\d{2}-\d{1,2}-\d{4}$', call.data):
            bot.answer_callback_query(call.id, f"You have selected {call.data}.")
            bot.edit_message_text(
                text=f"Choose Category @ {call.data}",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=createMarkupCategory(call.data)
            )
        else:
            # bot.answer_callback_query(call.id, f"You have selected {call.data}.")
            if "ENTER" in call.data:
                call.data = call.data.split("ENTER ")[1]
                number = call.data.split()[-1].strip('.')
                if '.' in number:
                    number = '{:0.2f}'.format(float(number))
                text = f"You have entered ${number} for {call.data.split()[1]} @ {call.data.split()[0]}\nEnter description: "
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(call.message.chat.id, text, reply_markup=ForceReply(selective=False))
            elif 'DEL' in call.data:
                call.data = call.data.split("DEL ")[1][:-1].strip('.')
                number = call.data.split()[2] if call.data[-1] != ' ' else ''
                bot.edit_message_text(
                    text=TEXT_PRICE.format(call.data.split()[1], call.data.split()[0])+number,
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=createMarkupPrice(call.data)
                )
            elif call.data in ['INVALID', 'IGNORE']:
                if call.data == 'INVALID':
                    bot.answer_callback_query(call.id, "Invalid operation, please select number or C")
                elif call.data == 'IGNORE':
                    pass
            else:
                if re.search(r'^\d{2}-\d{1,2}-\d{4} \w+ $', call.data):
                    bot.edit_message_text(
                        text=TEXT_PRICE.format(call.data.split()[1], call.data.split()[0]),
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        reply_markup=createMarkupPrice(call.data)
                    )
                else:
                    bot.edit_message_text(
                        text=TEXT_PRICE.format(call.data.split()[1], call.data.split()[0])+call.data.split()[2],
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        reply_markup=createMarkupPrice(call.data)
                    )

    @bot.message_handler(commands=['start'])
    def message_handler(message):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.send_message(message.chat.id, "Choose Date", reply_markup=createMarkupCalendar())

    # @bot.message_handler(func=lambda msg: msg)
    # def message_handler(message):
    #     pass
    
    @bot.message_handler(func=lambda message: 'reply_to_message' in vars(message).keys() and message.reply_to_message.json['from']['is_bot'] and "description" in message.reply_to_message.text)
    def message_handler(message):
        pattern = r'.*\$(\d+\.*\d*).* (.*) @ (.*)\n.*:(.*)'
        data = re.search(pattern, message.reply_to_message.text+message.text).groups()
        current = pendulum.now(tz='Asia/Singapore')
        # Edit/Delete Message
        bot.delete_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        if DEBUG_MODE:
            # import requests
            # response = requests.get('https://a731-42-61-160-251.ngrok.io')
            # print(vars(response))
            pushToDb(message, data, current)
            bot.send_message(
                text=TEXT_DONE.format(current.to_datetime_string()),
                chat_id=message.chat.id
            )
        else:
            try:
                # Push Data
                pushToDb(message, data, current)
                bot.send_message(
                    text=TEXT_DONE.format(current.to_datetime_string()),
                    chat_id=message.chat.id
                )
            except Exception as e:
                bot.send_message(
                    text=f"Data not pushed due to ({e})",
                    chat_id=message.chat.id
                )

    return bot

if __name__ == "__main__":
    bot = createBot()