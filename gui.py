import pygame
import math
from Board import *
from Minimax import *

# --- GUI CONSTANTS ---
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
RED = (200, 0, 0)
WHITE_CLR = (255, 255, 255)
BLACK_CLR = (0, 0, 0)
DARK_BROWN = (101, 67, 33)
LIGHT_BROWN = (222, 184, 135)
GOLD = (255, 215, 0)
HIGHLIGHT = (0, 255, 0)
MENU_BG = (40, 40, 40)
BTN_COLOR = (70, 130, 180)
BTN_HOVER = (100, 149, 237)
BTN_ACTIVE = (46, 139, 87) # Green when selected

pygame.font.init()
FONT_LARGE = pygame.font.SysFont("arial", 50, bold=True)
FONT_MED = pygame.font.SysFont("arial", 30)
FONT_SMALL = pygame.font.SysFont("arial", 20)

# --- HELPER CLASSES & FUNCTIONS ---
class Button:
    def __init__(self, x, y, width, height, text, value=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.value = value
        self.is_hovered = False

    def draw(self, surface, is_selected=False):
        color = BTN_ACTIVE if is_selected else (BTN_HOVER if self.is_hovered else BTN_COLOR)
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE_CLR, self.rect, 2, border_radius=10) # Border
        
        text_surf = FONT_MED.render(self.text, True, WHITE_CLR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

def draw_star(surface, color, center, size):
    """Calculates points for a 5-pointed star and draws it."""
    points = []
    for i in range(10):
        angle = i * math.pi / 5 - math.pi / 2
        r = size if i % 2 == 0 else size / 2.5
        x = center[0] + r * math.cos(angle)
        y = center[1] + r * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)

