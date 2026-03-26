from Board import *
from Minimax import *

if __name__ == "__main__":
    print("CHECKERS CHECKER")
    game_type = int(input("Choose game type: 0 (AI vs AI), 1 (AI vs Human), 2 (Human vs Human): "))

    ai_depth = 5
    use_random = False 

    # Only ask for AI settings if there is actually an AI playing
    if game_type in [0, 1]:
        ai_depth = int(input("Choose AI max-depth (1-10): "))
        random_input = int(input("Use randomness to break AI ties on multiple best moves? (0/1): "))
        use_random = bool(random_input)

    game = Board(debug=False) 
    minimax = Minimax(max_depth=ai_depth, random_ties=use_random) 
    
    cur_player = BLACK

    while True:
        game.display()
        moves = game.get_legal_moves(cur_player)
        player_name = "WHITE" if cur_player == WHITE else "BLACK"
        
        if not moves:
            winner = "WHITE" if cur_player == BLACK else "BLACK"
            print(f"Game Over! No moves left for {player_name}. {winner} wins!")
            break
            
        game.display_moves(moves, cur_player)
        
        # Find out who is in control of the current turn 
        is_human_turn = False
        if game_type == 2:
            is_human_turn = True
        elif game_type == 1 and cur_player == WHITE:
            is_human_turn = True # Human is white, AI is black 

        try:
            if is_human_turn:
                choice = int(input(f"[{player_name}] Select a move number (or 0 to quit): "))
                if choice == 0:
                    break
                if 1 <= choice <= len(moves):
                    game.make_move(moves[choice - 1])
                    cur_player = WHITE if cur_player == BLACK else BLACK 
                else:
                    print("Invalid choice. Try again.")
                    
            else:
                print(f"AI ({player_name}) is thinking...")
                
                # Pass the game and the current player to the AI
                best_move = minimax.get_best_move(game, cur_player)

                
                if best_move:
                    game.make_move(best_move[1])
                    cur_player = WHITE if cur_player == BLACK else BLACK 
                else:
                    print(f"AI ({player_name}) could not find a move. You win!")
                    break

        except ValueError:
            print("Please enter a valid number.")
