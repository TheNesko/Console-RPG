from imports import *
from game import Game
from display import Display


game = Game()
if __name__ == "__main__":
    Display.window("Rpg game", 55, 30)
    game.run()