def draw_board(win, board_obj, selected_square, valid_moves):
    """Draws the grid, highlights, and pieces based on the Board object."""
    win.fill(BLACK_CLR)
    
    # 1. Draw Squares
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
    # 2. Draw Highlights
    if selected_square:
        r, c = selected_square
        pygame.draw.rect(win, HIGHLIGHT, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)
        
    for move in valid_moves:
        end_r, end_c = move[-1]
        pygame.draw.circle(win, HIGHLIGHT, (end_c * SQUARE_SIZE + SQUARE_SIZE // 2, end_r * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    # 3. Draw Pieces
    grid = board_obj.get_board()
    for row in range(ROWS):
        for col in range(COLS):
            piece = grid[row][col]
            if piece != EMPTY:
                center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                radius = SQUARE_SIZE // 2 - 15
                
                piece_color = WHITE_CLR if piece in [WHITE, WHITE_KING] else BLACK_CLR
                pygame.draw.circle(win, piece_color, center, radius)
                
                if piece in [WHITE_KING, BLACK_KING]:
                    draw_star(win, GOLD, center, radius * 0.6)

def get_row_col_from_mouse(pos):
    x, y = pos
    return y // SQUARE_SIZE, x // SQUARE_SIZE

# --- THE MAIN MENU ---
def main_menu(win):
    """Runs a pre-game loop to gather settings, returns (game_type, depth, random_ties)"""
    run = True
    
    # Defaults
    game_type = 1 # 0: AI v AI, 1: AI v Hum, 2: Hum v Hum
    ai_depth = 10
    random_ties = True

    # Setup Buttons
    btn_ai_ai = Button(100, 200, 180, 50, "AI vs AI", 0)
    btn_ai_hu = Button(310, 200, 180, 50, "AI vs Human", 1)
    btn_hu_hu = Button(520, 200, 180, 50, "Human vs Human", 2)
    mode_btns = [btn_ai_ai, btn_ai_hu, btn_hu_hu]

    btn_depth_down = Button(250, 350, 50, 50, "-")
    btn_depth_up = Button(500, 350, 50, 50, "+")
    
    btn_rand_toggle = Button(310, 500, 180, 50, "ON")

    btn_start = Button(250, 650, 300, 70, "START GAME")

    while run:
        win.fill(MENU_BG)
        
        # Draw Text
        title = FONT_LARGE.render("CHECKERS ENGINE", True, WHITE_CLR)
        win.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        mode_txt = FONT_MED.render("Select Game Mode:", True, WHITE_CLR)
        win.blit(mode_txt, (WIDTH//2 - mode_txt.get_width()//2, 150))
        
        depth_txt = FONT_MED.render("AI Search Depth (1-20):", True, WHITE_CLR)
        win.blit(depth_txt, (WIDTH//2 - depth_txt.get_width()//2, 300))
        
        depth_val = FONT_LARGE.render(str(ai_depth), True, WHITE_CLR)
        win.blit(depth_val, (WIDTH//2 - depth_val.get_width()//2, 350))
        
        rand_txt = FONT_MED.render("AI Random Tie-Breaks:", True, WHITE_CLR)
        win.blit(rand_txt, (WIDTH//2 - rand_txt.get_width()//2, 450))

        # Get mouse position and draw buttons
        pos = pygame.mouse.get_pos()
        for btn in mode_btns:
            btn.check_hover(pos)
            btn.draw(win, is_selected=(game_type == btn.value))
            
        btn_depth_down.check_hover(pos)
        btn_depth_down.draw(win)
        
        btn_depth_up.check_hover(pos)
        btn_depth_up.draw(win)
        
        btn_rand_toggle.text = "ON" if random_ties else "OFF"
        btn_rand_toggle.check_hover(pos)
        btn_rand_toggle.draw(win, is_selected=random_ties)
        
        btn_start.check_hover(pos)
        btn_start.draw(win)

        pygame.display.update()

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Mode selection
                for btn in mode_btns:
                    if btn.is_hovered: game_type = btn.value
                
                # Depth adjustment
                if btn_depth_down.is_hovered and ai_depth > 1: ai_depth -= 1
                if btn_depth_up.is_hovered and ai_depth < 20: ai_depth += 1
                
                # Random toggle
                if btn_rand_toggle.is_hovered: random_ties = not random_ties
                
                # Start game
                if btn_start.is_hovered:
                    return game_type, ai_depth, random_ties

# --- MAIN GAME LOOP ---
def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Phase 4: Checkers Engine GUI")
    
    # 1. Run the Menu First
    game_type, ai_depth, random_ties = main_menu(win)
    
    # 2. Initialize Game Objects
    game = Board(debug=False)
    ai_bot = Minimax(max_depth=ai_depth, random_ties=random_ties) 
    
    run = True
    cur_player = WHITE # By standard rules, Black (dark) goes first, but your logic uses WHITE = Human
    selected_piece = None
    available_moves_for_player = []
    valid_moves_for_selection = []

    while run:
        # Determine who controls this turn
        is_human_turn = False
        if game_type == 2:
            is_human_turn = True
        elif game_type == 1 and cur_player == WHITE:
            is_human_turn = True

        # Check for game over
        available_moves_for_player = game.get_legal_moves(cur_player)
        if not available_moves_for_player:
            winner = "BLACK" if cur_player == WHITE else "WHITE"
            print(f"Game Over! {winner} wins!")
            # Wait a few seconds then quit
            pygame.time.delay(3000)
            run = False
            continue

        draw_board(win, game, selected_piece, valid_moves_for_selection)
        pygame.display.update()

        # Keep pygame responsive by pumping events even during AI turns
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # --- HUMAN TURN (Event Loop) ---
            if event.type == pygame.MOUSEBUTTONDOWN and is_human_turn:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                
                # Clicked our own piece? Select it.
                if game.is_player_piece(game.get_board()[row][col], cur_player):
                    selected_piece = (row, col)
                    valid_moves_for_selection = [m for m in available_moves_for_player if m[0] == (row, col)]
                
                # Clicked a valid landing spot? Move it.
                elif selected_piece:
                    for move in valid_moves_for_selection:
                        if move[-1] == (row, col):
                            game.make_move(move)
                            cur_player = BLACK if cur_player == WHITE else WHITE
                            selected_piece = None
                            valid_moves_for_selection = []
                            break

        # --- AI TURN ---
        if not is_human_turn:
            # Add a visual delay so AI vs AI games don't finish in 0.2 seconds
            pygame.time.delay(500) 
            eval_score, best_move = ai_bot.get_best_move(game, cur_player)
            
            if best_move:
                game.make_move(best_move)
                cur_player = BLACK if cur_player == WHITE else WHITE

    pygame.quit()

if __name__ == "__main__":
    main()
