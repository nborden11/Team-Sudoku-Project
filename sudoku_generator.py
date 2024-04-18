import math,random
import pygame, sys
from costants import *
from board import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("suduko")


class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for _ in range(row_length)] for _ in range(self.row_length)]
        self.box_length = int(math.sqrt(row_length))
        return None

    def get_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            for col in row:
                print(col if col!= 0 else '.', end = '')
            print()
        print()

    def valid_in_row(self, row, num):
        for i in self.board[row]:
            if i == num:
                return False
        return True

    def valid_in_col(self, col, num):
        for i in range(self.row_length):
            if self.board[i][col] == num:
                return False
        return True

    def valid_in_box(self, row_start, col_start, num):
        for i in range(row_start, row_start+3):
            for j in range(col_start, col_start+3):
                if self.board[i][j] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        if self.valid_in_box(row, col, num) and self.valid_in_row(row, num) and self.valid_in_col(col, num):
            return True
        return False
        pass

    def fill_box(self, row_start, col_start):
        box = list(range(1, self.row_length + 1))
        random.shuffle(box)
        for i in range(row_start, row_start+3):
            for j in range(col_start, col_start+3):
                self.board[row_start + i][col_start + j] = box.pop(0)

    def fill_diagonal(self):
        for i in range(0, self.row_length, 3):
            self.fill_box(i, i)

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, 0)

    def remove_cells(self):
        v1 = 1
        v2 = 1
        for i in range(self.board.difficulty):
            while True:
                v1 = random.randint(0, 8)
                v2 = random.randint(0, 8)
                if self.board[v1][v2] != 0:
                    break
            self.board[v1][v2] = 0
        pass

    def generate_sudoku(size, removed):
        generator = SudokuGenerator(size, removed)
        generator.fill_values()
        generator.remove_cells()
        return generator.get_board()

def main():
    sudoku = SudokuGenerator(9, 0)
    sudoku.fill_values()  # Generate the Sudoku board
    sudoku.remove_cells()  # Remove cells to create the puzzle
    board = sudoku.get_board()  # Get the Sudoku board

    for row in board:
        print(row)



if __name__ == "__main__":
    main()




