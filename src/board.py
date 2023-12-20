from enum import Enum


class Cell(Enum):
    Wall = -1
    Free = 0
    X = 1
    O = 2


class Board:
    def __init__(self, rows: int, columns: int, top: int, left: int):
        if rows < 0:
            raise ValueError("The number of rows must be positive!")
        self.__rows = rows
        if columns < 0:
            raise ValueError("The number of columns must be positive!")
        self.__columns = columns
        self.__top = top
        self.__left = left
        self.__grid = []

        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(Cell.Free)
            self.__grid.append(row)

    @property
    def rows(self):
        return self.__rows

    @property
    def columns(self):
        return self.__columns

    @property
    def left(self):
        return self.__left

    @property
    def top(self):
        return self.__top

    def free_cells(self):
        free_cells = []
        for i in range(self.__rows):
            for j in range(self.__columns):
                if self.__grid[i][j] == Cell.Free:
                    free_cells.append((i, j))
        return free_cells

    def __valid_row(self, row: int) -> bool:
        return 0 <= row < self.__rows

    def __valid_column(self, column: int) -> bool:
        return 0 <= column < self.__columns

    def __valid_cell(self, row: int, column: int) -> bool:
        return self.__valid_row(row) and self.__valid_column(column)

    def get_cell_state(self, row: int, column: int) -> Cell:
        if not self.__valid_cell(row, column):
            raise ValueError((row, column), "is not a valid cell!")
        return self.__grid[row][column]

    def set_cell_state(self, row: int, column: int, state: Cell):
        if not self.__valid_cell(row, column):
            raise ValueError((row, column), "is not a valid cell!")
        if self.get_cell_state(row, column) != Cell.Free:
            raise ValueError("Cell", (row, column), "is not free!")
        if state != Cell.X and state != Cell.O:
            raise ValueError("State must be either X or O!")
        self.__grid[row][column] = state
        self.__fill_surrounding_cells(row, column)

    def __fill_surrounding_cells(self, row: int, column: int):
        row_moves = [-1, -1, -1, 0, 0, 1, 1, 1]
        column_moves = [-1, 0, 1, -1, 1, -1, 0, 1]

        for i in range(8):
            neighbor_row = row + row_moves[i]
            neighbor_column = column + column_moves[i]
            if self.__valid_cell(neighbor_row, neighbor_column):
                self.__grid[neighbor_row][neighbor_column] = Cell.Wall

    def reset(self):
        for i in range(self.__rows):
            for j in range(self.__columns):
                self.__grid[i][j] = Cell.Free
