import cv2
import numpy as np


class ColorCatchGame:

    def __init__(self):
        return

    def get_picture(self):

        return

    @staticmethod
    def get_main_color(img):
        shape = np.shape(img)
        center_x = int(shape[1] / 2)
        center_y = int(shape[0] / 2)
        center_img = img[center_x -5 : center_x + 5 , center_y -5: center_y +5]
        center_img_hsv = cv2.cvtColor(center_img, cv2.COLOR_RGB2HSV)
        avg_color_per_row = np.average(center_img_hsv, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        return avg_color

    @staticmethod
    def get_color_img(color):
        color_img = np.zeros((300, 300, 3), np.uint8)
        color_img[:] = color
        return color_img

    @staticmethod
    def close_hue_rank(color_0, color_1):
        h0 = color_0[0]
        h1 = color_1[0]
        dh = min(abs(h1 - h0), 360 - abs(h1 - h0)) / 180.0
        return dh


