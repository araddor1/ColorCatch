from teleBot import *
import cv2
import numpy as np
import logging
import threading
import time
import msgs
import time
import operator




class ColorCatchGame:
    def __init__(self, api: TeleBot, players = 2):
        self.api = api
        self.cur_color = 0
        self.players = players
        self.rates = {}
        self.main_game()
        return

    def main_game(self):
        game_thread = threading.Thread(target=self.game_manager)
        connection_thread = threading.Thread(target=self.api.start_connection)
        connection_thread.start()
        game_thread.start()
        connection_thread.join()
        game_thread.join()

    def countdown(self, t):
        while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            if secs % 10 == 0:
                self.api.send_text_to_all(timeformat)
            time.sleep(1)
            t -= 1

    def connect_image(self,image_a,image_b):
        return cv2.vconcat([image_a, image_b])

    def stage_winner_choose(self, chosing_user , target_color , target_img):
        for user_id, img in self.api.imgs.items():
            #if user != chosing_user:
            cur_main_color = self.get_main_color(img)
            self.rates[user_id] = self.close_hue_rank(target_color, cur_main_color)
        max_user_id = max(self.rates.items(), key=operator.itemgetter(1))[0]
        self.api.send_text_to_all(msgs.WINNER_IS)
        self.api.send_text_to_all(self.api.get_name_by_id(max_user_id))
        winner_send = self.connect_image(target_img, self.api.imgs[max_user_id])
        self.api.send_photo_to_all(winner_send)


    def stage_color_picker(self, user):
        self.api.send_text(msgs.PICK_COLOR, user)
        self.api.send_text_to_all(" ITS " + user['first_name'] + "TURN", but_not_to=user)
        img = self.api.get_img_from_user(user)
        color = self.get_main_color(img)
        color_img = self.get_color_img(color)
        self.api.send_text_to_all(msgs.LOOKING_FOR)
        self.api.send_photo_to_all(color_img, user)
        return color , img

    def game_manager(self):
        while self.api.get_num_users() < self.players:
            continue
        self.api.get_input()
        for user in self.api.users:
            cur_color , cur_img = self.stage_color_picker(user)
            self.countdown(30)
            self.stage_winner_choose(user, cur_color , cur_img)
            self.api.clear_images()
        return

    @staticmethod
    def get_main_color(img):
        shape = np.shape(img)
        center_x = int(shape[1] / 2)
        center_y = int(shape[0] / 2)
        rng_x = int(shape[1] / 20)
        rng_y = int(shape[0] / 20)
        center_img = img[center_x - rng_x: center_x + rng_x, center_y - rng_y: center_y + rng_y]
        center_img_hsv = cv2.cvtColor(center_img, cv2.COLOR_RGB2HSV)
        avg_color_per_row = np.average(center_img_hsv, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        return avg_color

    @staticmethod
    def get_color_img(color):
        color_img_hsv = np.zeros((300, 300, 3), np.uint8)
        color_img_hsv[:] = color
        color_img = cv2.cvtColor(color_img_hsv, cv2.COLOR_HSV2RGB)
        return color_img

    @staticmethod
    def close_hue_rank(color_0, color_1):
        h0 = color_0[0]
        h1 = color_1[0]
        dh = min(abs(h1 - h0), 360 - abs(h1 - h0)) / 180.0
        return dh

    def color_choose_state(self, img):
        self.cur_color = self.get_main_color(img)







