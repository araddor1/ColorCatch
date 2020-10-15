import numpy as np
import cv2

"""
    "virtual" Class that connects between the front-end of the game to the game class.
    all api's need to follow this structure. can see an example for telegram API in teleBot.py
    """
class ConnectAPI:

    """
        :param start_msg: the starting msg of the API
        this method wil build the connectios class.
        The connection will be established in a diffrent method.
        the class need to include:
        1. self.imgs = {}: Python Dict of imgs. when key is the id of player and data is an img.
        2. self.users = [] : python List of users. user is a dict with :
                                                        1.id - diffrent number per user
                                                        2.first_name    3. last_name
    """
    def __init__(self, start_msg):
        return

        """
        Inner Method:
            method when new user comes in. adds the user to self.users
        """
    def start(self):
        return


    """
    Inner Method:
    when a user send a photo . add photo of user x to self.imgs[x]
    """
    def image_handler(self, update, context):
        return


    """
    API Method:
    starts a connection between the API to the front-end platform.
    IMPORTANT - this is the method that the game will run in a thread.
    so this method need to end with a method that *waits* for user interaction.
    """
    def start_connection(self):
        return


    """
        API Method:
        send/show a photo to all users.
        img : the numpy based photo
        (optional) but_not_to : user_id (number) that will not get the img
    """
    def send_photo_to_all(self, img, but_not_to=None):
        return


    """
      API Method:
        send/show a text to all users.
        text : the string that need to be sent
       (optional) but_not_to : user_id (number) that will not get the img
    """
    def send_text_to_all(self, text, but_not_to=None):
        return


    """
   API Method:
   id : user id
        returns the first and last name of user as one string
    """
    def get_name_by_id(self, id):
        return


    """
    API Method:
        send/show a text to a user.
        text : the string that need to be sent
        user : user_id (number) to send the text to
     """
    def send_text(self, text, user):
        return


    """
    API Method:
        returns the last imgs from user as a numpy array.
        user : user_id (number) to send the text to
    """
    def get_img_from_user(self, user):
        return


    """
    API Method:
        clears all data in self.imgs
    """
    def clear_images(self):
        return