class ConnectFour:
    def __init__(self):
        # Initialize the 6x7 grid (6 rows, 7 columns) as empty
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.current_player = 'R'  # Start with player 'R' (Red)


    def print_board(self):
        """Prints the board."""
        print(" 0 1 2 3 4 5 6")
        print("---------------")
        for row in self.board:
            print('|'.join(row))
            print("---------------")


    def drop_piece(self, column):
        """Drops a piece in the selected column."""
        for row in reversed(self.board):
            if row[column] == ' ':
                row[column] = self.current_player
                return True
        return False  # The column is full
    

    def switch_player(self):
        """Switches the current player."""
        self.current_player = 'Y' if self.current_player == 'R' else 'R'


    def check_win(self):
        """Checks if the current player has won."""
        # Check horizontal, vertical, and diagonal lines
        for row in range(6):
            for col in range(7):
                if self.check_line(row, col):
                    return True
        return False


    def check_line(self, row, col):
        """Checks if there are four in a row starting at (row, col)."""
        # Directions: (row, col) -> (vertical, horizontal, diagonal1, diagonal2)
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 0
            for i in range(4):
                r, c = row + i*dr, col + i*dc
                if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            if count == 4:
                return True
        return False
    
if __name__ == "__main__":
    game = ConnectFour()
    game.print_board()

    while True:
        column = int(input(f"Player {game.current_player}, enter a column (0-6): "))
        
        if 0 <= column < 7 and game.drop_piece(column):
            game.print_board()
            if game.check_win():
                print(f"Player {game.current_player} wins!")
                break
            game.switch_player()
        else:
            print("Invalid move. Try again.")

    
