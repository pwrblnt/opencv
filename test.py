import main

import telebot
token = "788811717:AAEoeDB2eFrSrTtxSGXusZh4cQZ7IoPBPTQ"
bot = telebot.TeleBot(token)


def test():
    app = main.ArtConverter(str(33), 10)
    app.run()
    img = open(f'out/' + '59290719' + '.jpg', 'rb')
    bot.send_photo(59290719, photo=img)


test()

