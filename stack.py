#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import flask
import telebot
import os
import time
import main

from flask import Flask

server = Flask(__name__)
token = os.getenv('TOKEN')
url_heroku = os.getenv('URL')
bot = telebot.TeleBot(token)
print(bot.get_me())


def log(message, answer):
    print("\n -----")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2}) \n Текст - {3}".format(message.from_user.first_name,
                                                                   message.from_user.last_name,
                                                                   str(message.from_user.id), message.text))
    print(answer)


@bot.message_handler(content_types=['contact'])
def handle_text(message):
    if message.contact:
        rr = message.contact.phone_number
        rrr = message.contact.first_name
        bot.send_contact(chat_id=-1001279911742, first_name=rrr, phone_number=rr)
        bot.send_message(chat_id=-1001279911742, text='YO!')
        print(message.contact.phone_number)
    else:
        print('telephone_to_me')


@bot.message_handler(commands=['start'])
def hendle_start(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    url_button1 = telebot.types.InlineKeyboardButton(text="Buy bot!", callback_data='b')
    keyboard.row(url_button1)
    bot.send_message(message.chat.id, 'Yo, ' + message.from_user.first_name + '! Send photo and enjoy (:',
                     reply_markup=keyboard)
    answer = "menu"
    log(message, answer)


@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    if call.message:
        if call.data == 'b':
            user_markup = telebot.types.ReplyKeyboardMarkup(True)
            phone = telebot.types.KeyboardButton(text='電話', request_contact=True)
            user_markup.row(phone)
            bot.send_message(call.from_user.id, 'Click button - 電話', reply_markup=user_markup)
        else:
            print('No call')


@bot.message_handler(content_types=['photo'])
def handle_text(message):
    if message.photo:
        markup = telebot.types.ForceReply(selective=False)
        raw = message.photo[-1].file_id
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        answer = "send_photo"
        log(message, answer)
        with open(f'img/' + str(message.from_user.id) + '.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)
        print(message.photo[-1].file_id + '.jpg')
        bot.send_message(message.chat.id, "send me level compression 1-15", reply_markup=markup)


def compression_on(level, chat_id, user_id):
    if 1 <= level <= 15:
        level_up = int(2 + level)
        print(level_up, chat_id, user_id, "level_is_ok")
        app = main.ArtConverter(user_id, level_up)
        app.run()
        img = open(f'out/' + user_id + '.jpg', 'rb')
        bot.send_photo(chat_id, photo=img)
    else:
        markup = telebot.types.ForceReply()
        bot.send_message(chat_id, "send me level compression 1-10", reply_markup=markup)
        answer = "bad answer_level"
        log(level, answer)
        time.sleep(5)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "йо":
        bot.send_message(message.chat.id, 'q')
        answer = "йо"
        log(message, answer)
    elif message.reply_to_message.text == "send me level compression 1-15":
        answer = "reply"
        print(message.text)
        level_set = int(message.text)
        chat_id_set = int(message.chat.id)
        user_id_set = str(message.from_user.id)
        compression_on(level_set, chat_id_set, user_id_set)
        log(message, answer)

    else:
        bot.send_message(message.chat.id, 'You send scam, you potentially lame')
        answer = "bad answer"
        log(message, answer)


server = Flask(__name__)


@server.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


@server.route("/%s/" % token, methods=['POST'])
def get_message():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url=url_heroku % token)

server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 80)), debug=True)
