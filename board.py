from costants import *
import pygame
from sudoku_generator import *

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.board = sudoku_generator(9, 0)

    def draw(self):
        self.screen.fill(BG_COLOR)
        for i in range(1, BOARD_ROWS):
            thickness = LINE_WIDTH
            if i % 3 == 0:
                thickness = LINE_WIDTH * 3  # Make every third line thicker
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (0, i * SQUARE_SIZE),
                (WIDTH, i * SQUARE_SIZE),
                thickness
            )
        for i in range(1, BOARD_COLS):
            thickness = LINE_WIDTH
            if i % 3 == 0:
                thickness = LINE_WIDTH * 3  # Make every third line thicker
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (i * SQUARE_SIZE, 0),
                (i * SQUARE_SIZE, HEIGHT),
                thickness
            )
        self.update_board()

    def select(self, row, col):
        if event.type == pygame.MOUSEBUTTONDOWN:
            (x, y) = pygame.mouse.get_pos()
            return x, y

        pass

    def click(self, x, y):
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        if self.selected == (row, col):
            # If already selected, deselect
            self.selected = None
        else:
            # Otherwise, select the cell
            self.selected = (row, col)
        self.update_board()
        pass

    def clear(self):
        pass

    def sketch(self, value):
        pass

    def place_number(self, value):
        pass

    def reset_to_original(self):
        self.board = initialize_board()  # Assuming you have a function to initialize the Sudoku board
        self.update_board()

    def is_full(self):
        pass

    def update_board(self):
        for row in range(9):
            for col in range(9):
                number = self.board[row][col]
                if number != 0:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(number), True, BLACK)
                    text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE / 2,
                                                       row * SQUARE_SIZE + SQUARE_SIZE / 2))
                    self.screen.blit(text, text_rect)
        pygame.display.update()

    def check_board(self):
        pass


