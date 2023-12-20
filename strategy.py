import random

from board import Board, Cell


class Strategy:
    def __init__(self, board: Board, symbol: Cell):
        self._board = board
        self._symbol = symbol


class RandomStrategy(Strategy):
    def __init__(self, board: Board, symbol: Cell):
        super().__init__(board, symbol)

    def move(self):
        if not self._board.free_cells():
            raise ValueError("There are no free cells on the board!")
        row, column = random.choice(self._board.free_cells())
        self._board.set_cell_state(row, column, self._symbol)