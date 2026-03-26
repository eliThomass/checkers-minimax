# Constants
EMPTY = 0
BLACK = 1
WHITE = 2
BLACK_KING = 3
WHITE_KING = 4

class MinimaxAB():
    def __init__(self):
        """
        Creates an 8x8 2D list representing the starting state of English Checkers.
        Black pieces are placed on rows 0-2, and White pieces on rows 5-7.
        """
        self.board = [[EMPTY for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 != 0:
                    if row < 3:
                        self.board[row][col] = BLACK
                    elif row > 4:
                        self.board[row][col] = WHITE

    def display(self):
        """
        A utility function to visualize the board state in the terminal.
        """
        # Mapping numbers to visual characters
        symbols = {
            EMPTY: ".",
            BLACK: "b",
            WHITE: "w",
            BLACK_KING: "B",
            WHITE_KING: "W"
        }
        
        print("\n    0 1 2 3 4 5 6 7") # Column headers
        print("  -----------------")
        for r_idx, row in enumerate(self.board):
            # Convert row values to symbols
            row_viz = [symbols[val] for val in row]
            print(f"{r_idx} | {' '.join(row_viz)} |")
        print("  -----------------")

    def get_legal_moves(self, player):
        """
        A function which returns all legal moves for a given player (BLACK/WHITE).
        """
        jumps = []
        slides = []
        
        # Determine directions based on piece type/player
        # White moves row - 1, Black moves row + 1
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if self.is_player_piece(piece, player):
                    piece_jumps = self.find_jumps(r, c)
                    if piece_jumps:
                        jumps.extend(piece_jumps)

                    # Only look for slides if no jumps found yet
                    elif not jumps:
                        slides.extend(self.find_slides(r, c))
        
        return jumps if jumps else slides

    def is_player_piece(self, piece, player):
        """
        A function which determines if a given piece matches playing player. 
        """
        if player == WHITE:
            return piece in [WHITE, WHITE_KING]
        return piece in [BLACK, BLACK_KING]

    def find_jumps(self, r, c):
        """
        A function to calculate all legal jumps for a piece on the board.
        Returns a list of (r, c) tuples which are valid to jump to.
        """
        return []

    def find_slides(self, r, c):
        """
        A function to calculate all legal slides (moving forward/backward).
        Only called if no jumps are found for given piece on the board.
        """
        return []


if __name__ == "__main__":
    test = MinimaxAB()

    test.display()

