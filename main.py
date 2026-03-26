from Board import *
from Minimax import *

if __name__ == "__main__":
    game = Board(debug=False) 
    minimax = Minimax()
    print(minimax.alpha)
    cur_player = BLACK

    while True:
        game.display()
        moves = game.get_legal_moves(cur_player)
        
        if not moves:
            print("Game Over! No moves left.")
            break
            
        # Display the formatted menu
        game.display_moves(moves, cur_player)
        
        # 1-indexed input loop
        try:
            choice = int(input("Select a move number (or 0 to quit): "))
            if choice == 0:
                break
            if 1 <= choice <= len(moves):
                game.make_move(moves[choice - 1])
                # Swap turns
                cur_player = WHITE if cur_player == BLACK else BLACK
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")

