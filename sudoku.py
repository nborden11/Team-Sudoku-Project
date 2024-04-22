import pygame
import sys
from board import Board
from constants import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Sudoku Game')

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    LIGHT_GRAY = (200, 200, 200)

    # Font
    font = pygame.font.Font(None, 36)

    # Game states
    game_over = False
    game_started = False
    difficulty = 'easy'  # Default difficulty

    board = None

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if not game_started:
                    # Check button positions for difficulty selection
                    if easy_button.collidepoint(x, y):
                        difficulty = 'easy'
                        game_started = True
                    elif medium_button.collidepoint(x, y):
                        difficulty = 'medium'
                        game_started = True
                    elif hard_button.collidepoint(x, y):
                        difficulty = 'hard'
                        game_started = True

                    if game_started:
                        # Create the board with selected difficulty
                        removed_cells = 30 if difficulty == 'easy' else 40 if difficulty == 'medium' else 50
                        board = Board(WIDTH, HEIGHT, screen, difficulty)

                else:
                    # Handle game interactions
                    if board:
                        clicked = board.click(x, y)
                        if clicked:
                            row, col = clicked
                            board.select(row, col)

        # Drawing the screen
        screen.fill(BG_COLOR)
        if not game_started:
            # Draw start screen with buttons
            easy_button = pygame.draw.rect(screen, LIGHT_GRAY, (50, 150, 200, 50))
            medium_button = pygame.draw.rect(screen, LIGHT_GRAY, (50, 250, 200, 50))
            hard_button = pygame.draw.rect(screen, LIGHT_GRAY, (50, 350, 200, 50))
            screen.blit(font.render('Easy', True, BLACK), (100, 160))
            screen.blit(font.render('Medium', True, BLACK), (85, 260))
            screen.blit(font.render('Hard', True, BLACK), (100, 360))
        else:
            # Game board
            if board:
                board.draw()

        pygame.display.flip()

if __name__ == "__main__":
    main()