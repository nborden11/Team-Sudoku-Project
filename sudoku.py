import pygame
import sys
from board import Board
from constants import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT+100))
    pygame.display.set_caption('Sudoku Game')

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    LIGHT_GRAY = (200, 200, 200)

    # Font
    font = pygame.font.Font(None, 36)
    welcome_font = pygame.font.Font(None, 48)  # Larger font for titles

    # Game states
    game_over = False
    game_started = False
    difficulty = 'easy'  # Default difficulty
    board = None

    # Buttons
    button_height = 40
    button_width = 150
    space_between = 10
    button_spacing = 10  # Space between buttons
    button_start_x = 50  # Horizontal start position for the first button
    bottom_panel_y = HEIGHT + 100 - button_height - 20  # Position buttons at the bottom

    # Define button rectangles
    reset_button = pygame.Rect(button_start_x, bottom_panel_y, button_width, button_height)
    restart_button = pygame.Rect(button_start_x + button_width + button_spacing, bottom_panel_y, button_width,
                                 button_height)
    exit_button = pygame.Rect(button_start_x + 2 * (button_width + button_spacing), bottom_panel_y, button_width,
                              button_height)

    welcome_text = welcome_font.render('Welcome to Sudoku!', True, BLACK)
    mode_text = font.render('Select Game Mode', True, BLACK)

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if game_started:
                    if board:
                        clicked = board.click(x, y)
                        if clicked:
                            row, col = clicked
                            board.select(row, col)

                # Check button presses
                if reset_button.collidepoint(x, y):
                    if board:
                        board.reset_to_original()
                elif restart_button.collidepoint(x, y):
                    board = Board(WIDTH, HEIGHT, screen, difficulty)
                elif exit_button.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()

                # Start screen logic
                if not game_started:
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
                        board = Board(WIDTH, HEIGHT, screen, difficulty)

                else:
                    # Handle game interactions
                    if board:
                        clicked = board.click(x, y)
                        if clicked:
                            row, col = clicked
                            board.select(row, col)


            # Handle key input for numbers
            if event.type == pygame.KEYDOWN and game_started:
                if board and board.selected:  # Check if a cell is selected
                    if event.unicode.isdigit():
                        num = int(event.unicode)
                        if 1 <= num <= 9:
                            board.place_number(num)

        # Drawing the screen
        screen.fill(BG_COLOR)
        if not game_started:
            # Draw start screen with buttons
            easy_button = pygame.draw.rect(screen, LIGHT_GRAY, (200, 250, 200, 50))
            medium_button = pygame.draw.rect(screen, LIGHT_GRAY, (200, 320, 200, 50))
            hard_button = pygame.draw.rect(screen, LIGHT_GRAY, (200, 390, 200, 50))
            screen.blit(welcome_text, (WIDTH / 2 - welcome_text.get_width() / 2, 50))
            screen.blit(mode_text, (WIDTH / 2 - mode_text.get_width() / 2, 150))
            screen.blit(font.render('Easy', True, BLACK), (250, 260))
            screen.blit(font.render('Medium', True, BLACK), (250, 330))
            screen.blit(font.render('Hard', True, BLACK), (250, 400))
        else:
            # Game board
            if board:
                board.draw()
        # Redraw buttons manually here
        reset_button = pygame.draw.rect(screen, LIGHT_GRAY, (50, bottom_panel_y, 150, button_height))
        restart_button = pygame.draw.rect(screen, LIGHT_GRAY, (225, bottom_panel_y, 150, button_height))
        exit_button = pygame.draw.rect(screen, LIGHT_GRAY, (400, bottom_panel_y, 150, button_height))
        screen.blit(font.render('Reset', True, BLACK), (reset_button.x + 45, reset_button.y + 10))
        screen.blit(font.render('Restart', True, BLACK), (restart_button.x + 35, restart_button.y + 10))
        screen.blit(font.render('Exit', True, BLACK), (exit_button.x + 50, exit_button.y + 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()