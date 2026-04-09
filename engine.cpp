#include <vector>
#include <cmath>
#include <algorithm>
#include <cstdlib>

// Constants
const int EMPTY = 0;
const int BLACK = 1;
const int WHITE = 2;
const int BLACK_KING = 3;
const int WHITE_KING = 4;

// A struct to represent a move sequence (passed back to Python)
struct Move {
    int r[12];
    int c[12];
    int len;
    
    Move() : len(0) {}
    void add(int row, int col) {
        r[len] = row;
        c[len] = col;
        len++;
    }
};

class BoardCPP {
public:
    int grid[8][8];

    // Board in CPP is one-dimensional for efficiency.
    // However this makes the code annoying as hell to look at.
    BoardCPP(int flat_board[64]) {
        for (int i = 0; i < 64; i++) {
            grid[i / 8][i % 8] = flat_board[i];
        }
    }

    // Is the piece on the board?
    bool is_on_board(int r, int c) {
        return r >= 0 && r < 8 && c >= 0 && c < 8;
    }

    // Is the piece a player piece?
    bool is_player_piece(int piece, int player) {
        if (player == WHITE) return piece == WHITE || piece == WHITE_KING;
        return piece == BLACK || piece == BLACK_KING;
    }

    // Is the piece able to move uni or bi-directional?
    std::vector<std::pair<int, int>> get_directions(int piece) {
        if (piece == WHITE) return {{-1, -1}, {-1, 1}};
        if (piece == BLACK) return {{1, -1}, {1, 1}};
        if (piece == WHITE_KING || piece == BLACK_KING) return {{-1, -1}, {-1, 1}, {1, -1}, {1, 1}};
        return {};
    }

    // Make a move (selected from minimax best move)
    void make_move(Move m) {
        int start_r = m.r[0], start_c = m.c[0];
        int end_r = m.r[m.len - 1], end_c = m.c[m.len - 1];
        int piece = grid[start_r][start_c];

        // Actually move the piece, make previous square empty
        grid[start_r][start_c] = EMPTY;
        grid[end_r][end_c] = piece;

        for (int i = 0; i < m.len - 1; i++) {
            int r1 = m.r[i], c1 = m.c[i];
            int r2 = m.r[i+1], c2 = m.c[i+1];
            if (std::abs(r1 - r2) == 2) {
                grid[(r1 + r2) / 2][(c1 + c2) / 2] = EMPTY;
            }
        }

        if (piece == WHITE && end_r == 0) grid[end_r][end_c] = WHITE_KING;
        else if (piece == BLACK && end_r == 7) grid[end_r][end_c] = BLACK_KING;
    }

    // Finds valid jumps from a selected position.
    // We need a current_path variable in the case of multiple jumps.
    void find_jumps(int r, int c, Move current_path, std::vector<Move>& all_jumps, BoardCPP state) {
        int piece = state.grid[r][c];
        int player = (piece == WHITE || piece == WHITE_KING) ? WHITE : BLACK;
        bool found_jump = false;

        // Check for jumps in valid directions
        for (auto dir : get_directions(piece)) { 
            // mr, mc = middle row, middle column (piece to jump over)
            // lr, lc = land row, land column (where we land)
            int mr = r + dir.first, mc = c + dir.second;
            int lr = r + 2 * dir.first, lc = c + 2 * dir.second;

            // If the new position is on the board, let's calculate the jump
            if (is_on_board(lr, lc)) {
                int mid_piece = state.grid[mr][mc];
                bool is_opponent = (player == WHITE) ? (mid_piece == BLACK || mid_piece == BLACK_KING) 
                                                     : (mid_piece == WHITE || mid_piece == WHITE_KING);
                
                // If middle piece is an opponent piece, and the landing spot is empty,
                // we can jump!
                if (is_opponent && state.grid[lr][lc] == EMPTY) {
                    found_jump = true;
                    BoardCPP temp = state;
                    temp.grid[lr][lc] = piece;
                    temp.grid[mr][mc] = EMPTY;
                    temp.grid[r][c] = EMPTY;

                    bool became_king = (player == WHITE && lr == 0) || (player == BLACK && lr == 7);
                    Move next_path = current_path;
                    next_path.add(lr, lc);

                    if ((piece == WHITE || piece == BLACK) && became_king) {
                        all_jumps.push_back(next_path);
                    } else {
                        // We have to recurse, in case there is a multi-jump here
                        find_jumps(lr, lc, next_path, all_jumps, temp);
                    }
                }
            }
        }
        if (!found_jump && current_path.len > 1) {
            all_jumps.push_back(current_path);
        }
    }

