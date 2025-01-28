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
YELLOW = (255, 220, 0)
WHITE = (240, 240, 240)
LIGHTBLUE = (173, 216, 230)
OFFWHITE = (230, 230, 230)
PLAYER = 1
AI = 2
END = False

# Button dimensions
BUTTON_X = 254.4
BUTTON_Y = 541
BUTTON_WIDTH = 191.2
BUTTON_HEIGHT = 67.3

def drop_piece(board, row, col, piece):
    x_pos = col * SQUARESIZE + SQUARESIZE // 2
    for r in range(1,ROW_COUNT-1): # Iterate from the top to the target row
        if board[ROW_COUNT-r][col] == 0:  # If the current row is empty
            y_pos = r * SQUARESIZE + SQUARESIZE // 2
            # Draw the falling piece
            pygame.draw.circle(screen, RED if piece == PLAYER else YELLOW, (x_pos, y_pos), RADIUS)
            pygame.display.update()
            pygame.time.wait(100)  # Adjust timing for smoother animation
            pygame.draw.circle(screen, OFFWHITE, (x_pos, y_pos), RADIUS)

    # Update the board state after animation
    board[row][col] = piece

def copy_drop_piece(board, row, col, piece):
    #Drops a piece into the board without a falling animation.
    board[row][col] = piece    

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_available_row(board, col):
    for r in range(ROW_COUNT):  
        if board[r][col] == 0: 
            return r  

def find_winning_move(board, piece):
    # Loop through all valid locations to find a winning move
    valid_locations = get_valid_locations(board)
    
    for col in valid_locations:
        row = get_next_available_row(board, col)
        copy_board = board.copy()
        copy_drop_piece(copy_board, row, col, piece)
        
        if check_win(copy_board, piece):
            return col  # Return the column where AI can win

    return None  # No winning move found

def check_win(board, piece):
    # Check for horizontal, vertical, and diagonal wins
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] != 0:
                if check_directions(board, r, c, piece):
                    return True
    return False

def check_directions(board, row, col, piece):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        if check_line(board, row, col, dr, dc, piece):
            return True
    return False

def check_line(board, row, col, dr, dc, piece):
    for i in range(4):
        r, c = row + i * dr, col + i * dc
        if r < 0 or r >= ROW_COUNT or c < 0 or c >= COLUMN_COUNT or board[r][c] != piece:
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
    for alpha in range(0, 256, 5): # Slowly increase the transparency
        fade_surface.set_alpha(alpha)  
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

def connect_eval(connect, piece):
    opp_piece = PLAYER if piece == AI else AI
    piece_count = connect.count(piece)
    empty_count = connect.count(0)
    opp_count = connect.count(opp_piece)
    
    if piece_count == 4:
        return 100
    elif piece_count == 3 and empty_count == 1:
        return 5
    elif piece_count == 2 and empty_count == 2:
        return 2
    elif opp_count == 3 and empty_count == 1:
        return -4
    return 0


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
            score += connect_eval(connect, piece)

    #vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            connect = col_array[r:r + 4]
            score += connect_eval(connect, piece)

    #positive diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            connect = [board[r + i][c + i] for i in range(4)]
            score += connect_eval(connect, piece)  

    #negative diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            connect = [board[r + 3 - i][c + i] for i in range(4)]
            score += connect_eval(connect, piece)

    return score

