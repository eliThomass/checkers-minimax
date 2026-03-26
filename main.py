# Constants
EMPTY = 0
BLACK = 1
WHITE = 2
BLACK_KING = 3
WHITE_KING = 4

class MinimaxAB():
    def __init__(self, debug):
        self.initialize_board()
        self.board[3][2] = WHITE
        self.board[5][0] = EMPTY
        self.board[6][5] = EMPTY
        self.debug = debug

    def initialize_board(self):
        """
        Creates an 8x8 2D list representing the starting state of English Checkers.
        Black pieces are placed on rows 0-2, and White pieces on rows 5-7.
        """
        self.board = [[EMPTY for _ in range(8)] for _ in range(8)]
        for r in range(8):
            for c in range(8):
                if (r + c) % 2 != 0:
                    if r < 3: self.board[r][c] = BLACK
                    elif r > 4: self.board[r][c] = WHITE


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

        print(f"movement for {player}: \njumps = {jumps} \nslides = {slides}\n") if self.debug else 0
        return jumps if jumps else slides

    def is_on_board(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def get_piece_directions(self, r, c, board):
        """
        Helper function for get_slides and get_jumps
        Returns valid directions of movement based on piece type
        """
        piece = board[r][c]
        if piece == WHITE: return [(-1, -1), (-1, 1)]
        if piece == BLACK: return [(1, -1), (1, 1)]
        if piece in [WHITE_KING, BLACK_KING]: return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return []

    def is_player_piece(self, piece, player):
        """
        A function which determines if a given piece matches playing player. 
        """
        if player == WHITE:
            return piece in [WHITE, WHITE_KING]
        return piece in [BLACK, BLACK_KING]

    def find_jumps(self, r, c, board_state=None):
        """
        Recursively finds all capturing sequences including multi-jumps.
        Returns a list of move sequences: [[(r,c), (r2,c2)], [(r,c), (r2,c2), (r3,c3)]]
        We need board-state parameter to pass temporary board states to find successive jumps
        """
        if board_state is None:
            board_state = self.board
            
        piece = board_state[r][c]
        player = WHITE if piece in [WHITE, WHITE_KING] else BLACK
        opponent = [BLACK, BLACK_KING] if player == WHITE else [WHITE, WHITE_KING]
        
        all_sequences = []
        found_any_jump = False

        for dr, dc in self.get_piece_directions(r, c, board_state):
            # Midpoint (enemy to jump) and landing spot
            mr, mc = r + dr, c + dc
            lr, lc = r + 2*dr, c + 2*dc

            if self.is_on_board(lr, lc):
                if board_state[mr][mc] in opponent and board_state[lr][lc] == EMPTY:
                    found_any_jump = True
                    
                    # Create a temporary board to simulate the jump for multi-jump detection
                    temp_board = [row[:] for row in board_state]
                    temp_board[lr][lc] = piece
                    temp_board[mr][mc] = EMPTY
                    temp_board[r][c] = EMPTY
                    
                    # If a piece becomes a King, its turn ends (rule)
                    became_king = (player == WHITE and lr == 0) or (player == BLACK and lr == 7)
                    
                    # Recursively look for more jumps from the landing spot
                    if piece in [WHITE, BLACK] and became_king:
                        sub_jumps = [] # Turn ends on promotion
                    else:
                        sub_jumps = self.find_jumps(lr, lc, temp_board)

                    if sub_jumps:
                        for seq in sub_jumps:
                            all_sequences.append([(r, c)] + seq)
                    else:
                        all_sequences.append([(r, c), (lr, lc)])

        return all_sequences

    def find_slides(self, r, c):
        """
        A function to calculate all legal slides (non-capturing diagonal movements)
        for a piece (r, c).
        Only called if no jumps are found for given piece on the board.
        """
        slides = []
        for dr, dc in self.get_piece_directions(r, c, self.board):
            nr, nc = r + dr, c + dc
            if self.is_on_board(nr, nc) and self.board[nr][nc] == EMPTY:
                # Format: ((start_r, start_c), (end_r, end_c))
                slides.append(((r, c), (nr, nc)))
        return slides


if __name__ == "__main__":
    test = MinimaxAB(debug=True)

    cur_player = "BLACK"

    test.display()
    test.get_legal_moves(cur_player)