    // Function to get all our legal moves
    std::vector<Move> get_legal_moves(int player) {
        std::vector<Move> jumps;
        std::vector<Move> slides;

        for (int r = 0; r < 8; r++) {
            for (int c = 0; c < 8; c++) {
                int piece = grid[r][c];
                if (is_player_piece(piece, player)) {
                    // Check jumps
                    Move start_path;
                    start_path.add(r, c);
                    find_jumps(r, c, start_path, jumps, *this);

                    // Check slides if no jumps found globally yet
                    if (jumps.empty()) {
                        for (auto dir : get_directions(piece)) {
                            int nr = r + dir.first, nc = c + dir.second;
                            if (is_on_board(nr, nc) && grid[nr][nc] == EMPTY) {
                                Move m; m.add(r, c); m.add(nr, nc);
                                slides.push_back(m);
                            }
                        }
                    }
                }
            }
        }
        return jumps.empty() ? slides : jumps;
    }

    // Our evaulation function.
    // Currently rewards players keeping pieces or upgrading to king.
    // Also rewards being in the middle of the board.
    int evaluate(int maximizing_player) {
        int p1 = 0, p2 = 0;
        for (int r = 0; r < 8; r++) {
            for (int c = 0; c < 8; c++) {
                int piece = grid[r][c];
                if (piece == EMPTY) continue;

                int score = 0;
                if (piece == BLACK || piece == WHITE) {
                    score = 10;
                    score += (piece == BLACK) ? r : (7 - r);
                } else if (piece == BLACK_KING || piece == WHITE_KING) {
                    score = 25;
                    if (r >= 2 && r <= 5 && c >= 2 && c <= 5) score += 3;
                }

                if (is_player_piece(piece, maximizing_player)) p1 += score;
                else p2 += score;
            }
        }
        return p1 - p2;
    }
};

// MINIMAX LOGIC
int alpha_beta(BoardCPP board, int depth, int alpha, int beta, bool is_max, int max_player) {
    int current_turn = is_max ? max_player : (max_player == BLACK ? WHITE : BLACK);
    std::vector<Move> moves = board.get_legal_moves(current_turn);

    // Move ordering optimization
    std::sort(moves.begin(), moves.end(), [](const Move& a, const Move& b) {
        return std::abs(a.r[0] - a.r[1]) == 2 > std::abs(b.r[0] - b.r[1]) == 2;
    });

    if (depth == 0 || moves.empty()) {
        if (moves.empty()) return is_max ? -999999 : 999999;
        return board.evaluate(max_player);
    }

    if (is_max) {
        int max_eval = -999999; // -infinity
        for (Move m : moves) {
            BoardCPP sim = board;
            sim.make_move(m);
            int eval = alpha_beta(sim, depth - 1, alpha, beta, false, max_player);
            max_eval = std::max(max_eval, eval);
            alpha = std::max(alpha, eval);
            if (beta <= alpha) break;
        }
        return max_eval;
    } else {
        int min_eval = 999999; // infinity
        for (Move m : moves) {
            BoardCPP sim = board;
            sim.make_move(m);
            int eval = alpha_beta(sim, depth - 1, alpha, beta, true, max_player);
            min_eval = std::min(min_eval, eval);
            beta = std::min(beta, eval);
            if (beta <= alpha) break;
        }
        return min_eval;
    }
}

// Python to C API 
extern "C" {
    // Here is where we pass in our flat_board for lower memory usage.
    void get_best_move_c(int* flat_board, int max_player, int depth, bool random_ties, Move* out_move) {
        BoardCPP root(flat_board);
        std::vector<Move> moves = root.get_legal_moves(max_player);
        
        if (moves.empty()) {
            out_move->len = 0;
            return;
        }

        std::vector<Move> best_moves;
        int best_eval = -999999;
        int alpha = -999999; // The player who calls this function will always be alpha (maximizing player)

        // Loop through all available moves, run alpha beta pruning on the branches
        for (Move m : moves) {
            BoardCPP sim = root;
            sim.make_move(m);
            // Calls our main minimax function with pruning
            int eval = alpha_beta(sim, depth - 1, alpha, 999999, false, max_player);

            // Save the best move
            if (eval > best_eval) {
                best_eval = eval;
                best_moves.clear();
                best_moves.push_back(m);
            } else if (eval == best_eval) {
                // We CAN have multiple best moves, so can either pick first move or randomly
                best_moves.push_back(m);
            }
            alpha = std::max(alpha, best_eval);
        }

        // Randomize best move
        if (random_ties && !best_moves.empty()) {
            srand(time(NULL));
            *out_move = best_moves[rand() % best_moves.size()];
        } else {
            // Otherwise just choose first best move
            *out_move = best_moves[0];
        }
    }
}