def terminal_node(board):
    return check_win(board, PLAYER) or check_win(board, AI) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    if depth == 0 or terminal_node(board):
        if terminal_node(board):
            if check_win(board, AI):
                return (None, 10000)
            elif check_win(board, PLAYER):
                return (None, -10000)
            else:
                return (None, 0) #game is over
        else:
            return (None, score_position(board, AI))  
    if maximizingPlayer:
        column = random.choice(valid_locations)
        value = float('-inf')
        for col in valid_locations:
            row = get_next_available_row(board, col)
            copy_board = board.copy()
            copy_drop_piece(copy_board, row, col, AI)
            new_score = minimax(copy_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        column = random.choice(valid_locations)
        value = float('inf')
        for col in valid_locations:
            row = get_next_available_row(board, col)
            copy_board = board.copy()
            copy_drop_piece(copy_board, row, col, PLAYER)
            new_score = minimax(copy_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break    
        return column, value

def best_move_trivial(board, piece):
    best_score = -1000
    valid_locations = get_valid_locations(board)
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_available_row(board, col)
        copy_board = board.copy()
        copy_drop_piece(copy_board, row, col, piece)
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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Press 'R' to restart
                END = False
                board , turn = initialize_board()
            elif event.key == pygame.K_q:  # Press 'Q' to quit
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_h: # Simulate AI vs AI
                while not END:
                    if turn == PLAYER and not END:
                        winning_move = find_winning_move(board, PLAYER)
                        if winning_move is not None:
                            col = winning_move
                        else:   
                            col, _ = minimax(board, 5, -math.inf, math.inf, True)
                        if is_valid_location(board, col):
                            #pygame.time.wait(500)  # An Optional delay for the player to see the move
                            row = get_next_available_row(board, col)
                            drop_piece(board, row ,col, PLAYER)  # Drop the piece in the correct column
                            draw_board(board)  # Redraw the game board
                            
                            if check_win(board, PLAYER):  # Check for win condition
                                pygame.time.wait(1000)
                                print("Player wins!")
                                winner_screen("Player")
                                END = True  
                            else:    
                                turn = AI
                    elif turn == AI and not END:
                        #col = random.randint(0, COLUMN_COUNT - 1) # Random move
                        #col = best_move_trivial(board, AI) # Trivial AI
                        winning_move = find_winning_move(board, AI)
                        if winning_move is not None:
                            col = winning_move
                        else:   
                            col, _ = minimax(board, 5, -math.inf, math.inf, True)
                        if is_valid_location(board, col):
                            #pygame.time.wait(500)  # An Optional delay for the player to see the move
                            row = get_next_available_row(board, col)
                            drop_piece(board, row ,col, AI)  # Drop the piece in the correct column
                            draw_board(board)  # Redraw the game board
                            
                            if check_win(board, AI):  # Check for win condition
                                pygame.time.wait(1000)
                                print("AI wins!")
                                winner_screen("AI")
                                END = True
                            else:
                                turn = PLAYER          
           

        if event.type == pygame.MOUSEBUTTONDOWN and not END: # Player's turn
            posx = event.pos[0]
            col = int(posx // SQUARESIZE)
            if is_valid_location(board, col):
                row = get_next_available_row(board, col)
                drop_piece(board, row, col, PLAYER)  # Drop the piece in the correct column
                draw_board(board)  # Redraw the game board
                if check_win(board, PLAYER): # Check for win condition
                    pygame.time.wait(500)
                    print("Player wins!")
                    winner_screen("Player")
                    END = True
                else:
                    turn = AI

        elif turn == AI and not END: # AI's turn
            #col = random.randint(0, COLUMN_COUNT - 1) # Random move
            #col = best_move_trivial(board, AI) # Trivial AI
            winning_move = find_winning_move(board, AI) # Find a winning move if it exists
            if winning_move is not None:
                col = winning_move
            else:   
                col, _ = minimax(board, 5, -math.inf, math.inf, True)
            if is_valid_location(board, col):
                #pygame.time.wait(500)  # An Optional delay for the player to see the move
                row = get_next_available_row(board, col)
                drop_piece(board, row ,col, AI)  # Drop the piece in the correct column
                draw_board(board)  # Redraw the game board
                
                if check_win(board, AI):  # Check for win condition
                    pygame.time.wait(1000)
                    print("AI wins!")
                    winner_screen("AI")
                    END = True  
                else:
                    turn = PLAYER     

        if not END:
            draw_top_bar()




