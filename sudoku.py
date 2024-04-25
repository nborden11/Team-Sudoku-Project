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
   LIGHT_GRAY = (200, 200, 200)

   # Font
   font = pygame.font.Font(None, 36)
   welcome_font = pygame.font.Font(None, 48)

   # Buttons
   button_height = 40
   button_width = 150
   button_spacing = 10
   button_start_x = 50
   bottom_panel_y = HEIGHT + 100 - button_height - 20

   # Define button rectangles
   reset_button = pygame.Rect(button_start_x, bottom_panel_y, button_width, button_height)
   restart_button = pygame.Rect(button_start_x + button_width + button_spacing, bottom_panel_y, button_width,
                                button_height)
   exit_button = pygame.Rect(button_start_x + 2 * (button_width + button_spacing), bottom_panel_y, button_width,
                             button_height)

   welcome_text = welcome_font.render('Welcome to Sudoku!', True, BLACK)
   mode_text = font.render('Select Game Mode', True, BLACK)

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

       # Game loop
       while True:
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   pygame.quit()
                   sys.exit()
               if event.type == pygame.MOUSEBUTTONDOWN:
                   x, y = event.pos
                   if easy_button.collidepoint(x, y):
                       return 'easy'
                   if medium_button.collidepoint(x, y):
                       return 'medium'
                   if hard_button.collidepoint(x, y):
                       return 'hard'

           pygame.display.update()

   def draw_end_screen(screen,win_lose_text):
       screen.fill(BG_COLOR)
       restart_button = pygame.Rect(button_start_x + button_width + button_spacing, bottom_panel_y, button_width,
                                    button_height)
       exit_button = pygame.Rect(button_start_x + 2 * (button_width + button_spacing), bottom_panel_y, button_width,
                                 button_height)
       text = font.render(win_lose_text, True, BLACK)
       screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
       draw_buttons(screen, None, restart_button, exit_button)  # Only show exit button
       # Game loop
       while True:
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   pygame.quit()
                   sys.exit()
               if event.type == pygame.MOUSEBUTTONDOWN:
                   x, y = event.pos
                   if restart_button.collidepoint(x, y):
                       return
                   elif exit_button.collidepoint(x, y):
                       pygame.quit()
                       sys.exit()
           pygame.display.update()

   # game start screen
   difficulty = draw_start_screen(screen, welcome_text, mode_text)
   board = Board(WIDTH, HEIGHT, screen, difficulty)

   # Game loop
   while True:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()

           #reset_button, restart_button, and exit_button logic
           if event.type == pygame.MOUSEBUTTONDOWN:
               x, y = event.pos
               if reset_button.collidepoint(x, y):
                   if True:
                       # Iterate through all cells and reset sketches directly
                       for row in board.cells:
                           for cell in row:
                               if not cell.confirmed or cell.value == 0:  # Check if the cell is not confirmed
                                   cell.set_value(0, confirmed=False)
                                   cell.draw()
                   board.reset_to_original()
               elif restart_button.collidepoint(x, y):
                   difficulty = draw_start_screen(screen, welcome_text, mode_text)
                   board = Board(WIDTH, HEIGHT, screen, difficulty)
               elif exit_button.collidepoint(x, y):
                   pygame.quit()
                   sys.exit()

               # Handle game interactions
               if True:
                   clicked = board.click(x, y)
                   if clicked:
                       row, col = clicked
                       board.select(row, col)

           # Handle input for numbers and key presses
           if event.type == pygame.KEYDOWN:
               if board.selected:
                   if event.unicode.isdigit():
                       num = int(event.unicode)
                       if 1 <= num <= 9:
                           board.sketch(num)
                   elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                       if board.selected and board.selected.sketched_value != 0:
                           board.place_number(board.selected.sketched_value)
                   elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                       if board.selected and not board.selected.confirmed:
                           board.clear()
                   # Handle arrow keys
                   elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                       current_row, current_col = board.selected.row, board.selected.column
                       if event.key == pygame.K_UP:
                           new_row = max(0, current_row - 1)
                           board.select(new_row, current_col)
                       elif event.key == pygame.K_DOWN:
                           new_row = min(8, current_row + 1)
                           board.select(new_row, current_col)
                       elif event.key == pygame.K_LEFT:
                           new_col = max(0, current_col - 1)
                           board.select(current_row, new_col)
                       elif event.key == pygame.K_RIGHT:
                           new_col = min(8, current_col + 1)
                           board.select(current_row, new_col)

       # Check if the board is full
       if board.is_full():
           if board.check_board():
               print('win')
               print(board.check_board())
               draw_end_screen(screen,'Game Win!')
               difficulty = draw_start_screen(screen, welcome_text, mode_text)
               board = Board(WIDTH, HEIGHT, screen, difficulty)

           else:
               print('lose')
               print(board.check_board())
               draw_end_screen(screen,'Game Lose!')
               difficulty = draw_start_screen(screen, welcome_text, mode_text)
               board = Board(WIDTH, HEIGHT, screen, difficulty)

       # Drawing the screen only when necessary
       board.draw()
       draw_buttons(screen, reset_button, restart_button, exit_button)
       pygame.display.flip()


if __name__ == "__main__":
   main()