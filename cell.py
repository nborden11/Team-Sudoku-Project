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


    def set_value(self, value):
        self.value = value

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
            text_rect = text.get_rect(center=(x + self.cell_size / 2, y + self.cell_size / 2))
            self.screen.blit(text, text_rect)
        elif self.sketched_value != 0:
            text = self.font.render(str(self.sketched_value), True, pygame.Color('gray'))
            self.screen.blit(text, (x + 5, y + 5))

        if self.selected:
            pygame.draw.rect(self.screen, pygame.Color('red'), (x, y, self.cell_size, self.cell_size), 4)
