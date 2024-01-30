from board import Board
from gui import GUI
from strategy import *

if __name__ == '__main__':
    board = Board(6, 6, 160, 100)
    gui = GUI(board)

    gui.single_player_mode(RandomStrategy())
    # gui.single_player_mode(MinimaxStrategy())
    # gui.multiplayer_mode()
