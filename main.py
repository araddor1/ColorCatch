from game import *
from teleBot import *

def main():
    my_game = ColorCatchGame()
    my_bot = teleBot(my_game)
    my_bot.bot_main()

if __name__ == '__main__':
    main()