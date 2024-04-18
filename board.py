from cell import *
from sudoku_generator import *

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cells = [[Cell(0, i, j, screen) for j in range(9)] for i in range(9)]
        self.selected_cell = None


    def draw(self):
        for i in range(10):
            line_width = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, pygame.Color('black'), (0, i * 50), (self.width, i * 50), line_width)
            pygame.draw.line(self.screen, pygame.Color('black'), (i * 50, 0), (i * 50, self.height), line_width)

        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        if self.selected_cell:
            self.selected_cell.selected = False
        self.selected_cell = self.cells[row][col]
        self.selected_cell.selected = True

    def click(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            col = x // 50
            row = y // 50
            return (row, col)
        return None

    def clear(self):
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_cell_value(0)
            self.selected_cell.set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_cell_value(value)

    def reset_to_original(self):
        for row in self.cells:
            for cell in row:
                cell.set_cell_value(0)

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].value = self.board[i][j]

    def find_empty(self):
        for i in range(len(self.board)):
            for j in range(i):
                if j == "-":
                    return (i, j)

    def check_board(self):
        for i in range(9):
            row_vals = [cell.value for cell in self.cells[i] if cell.value != 0]
            col_vals = [self.cells[r][i].value for r in range(9) if self.cells[r][i].value != 0]
            if len(set(row_vals)) != len(row_vals) or len(set(col_vals)) != len(col_vals):
                return False

        for box_start_row in range(0, 9, 3):
            for box_start_col in range(0, 9, 3):
                box_vals = [self.cells[row][col].value for row in range(box_start_row, box_start_row + 3)
                            for col in range(box_start_col, box_start_col + 3) if self.cells[row][col].value != 0]
                if len(set(box_vals)) != len(box_vals):
                    return False

        return True


