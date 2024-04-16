class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.column = col
        self.screen = screen

    def set_cell_value(self, value):
        pass

    def set_sketched_value(self, value):
        pass

    def draw(self):
        pass