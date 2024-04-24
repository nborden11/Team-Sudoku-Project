import pygame
import sys
from board import Board
from constants import *
#hope this works


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT+100))
    pygame.display.set_caption('Sudoku Game')

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    LIGHT_GRAY = (200, 200, 200)

    def draw_buttons(screen, reset_button, restart_button, exit_button):
        # Button properties
        button_color = LIGHT_GRAY
        text_color = BLACK
        button_text_y_offset = 10

        if reset_button:
            pygame.draw.rect(screen, button_color, reset_button)
            screen.blit(font.render('Reset', True, text_color),
                        (reset_button.x + 45, reset_button.y + button_text_y_offset))
        if restart_button:
            pygame.draw.rect(screen, button_color, restart_button)
            screen.blit(font.render('Restart', True, text_color),
                        (restart_button.x + 35, restart_button.y + button_text_y_offset))
        if exit_button:
            pygame.draw.rect(screen, button_color, exit_button)
            screen.blit(font.render('Exit', True, text_color),
                        (exit_button.x + 50, exit_button.y + button_text_y_offset))

    def draw_start_screen(screen, welcome_text, mode_text):
        screen.fill(BG_COLOR)
        easy_button = pygame.draw.rect(screen, LIGHT_GRAY, (200, 250, 200, 50))
        medium_button = pygame.draw.rect(screen, LIGHT_GRAY, (200, 320, 200, 50))
        hard_button = pygame.draw.rect(screen, LIGHT_GRAY, (200, 390, 200, 50))

        screen.blit(welcome_text, (WIDTH // 2 - welcome_text.get_width() // 2, 50))
        screen.blit(mode_text, (WIDTH // 2 - mode_text.get_width() // 2, 150))

        screen.blit(font.render('Easy', True, BLACK), (250, 260))
        screen.blit(font.render('Medium', True, BLACK), (250, 330))
        screen.blit(font.render('Hard', True, BLACK), (250, 400))

        return easy_button, medium_button, hard_button  # Return button rects for click detection

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

            #reset_button, restart_button, and exit_button logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if reset_button.collidepoint(x, y) and game_started:
                    if board:
                        # Iterate through all cells and reset sketches directly
                        for row in board.cells:
                            for cell in row:
                                if not cell.confirmed:  # Check if the cell is not confirmed
                                    cell.set_value(0, confirmed=False)
                                    cell.draw()
                elif restart_button.collidepoint(x, y) and game_started:
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
                if board and board.selected:
                    if event.unicode.isdigit():
                        num = int(event.unicode)
                        if 1 <= num <= 9:
                            board.sketch(num)  # Sketch the number in red
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if board.selected and board.selected.sketched_value != 0:
                            board.place_number(board.selected.sketched_value)  # Confirm the number
                    elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        if board.selected and not board.selected.confirmed:
                            board.clear()  # Clear only if the number is not confirmed

        # Check if the board is full
        if board and board.is_full():
            if board.check_board():
                screen.fill(BG_COLOR)
                text = font.render('Game Won!', True, BLACK)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
                draw_buttons(screen, None, None, exit_button)  # Only show exit button
                pygame.display.update()
            else:
                screen.fill(BG_COLOR)
                text = font.render('Game Over :(', True, BLACK)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
                draw_buttons(screen, None, restart_button, None)
                pygame.display.update()

        # Drawing the screen only when necessary
        if not game_started:
            easy_button, medium_button, hard_button = draw_start_screen(screen, welcome_text, mode_text)
        elif game_started and board:
            board.draw()
            draw_buttons(screen, reset_button, restart_button, exit_button)

        pygame.display.update()


if __name__ == "__main__":
    main()