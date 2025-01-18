import math
import random
import numpy as np
import pygame
import sys
import os

# game attributes
WIDTH, HEIGHT = 700, 700
SQUARESIZE = 100
ROW_COUNT = 6
COLUMN_COUNT = 7
RADIUS = int(SQUARESIZE / 2 - 7)
BLUE = (44, 108, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (240, 240, 240)
LIGHTBLUE = (173, 216, 230)
OFFWHITE = (230, 230, 230)
PLAYER = 1
AI = 2

# Button dimensions
BUTTON_X = 254.4
BUTTON_Y = 541
BUTTON_WIDTH = 191.2
BUTTON_HEIGHT = 67.3

def drop_piece(board ,row, col, piece):
    board[row][col] = piece
    
    
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_available_row(board, col):
    for r in range(ROW_COUNT):  
        if board[r][col] == 0: 
            return r        

def check_win(board):
    # Check for horizontal, vertical, and diagonal wins
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] != 0:
                if check_directions(board, r, c):
                    return True
    return False

def check_directions(board, row, col):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        if check_line(board, row, col, dr, dc):
            return True
    return False

def check_line(board, row, col, dr, dc):
    player = board[row][col]
    for i in range(1, 4):
        r, c = row + i * dr, col + i * dc
        if r < 0 or r >= ROW_COUNT or c < 0 or c >= COLUMN_COUNT or board[r][c] != player:
            return False
    return True

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
    message = font.render(f"{winner} Wins!", True, RED if winner == "Player" else YELLOW)
    screen.blit(message, (WIDTH // 4, HEIGHT // 4))
    
    # Instructions to restart or quit
    instructions = font.render("Press R to Restart", True, WHITE)
    screen.blit(instructions, (WIDTH // 8, HEIGHT // 2))
    instructions2 = font.render("Press Q to Quit", True, WHITE)
    screen.blit(instructions2, (WIDTH // 8, HEIGHT // 2 + 150))
    pygame.display.update()


def initialize_board():
    # Draw the empty board
    turn = random.randint(PLAYER, AI)
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT + 1):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, OFFWHITE , (c * SQUARESIZE + SQUARESIZE // 2, r * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2), RADIUS)
    return board , turn

def draw_board(board):
    # Draw the discs on the board
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT + 1):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, OFFWHITE , (c * SQUARESIZE + SQUARESIZE // 2, r * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER:
                pygame.draw.circle(screen, RED, (c * SQUARESIZE + SQUARESIZE // 2, (5 - r) * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2), RADIUS)
            elif board[r][c] == AI:
                pygame.draw.circle(screen, YELLOW, (c * SQUARESIZE + SQUARESIZE // 2, (5 - r) * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2), RADIUS)
            else:
                pygame.draw.circle(screen, OFFWHITE, (c * SQUARESIZE + SQUARESIZE // 2, (5 - r) * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2), RADIUS)    
    pygame.display.update()

def draw_top_bar():
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, SQUARESIZE))  # Clear the top bar
    posx = max(RADIUS, min(WIDTH - RADIUS, pygame.mouse.get_pos()[0]))
    if turn == PLAYER:
        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)  # Player's piece
    else:
        pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)  # AI's piece
    pygame.display.update()  

def window_eval(connect, piece):
    score = 0 
    opp_piece = PLAYER
    if piece == PLAYER:
        opp_piece = AI
    if connect.count(piece) == 4:
        score += 100 #winning move
    elif connect.count(piece) == 3 and connect.count(0) == 1:
        score += 10 #3 in a row
    elif connect.count(piece) == 2 and connect.count(0) == 2:
        score += 5 #2 in a row
    if connect.count(opp_piece) == 3 and connect.count(0) == 1:
        score -= 50 #block opponent
    return score

def score_position(board, piece):
    score = 0

    #center preference
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    #horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            connect = row_array[c:c + 4]
            score += window_eval(connect, piece)

    #vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            connect = col_array[r:r + 4]
            score += window_eval(connect, piece)

    #positive diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            connect = [board[r + i][c + i] for i in range(4)]
            score += window_eval(connect, piece)  

    #negative diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            connect = [board[r + 3 - i][c + i] for i in range(4)]
            score += window_eval(connect, piece)

    return score

def terminal_node(board):
    return check_win(board) or len(get_valid_locations(board)) == 0

def minimax(board, depth, maxmizingPlayer):
    valid_locations = get_valid_locations(board)
    if depth == 0 or terminal_node(board):
        if terminal_node(board):
            if check_win(board) and turn == AI:
                return (None, 100000000000000)
            elif check_win(board) and turn == PLAYER:
                return (None, -100000000000000)
            else:
                return (None, 0) #game is over
        else:
            return (None, score_position(board, AI))  
    if maxmizingPlayer:
        column = random.choice(valid_locations)
        value = math.inf * -1
        for col in valid_locations:
            row = get_next_available_row(board, col)
            copy_board = board.copy()
            drop_piece(copy_board, row, col, AI)
            new_score = minimax(copy_board, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else:
        column = random.choice(valid_locations)
        value = math.inf
        for col in valid_locations:
            row = get_next_available_row(board, col)
            copy_board = board.copy()
            drop_piece(copy_board, row, col, PLAYER)
            new_score = minimax(copy_board, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value

def best_move_trivial(board, piece):
    best_score = -1000
    valid_locations = get_valid_locations(board)
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_available_row(board, col)
        copy_board = board.copy()
        drop_piece(copy_board, row, col, piece)
        score = score_position(copy_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col        

             

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

game_over = False
pygame.init()
pygame.display.set_caption("Connect Four")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
board , turn = initialize_board()
draw_home_screen()
draw_board(board)


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not check_win(board) and turn == PLAYER:
            posx = event.pos[0]
            col = int(posx // SQUARESIZE)
            if is_valid_location(board, col):
                row = get_next_available_row(board, col)
                drop_piece(board, row, col, PLAYER)  # Drop the piece in the correct column
                draw_board(board)  # Redraw the game board
                if check_win(board): # Check for win condition
                    pygame.time.wait(500)
                    print("Player wins!")
                    winner_screen("Player")
                turn += 1
                turn = (turn % 2) + 2     

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Press 'R' to restart
                board , turn = initialize_board()
            elif event.key == pygame.K_q:  # Press 'Q' to quit
                pygame.quit()
                sys.exit()
        if turn == AI and not check_win(board):
            # col = random.randint(0, COLUMN_COUNT - 1)
            #col = best_move_trivial(board, AI)
            col, minimax_score = minimax(board, 3, True)
            if is_valid_location(board, col):
                pygame.time.wait(500)  # Wait for 0.5 seconds before dropping the piece
                row = get_next_available_row(board, col)
                drop_piece(board, row ,col, AI)  # Drop the piece in the correct column
                draw_board(board)  # Redraw the game board
                
                if check_win(board):  # Check for win condition
                    pygame.time.wait(500)
                    print("AI wins!")
                    winner_screen("AI")    
                turn += 1
                turn = turn % 2  

        if not check_win(board):
            draw_top_bar()


#ideas to continute -
    # add a motion to the pieces when they are dropped

