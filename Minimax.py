import copy
import random

# Constants
EMPTY = 0
BLACK = 1
WHITE = 2
BLACK_KING = 3
WHITE_KING = 4

class Minimax():
    def __init__(self, max_depth=5, random_ties=0):
        self.max_depth = max_depth
        self.random_ties = random_ties


    def evaluate(self, board, maximizing_player):
        """
        Calculates the static heuristic value of the board.
        Score = (Material) + (Kings) + (Positional Advantage)
        """
        p1_score = 0 # Maximizing player's score
        p2_score = 0 # Minimizing opponent's score
        
        for r in range(8):
            for c in range(8):
                piece = board.board[r][c]
                if piece == EMPTY:
                    continue
                
                # The cell starts with a value of 0
                score = 0
                if piece in [BLACK, WHITE]:
                    # Having any piece gives 10 score
                    score = 10 # Standard material weight (w1)
                    # Positional bonus (w3): Moving closer to king row is better
                    if piece == BLACK:
                        if c == 6:
                            score += 1000
                        score += r 
                    else:
                        # Need to reverse for WHITE (equal scoring)
                        score += (7 - r)
                elif piece in [BLACK_KING, WHITE_KING]:
                    score = 25 # King material weight (w2)
                    # Positional bonus (w3): Center control is strong for Kings
                    if 2 <= r <= 5 and 2 <= c <= 5:
                        score += 3

                # Attribute score to the correct player
                if piece in [maximizing_player, maximizing_player + 2]: # +2 catches the King constant (top of file)
                    p1_score += score
                else:
                    p2_score += score

        # The core Minimax utility equation
        return p1_score - p2_score

    def get_best_move(self, board, max_player):
        """
        The entry point for the AI. Evaluates all top-level moves and 
        picks randomly among those that tie for the absolute best score.
        """
        legal_moves = board.get_legal_moves(max_player)
        if not legal_moves:
            return None

        # Move ordering to reduce time complexity.
        # Push moves which capture (jump) to the front of the legal_moves list, and slide moves go to the back.
        # We check this by looking at the row distance between the start and the first landing spot.
        legal_moves.sort(key=lambda m: abs(m[0][0] - m[1][0]) == 2, reverse=True)

        best_moves = []
        # we are alpha
        best_eval = float('-inf')
        alpha = float('-inf')

        for move in legal_moves:
            sim_board = copy.deepcopy(board)
            sim_board.make_move(move)
            
            # Pass to the minimizer at depth - 1
            evaluation, _ = self._alpha_beta(
                sim_board, 
                self.max_depth - 1, 
                float('-inf'), 
                alpha, 
                False, 
                max_player
            )

            # If we find a strictly better move, clear the list
            if evaluation > best_eval:
                best_eval = evaluation
                best_moves = [move] 
            # If we find a move exactly as good, add it to the ties
            elif evaluation == best_eval:
                best_moves.append(move)

            alpha = max(alpha, best_eval)

        # Randomly select one of the equally optimal moves if we chose to break ties
        if self.random_ties:
            return best_eval, random.choice(best_moves)
        else:
            return best_eval, best_moves[0] 

    def _alpha_beta(self, board, depth, alpha, beta, is_maximizing, max_player):
        """
        The core recursive function of Minimax using alpha and beta.
        Returns a tuple: (best_evaluation_score, best_move)
        """
        # Determine whose turn it is in this simulated timeline
        current_turn = max_player if is_maximizing else (WHITE if max_player == BLACK else BLACK)
        legal_moves = board.get_legal_moves(current_turn)

        # Move ordering to reduce time complexity. O(b^d) -> O(sqrt(b^d)
        # Push moves which capture (jump) to the front of the legal_moves list, and slide moves go to the back.
        # We check this by looking at the row distance between the start and the first landing spot.
        legal_moves.sort(key=lambda m: abs(m[0][0] - m[1][0]) == 2, reverse=True)

        # Reached max depth or game over are base cases here
        if depth == 0 or not legal_moves:
            # If no legal moves, the current player lost.
            if not legal_moves:
                return (float('-inf') if is_maximizing else float('inf')), None
            return self.evaluate(board, max_player), None

        best_move = None

        # MAX level
        if is_maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                # Simulate the move on a copy of the board
                # Deepcopy is slow, but when we optimize to C++ we will change it
                sim_board = copy.deepcopy(board)
                sim_board.make_move(move)
                
                # Recurse down the tree, passing control to the minimizer
                evaluation, _ = self._alpha_beta(sim_board, depth - 1, alpha, beta, False, max_player)
                
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
                
                # alpha-beta Pruning
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break # Prune the branch
            return max_eval, best_move

        # MIN level
        else:
            min_eval = float('inf')
            for move in legal_moves:
                sim_board = copy.deepcopy(board)
                sim_board.make_move(move)
                
                # Recurse down the tree, passing control back to the maximizer
                evaluation, _ = self._alpha_beta(sim_board, depth - 1, alpha, beta, True, max_player)
                
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
                    
                # alpha-beta Pruning
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break # Prune the branch
            return min_eval, best_move
