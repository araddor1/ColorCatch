from ConnectAPI import *
from telegram.ext import *
from telegram import ReplyKeyboardMarkup , ReplyKeyboardRemove
import numpy as np
import cv2
import urllib.request
from collections import deque


class TeleBot(ConnectAPI):
    def __init__(self, start_msg):
        self.token = self.init_token()
        self.img_q = deque()
        self.start_msg = start_msg
        self.users = []
        self.bot = None
        self.update = None


    @staticmethod
    def init_token():
        token=""
        with open('bot_token.txt', 'r') as file:
            token = file.read().replace('\n', '')
        return token

    def start(self, update, context):
        if self.bot is None:
            self.init_class_attr(update, context)
        print(self.update.effective_chat)
        full_name = self.update.effective_chat['first_name'] + " " + self.update.effective_chat['last_name']
        self.users.append(full_name)
        self.bot.send_message(chat_id=self.update.effective_chat.id ,text=self.start_msg)

    def get_input(self):
        return

    def init_class_attr(self,update, context):
        self.bot = context.bot
        self.update = update

    def image_handler(self, update, context):
        if self.bot is None:
            self.init_class_attr(update, context)
        id = context.bot.getFile(update.message.photo[0].file_id)
        print(id)
        resp = urllib.request.urlopen(id['file_path'])
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        self.img_q.append(image)

    def start_connection(self):
        print("starting connection to Bot")
        updater = Updater(token=self.token, use_context=True)
        dp = updater.dispatcher
        start_handler = CommandHandler('start', self.start)
        message_handler = MessageHandler(Filters.photo, self.image_handler)
        dp.add_handler(start_handler)
        dp.add_handler(message_handler)
        updater.start_polling()

    def send_photo(self, img):
        cv2.imwrite("temp/temp_send.jpeg", img)
        self.bot.send_photo(chat_id=self.update.effective_chat.id, photo=open('temp/temp_send.jpeg', 'rb'))

    def send_text(self, text):
        self.bot.send_message(chat_id=self.update.effective_chat.id, text=text)

    def get_last_img(self):
        return self.img_q.popleft()

    def img_q_size(self):
        return len(self.img_q)

    def get_num_users(self):
        return len(self.users)




# ## custom KEYS
#         custom_keyboard = [['Start']]
#         reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keybord=True)
#         self.update.message.reply_text(
#             "welcome , do you want to start?" ,reply_markup=reply_markup)
