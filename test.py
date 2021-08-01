import main

import telebot
import time
token = "788811717:AAFCXXumZJkwkJFy_PRkRUZQe8jww_2RlMo"
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


@bot.message_handler(commands=['start'])
def hendle_start(message):
    app = main.ArtConverter(str(444), 3)
    app.run()
    img = open(f'out/' + '444' + '.jpg', 'rb')
    bot.send_message(59290719, 'ewfef')
    bot.send_photo(59290719, photo=img)
    answer = "menu"
    log(message, answer)


while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)
        # или import traceback; traceback.print_exc() для печати полной инфы
        time.sleep(15)

