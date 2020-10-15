from ConnectAPI import *
import numpy as np
import threading
import cv2
import msgs
import time

font = cv2.FONT_HERSHEY_SIMPLEX

class ColorCatchGame:
    def __init__(self, api: ConnectAPI, min_players=2):
        self.api = api
        self.cur_color = 0
        self.min_players = min_players
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
            timeformat = '{:02d}'.format(t)
            if t % 10 == 0:
                self.api.send_text_to_all(timeformat + msgs.COUNTDOWN)
            time.sleep(1)
            t -= 1

    def create_winner_image(self,image_a,image_b):
        image_a = cv2.resize(image_a, (100,100), interpolation=cv2.INTER_AREA)
        image_b = cv2.resize(image_b, (100, 100), interpolation=cv2.INTER_AREA)
        connected_image = cv2.vconcat([image_a, image_b])
        return connected_image

    def create_result_image(self):
        length = len(self.rates)
        if length > 7:
            length = 7
        img_size = 200
        res_img = np.zeros((img_size, img_size * length,3))
        cur_num = 0

        for user_id , rate in self.rates:
                cur_img = self.api.imgs[user_id]
                cur_img_res = cv2.resize(cur_img, (img_size,img_size), interpolation=cv2.INTER_AREA)
                cur_img_res = cv2.putText(cur_img_res, str(cur_num + 1), (75, 75), font, 1, (255, 0, 0),3, cv2.LINE_AA)
                if cur_num <= length:
                    res_img[0:img_size, cur_num * img_size:(cur_num + 1) * img_size] = cur_img_res
                cur_num += 1
        return res_img


    def stage_winner_choose(self, chosing_user , target_color , target_img):
        self.rates={}
        for user_id, img in self.api.imgs.items():
            if user_id != chosing_user['id']:
                cur_main_color = self.get_main_color(img)
                self.rates[user_id] = self.close_hue_rank(target_color, cur_main_color)
        self.rates = sorted(self.rates.items(), key=lambda x: x[1])
        result_image = self.create_result_image()
        self.api.send_photo_to_all(result_image)
        max_user_id = self.rates[0][0]
        self.api.send_text_to_all(msgs.WINNER_IS)
        self.api.send_text_to_all(self.api.get_name_by_id(max_user_id))


    def stage_color_picker(self, user):
        self.api.send_text(msgs.PICK_COLOR, user)
        self.api.send_text_to_all(" ITS " + user['first_name'] + " TURN", but_not_to=user)
        img = self.api.get_img_from_user(user)
        color = self.get_main_color(img)
        color_img = self.get_color_img(color)
        self.api.send_text_to_all(msgs.LOOKING_FOR)
        self.api.send_photo_to_all(color_img)
        return color, img

    def game_manager(self):
        while len(self.api.users) < self.min_players:
            continue
        for user in self.api.users:
            cur_color, cur_img = self.stage_color_picker(user)
            self.countdown(30)
            self.stage_winner_choose(user, cur_color , cur_img)
            self.api.clear_images()
        self.api.send_text_to_all(msgs.END_OF_GAME)
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







