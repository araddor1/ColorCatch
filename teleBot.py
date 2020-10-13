from telegram.ext import *
from PIL import Image
import urllib2

bot_token = "1259414137:AAE616L7yagtU2psPjk0jaKy2GNCSkf7wJA"
updater = Updater(token= bot_token, use_context=True)


class teleBot:
    def __init__(self,game):
        self.game = game

    def start(self,update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="ברוכים הבאים לתופסת הצבעים!")

    def image_handler(self,update ,context ):
        id = context.bot.getFile(update.message.photo[1].file_id)
        print(id)
        print(id['file_path'])

    def bot_main(self):
        dp = updater.dispatcher
        start_handler = CommandHandler('start', self.start)
        dp.add_handler(start_handler)
        dp.add_handler(MessageHandler(Filters.photo, self.image_handler))
        updater.start_polling()
        updater.idle()
