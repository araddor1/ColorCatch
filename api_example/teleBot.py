from ConnectAPI import *
from telegram.ext import *
import numpy as np
import cv2
import urllib.request


class TeleBot(ConnectAPI):
    def __init__(self, start_msg):
        self.token = self.init_token()
        self.imgs = {}
        self.start_msg = start_msg
        self.users = []

    @staticmethod
    def init_token():
        token=""
        with open('../bot_token.txt', 'r') as file:
            token = file.read().replace('\n', '')
        return token

    def start(self, update, context):
        self.bot = context.bot
        cur_user = update.message.chat
        if not cur_user in self.users:
            self.users.append(cur_user)
        print(cur_user)
        context.bot.send_message(chat_id=cur_user.id, text=self.start_msg)
        self.send_text_to_all(cur_user.first_name +" joined the game!", cur_user.id)

    def image_handler(self, update, context):
        id = context.bot.getFile(update.message.photo[0].file_id)
        resp = urllib.request.urlopen(id['file_path'])
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        self.imgs[update.effective_chat.id] = image

    def start_connection(self):
        print("starting connection to Bot")
        updater = Updater(token=self.token, use_context=True)
        dp = updater.dispatcher
        start_handler = MessageHandler(Filters.command, self.start)
        message_handler = MessageHandler(Filters.photo, self.image_handler)
        dp.add_handler(start_handler)
        dp.add_handler(message_handler)
        updater.start_polling()

    def send_photo_to_all(self, img , but_not_to = None):
        cv2.imwrite("../temp/temp_send.jpeg", img)
        for user in self.users:
            if user['id'] != but_not_to:
                self.bot.send_photo(chat_id=user['id'], photo=open('../temp/temp_send.jpeg', 'rb'))

    def send_text_to_all(self, text , but_not_to=None):
        for user in self.users:
            if user.id != but_not_to:
                self.bot.send_message(chat_id=user['id'], text=text)

    def get_name_by_id(self, id):
        for user in self.users:
            if id == user['id']:
                return user['first_name'] + " " + user['last_name']

    def send_text(self, text, user=None):
        self.bot.send_message(chat_id=user['id'], text=text)

    def get_img_from_user(self, user):
        while not user["id"] in self.imgs:
            continue
        return self.imgs[user['id']]

    def clear_images(self):
        self.imgs.clear()