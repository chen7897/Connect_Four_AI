import time
import pygame
import sys
import os

class ConnectFour:
    def __init__(self):
        self.ROWS = 6  
        self.COLUMNS = 7  
        self.board = [[0 for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]  # Initialize a 6x7 board
        self.game_over = False 
        self.turn = True  # Player 1 starts (1 for player 1, 2 for player 2)

    def create_board(self):
        return [[0 for _ in range(7)] for _ in range(6)]

    def drop_piece(self, col):
        if self.game_over:
            return
        row = self.get_next_available_row(col)
        if row is not None:
            self.board[row][col] = 1 if self.turn else 2
            self.turn = not(self.turn)

    def get_next_available_row(self, col):
        for r in range(6):  # Start from the bottom row
            if self.board[r][col] == 0:  # Find the next available empty spot
                return r
        return None         
    

    def check_win(self):
        # Check for horizontal, vertical, and diagonal wins
        for r in range(self.ROWS):
            for c in range(self.COLUMNS):
                if self.board[r][c] != 0:
                    if self.check_directions(r, c):
                        return True
        return False

    def check_directions(self, row, col):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            if self.check_line(row, col, dr, dc):
                return True
        return False

    def check_line(self, row, col, dr, dc):
        player = self.board[row][col]
        for i in range(1, 4):
            r, c = row + i * dr, col + i * dc
            if r < 0 or r >= self.ROWS or c < 0 or c >= self.COLUMNS or self.board[r][c] != player:
                return False
        return True


# Pygame setup and game loop
WIDTH, HEIGHT = 700, 700
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 7)
BLUE = (44, 108, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (240, 240, 240)
LIGHTBLUE = (173, 216, 230)
OFFWHITE = (230, 230, 230)

# Button dimensions
BUTTON_X = 254.4
BUTTON_Y = 541
BUTTON_WIDTH = 191.2
BUTTON_HEIGHT = 67.3
    
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect Four")


def draw_home_screen():
    # Load the background image
    docs_folder = os.path.join(os.path.dirname(__file__), "../docs")
    background_image_path = os.path.join(docs_folder, "home_screen.jpg")
    background = pygame.image.load(background_image_path)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Draw the background
    screen.blit(background, (0, 0))
    pygame.display.update()

    # Wait for user to click the button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH) and \
                   (BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT):
                    fade_to_black(background)  # Fade out the home screen
                    return  # Exit the function to start the game
                

def fade_to_black(image):
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    for alpha in range(0, 256, 5):  # Gradually increase alpha from 0 to 255
        fade_surface.set_alpha(alpha)  # Set the transparency level
        screen.blit(image, (0, 0))  # Redraw the current image
        screen.blit(fade_surface, (0, 0))  # Draw the fade overlay
        pygame.display.update()
        pygame.time.delay(7)  # Control the speed of the fade effect

def winner_screen(winner):
    screen.fill(BLACK)
    font = pygame.font.SysFont("monospace", 50)
    message = font.render(f"Player {winner} Wins!", True, RED if winner == 1 else YELLOW)
    screen.blit(message, (WIDTH // 5, HEIGHT // 4))
    
    # Instructions to restart or quit
    instructions = font.render("Press R to Restart", True, WHITE)
    screen.blit(instructions, (WIDTH // 8, HEIGHT // 2))
    instructions2 = font.render("Press Q to Quit", True, WHITE)
    screen.blit(instructions2, (WIDTH // 8, HEIGHT // 2 + 150))
    pygame.display.update()


def initialize_board(game):
    # Draw the empty board
    for c in range(game.COLUMNS):
        for r in range(game.ROWS + 1):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, OFFWHITE , (c * SQUARESIZE + SQUARESIZE // 2, r * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2), RADIUS)
    

def draw_board(game):
    # Draw the discs on the board
    for c in range(game.COLUMNS):
        for r in range(game.ROWS):
            if game.board[r][c] == 1:
                pygame.draw.circle(screen, RED, (c * SQUARESIZE + SQUARESIZE // 2, (5 - r) * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2), RADIUS)
            elif game.board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (c * SQUARESIZE + SQUARESIZE // 2, (5 - r) * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2), RADIUS)
            else:
                pygame.draw.circle(screen, OFFWHITE, (c * SQUARESIZE + SQUARESIZE // 2, (5 - r) * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2), RADIUS)    

    pygame.display.update()

def draw_top_bar(game):
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, SQUARESIZE))  # Clear the top bar
    posx = max(RADIUS, min(WIDTH - RADIUS, pygame.mouse.get_pos()[0]))
    if game.turn:
        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)  # Player 2's piece
    else:
        pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)  # Player 1's piece

    pygame.display.update()    


def main():
    draw_home_screen()
    game = ConnectFour()
    draw_board(game)
    initialize_board(game)

    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)
                game.drop_piece(col)  # Drop the piece in the correct column
                draw_board(game)  # Redraw the game board

                # Check for win condition
                if game.check_win():
                    time.sleep(0.15)
                    print(f"Player {2 if game.turn else 1} wins!")
                    winner_screen(2 if game.turn else 1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press 'R' to restart
                    game.__init__()
                    initialize_board(game)
                elif event.key == pygame.K_q:  # Press 'Q' to quit
                    pygame.quit()
                    sys.exit()
        if not game.check_win():
            draw_top_bar(game)
        
if __name__ == "__main__":
    main()


#ideas to continute -
    # add a motion to the pieces when they are dropped

