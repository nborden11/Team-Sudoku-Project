import pygame
from constants import *
class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.column = col
        self.screen = screen
        self.selected = False
        self.font = pygame.font.Font(None, 40)
        self.cell_size = 66.6
        self.sketched_value = 0
        self.confirmed = False



    def set_value(self, value, confirmed = False):
        if confirmed:
            self.value = value
            self.sketched_value = 0
            self.confirmed = True
        else:
            self.sketched_value = value
            self.confirmed = False

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        x = self.column * self.cell_size
        y = self.row * self.cell_size
        pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, self.cell_size, self.cell_size))

        if self.value != 0:
            text = self.font.render(str(self.value), True, pygame.Color('black'))
            self.screen.blit(text, (x + self.cell_size / 2, y + self.cell_size / 2))
        elif self.sketched_value != 0:
            text = self.font.render(str(self.sketched_value), True, pygame.Color('red'))
            self.screen.blit(text, (x + 10, y + 10))

        if self.selected:
            pygame.draw.rect(self.screen, pygame.Color('red'), (x, y, self.cell_size, self.cell_size), 4)
