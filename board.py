from sudoku_generator import SudokuGenerator
from cell import Cell
from constants import *
import pygame
#Hope this works

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        removed_cells = {'easy': 30, 'medium': 40, 'hard': 50}[difficulty]
        self.generator = SudokuGenerator(9, removed_cells)
        self.generator.fill_values()
        self.generator.remove_cells()
        self.cells = [[Cell(self.generator.board[i][j], i, j, screen) for j in range(9)] for i in range(9)]
        self.selected = None

    def draw(self):
        self.screen.fill(BG_COLOR)

        for row in self.cells:
            for cell in row:
                cell.draw()

        # Draw grid lines
        for i in range(1, BOARD_ROWS+1):
            thickness = LINE_WIDTH * 3 if i % 3 == 0 else LINE_WIDTH
            pygame.draw.line(self.screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), thickness)
            pygame.draw.line(self.screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), thickness)

        pygame.display.update()

    def select(self, row, col):
        if self.selected:
            self.selected.selected = False
        self.selected = self.cells[row][col]
        self.selected.selected = True

    def click(self, x, y):
        col = int(x // SQUARE_SIZE)
        row = int(y // SQUARE_SIZE)
        if 0 <= col < 9 and 0 <= row < 9:
            self.select(row, col)

    def clear(self):
        if self.selected and not self.selected.confirmed:
            self.selected.set_value(0)
            self.selected.draw()

    def sketch(self, value):
        if self.selected and not self.selected.confirmed:
            self.selected.set_value(value, confirmed=False)
            self.selected.draw()

    def place_number(self, value):
        if self.selected and not self.selected.confirmed:
            self.selected.set_value(value, confirmed=True)
            self.selected.draw()

    def reset_to_original(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    cell.set_cell_value(0)
                cell.draw()

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        for row in range(9):
            for col in range(9):
                self.cells[row][col].set_cell_value(self.generator.board[row][col])
                self.cells[row][col].draw()

    def check_board(self):
        return all(cell.confirmed and self.generator.is_valid(cell.row, cell.col, cell.value)
                   for row in self.cells for cell in row)


