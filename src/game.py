import pygame
import sys

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
    
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect Four")

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

    pygame.display.update()

def draw_top_bar(game):
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, SQUARESIZE))  # Clear the top bar
    posx = pygame.mouse.get_pos()[0]  # Get current mouse position
    if game.turn:
        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)  # Player 2's piece
    else:
        pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)  # Player 1's piece

    pygame.display.update()    


def main():
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
                    print(f"Player {2 if game.turn else 1} wins!")
                    game.game_over = True
        draw_top_bar(game)


if __name__ == "__main__":
    main()


#ideas to continute -
    # add a restart button
    # instead of exiting when a player wins and printing it on the terminal, make a pop up window that says who won with ok button to exit.   