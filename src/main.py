import pygame.font

from board import Board
from gui import GUI

if __name__ == '__main__':
    board = Board(8, 8, 160, 100)
    gui = GUI(board)
    gui.single_player_mode()
    # gui.multiplayer_mode()
