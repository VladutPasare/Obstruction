import pygame
import time
from pygame.locals import MOUSEBUTTONDOWN

from board import Board, Cell
from client import Client
from strategy import RandomStrategy


class GUI:
    __WAIT_TIME = 1.5
    __MY_TURN = 1
    __ENEMY_TURN = 0
    __WINDOW_CAPTION = "OBSTRUCTION"
    __BACKGROUND_COLOR = (246, 246, 246)

    def __init__(self, board: Board):
        self.__board = board
        pygame.init()
        pygame.display.set_caption(self.__WINDOW_CAPTION)
        self.__window = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
        self.__window.fill(self.__BACKGROUND_COLOR)
        self.__score = 0
        self.__FONT = pygame.font.SysFont("sfcamera", 26)
        self.__TEXT_COLOR = (0, 0, 0)

    def __display_board(self):
        for row in range(self.__board.rows):
            for column in range(self.__board.columns):
                state = self.__board.get_cell_state(row, column)
                cell_image = pygame.image.load("assets/free_cell.png")
                if state == Cell.Wall:
                    cell_image = pygame.image.load("assets/wall_cell.png")
                if state == Cell.X:
                    cell_image = pygame.image.load("assets/x_cell.png")
                if state == Cell.O:
                    cell_image = pygame.image.load("assets/o_cell.png")
                self.__window.blit(cell_image, (self.__board.left + column * 50, self.__board.top + row * 50))

    def __click_on_board(self, x: int, y: int) -> bool:
        return self.__board.top <= x <= self.__board.top + self.__board.rows * 50 and self.__board.left <= y <= self.__board.left + self.__board.columns * 50

    def __get_row(self, x: int) -> int:
        return (x - self.__board.top) // 50

    def __get_column(self, y: int) -> int:
        return (y - self.__board.left) // 50

    def __display_score(self):
        pygame.draw.rect(self.__window, self.__BACKGROUND_COLOR, (500, 30, 100, 30))
        text = self.__FONT.render(f'Score: {self.__score}', True, self.__TEXT_COLOR, self.__BACKGROUND_COLOR)
        self.__window.blit(text, (500, 30))

    def single_player_mode(self):
        random_strategy = RandomStrategy(self.__board, Cell.O)
        computer = 0
        player = 1
        turn = player

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if not self.__board.free_cells():
                    time.sleep(0.4)

                    if turn == computer:
                        you_won_message = pygame.image.load("assets/you_won.png")
                        self.__window.blit(you_won_message, (140, 40))
                        self.__score += 1
                    else:
                        you_lost_message = pygame.image.load("assets/you_lost.png")
                        self.__window.blit(you_lost_message, (140, 40))
                        if self.__score > 0:
                            self.__score -= 1

                    pygame.display.update()
                    time.sleep(1)
                    self.__board.reset()
                    self.__window.fill(self.__BACKGROUND_COLOR)

                elif turn == computer:
                    time.sleep(0.6)
                    random_strategy.move()
                    turn = player

                elif event.type == MOUSEBUTTONDOWN:
                    if turn == player:
                        y, x = pygame.mouse.get_pos()

                        if self.__click_on_board(x, y):
                            row = self.__get_row(x)
                            column = self.__get_column(y)

                            if self.__board.get_cell_state(row, column) == Cell.Free:
                                self.__board.set_cell_state(row, column, Cell.X)
                                turn = computer
                self.__display_score()
                self.__display_board()
                pygame.display.update()

    def multiplayer_mode(self):
        client = Client(5270)
        turn = client.turn
        game_over = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                self.__display_score()
                self.__display_board()
                pygame.display.update()

                if game_over:
                    self.__board.reset()
                    self.__window.fill(self.__BACKGROUND_COLOR)
                    time.sleep(self.__WAIT_TIME)
                    game_over = 0
                    continue

                if turn == self.__ENEMY_TURN:
                    enemy_row, enemy_column, game_over = client.receive()
                    self.__board.set_cell_state(enemy_row, enemy_column, Cell.O)

                    if game_over == 1:
                        you_lost_message = pygame.image.load("assets/you_lost.png")
                        self.__window.blit(you_lost_message, (140, 40))
                    turn = self.__MY_TURN
                    continue

                if event.type == MOUSEBUTTONDOWN:
                    y, x = pygame.mouse.get_pos()

                    if self.__click_on_board(x, y):
                        row = self.__get_row(x)
                        column = self.__get_column(y)

                        if self.__board.get_cell_state(row, column) == Cell.Free:
                            self.__board.set_cell_state(row, column, Cell.X)
                            turn = self.__ENEMY_TURN
                            if self.__board.free_cells():
                                client.send(row, column, game_over)
                            else:
                                game_over = 1
                                client.send(row, column, game_over)
                                you_won_message = pygame.image.load("assets/you_won.png")
                                self.__window.blit(you_won_message, (140, 40))
                                self.__score += 1
