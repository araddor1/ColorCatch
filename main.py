from game import *
from teleBot import *

def main():
    my_bot = TeleBot("Welcome to ColorCatch Game")
    my_game = ColorCatchGame(my_bot)

if __name__ == '__main__':
    main()