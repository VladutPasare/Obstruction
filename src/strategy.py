import random
import sys

from board import Board, Cell


class Strategy:
    pass


class RandomStrategy(Strategy):
    def move(self, board: Board):
        if not board.free_cells():
            raise ValueError("There are no free cells on the board!")
        row, column = random.choice(board.free_cells())
        board.set_cell_state(row, column, Cell.O)


class MinimaxStrategy(Strategy):
    MAXIMIZER = sys.maxsize
    MINIMIZER = -sys.maxsize
    NONE = 0

    def __init__(self):
        self._temporarily_occupied_cells = []

    def move(self, board: Board):
        best_move = None
        best_score = self.MINIMIZER

        for cell in board.free_cells():
            self._temporarily_occupied_cells.append(cell)
            score = self.minimax(board, True, 0)
            self._temporarily_occupied_cells.remove(cell)

            if score >= best_score:
                best_score = score
                best_move = cell

        board.set_cell_state(best_move[0], best_move[1], Cell.O)

    def is_victory(self, board):
        for cell in board.free_cells():
            blocked = False

            for temporarily_cell in self._temporarily_occupied_cells:
                if -1 <= cell[0] - temporarily_cell[0] <= 1 and -1 <= cell[1] - temporarily_cell[1] <= 1:
                    blocked = True
            if not blocked:
                return False
        return True

    def potential_move(self, board: Board, cell):
        if board.get_cell_state(cell[0], cell[1]) != Cell.Free:
            return False

        for occupied_cell in self._temporarily_occupied_cells:
            if -1 <= cell[0] - occupied_cell[0] <= 1 and -1 <= cell[1] - occupied_cell[1] <= 1:
                return False
        return True

    def minimax(self, board, maximizer, depth):
        if depth > 2:
            return self.NONE

        if self.is_victory(board):
            return self.MAXIMIZER

        in_depth_scores = []

        for cell in board.free_cells():
            if self.potential_move(board, cell):
                self._temporarily_occupied_cells.append(cell)
                in_depth_scores.append(-self.minimax(board, not maximizer, depth + 1))
                self._temporarily_occupied_cells.remove(cell)

        min_score = self.MAXIMIZER
        max_score = self.MINIMIZER

        for score in in_depth_scores:
            if score < min_score:
                min_score = score
            if score > max_score:
                max_score = score

        if maximizer:
            return max_score
        else:
            return min_score
