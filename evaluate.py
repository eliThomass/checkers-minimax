import time
import csv
from Board import *
from Minimax import *

def run_benchmarks():
    filename = "checkers_benchmark_results_no_tie_breaks.csv"

    # We will test depths 1-13 on this "boss" depth
    boss_depth = 10
    games_per_depth = 2

    # In case the AI's refuse to end
    max_turns_per_game = 150

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Test_Depth", "Boss_Depth", "Game_Number", "Test_Color", "Winner", "Test_Avg_Turn_Time_Sec", "Boss_Avg_Turn_Time_Sec", "Total_Turns"])

        print(f"=== STARTING AI BENCHMARK ===")
        print(f"Results will be saved in real-time to {filename}\n")

        # Loop through depths 1 to 13
        for test_depth in range(1, 14):
            print(f"--- INITIATING DEPTH {test_depth} vs DEPTH {boss_depth} ---")
            
            for game_num in range(1, games_per_depth + 1):
                # Turned off random tie-break (having it on resulted in a washout effect, lowering performance)
                test_ai = Minimax(max_depth=test_depth, random_ties=False)
                boss_ai = Minimax(max_depth=boss_depth, random_ties=False)
                game = Board(debug=False)
                
                # Alternate who goes first for fairness
                test_color = BLACK if game_num % 2 != 0 else WHITE
                boss_color = WHITE if test_color == BLACK else BLACK
                
                cur_player = BLACK
                
                test_total_time = 0
                boss_total_time = 0
                test_turns = 0
                boss_turns = 0
                
                while True:
                    moves = game.get_legal_moves(cur_player)
                    
                    if not moves:
                        winner_val = WHITE if cur_player == BLACK else BLACK
                        winner_name = "TEST_AI" if winner_val == test_color else "BOSS_AI"
                        break
                    
                    # If no one can end the game, just declare a draw
                    if test_turns + boss_turns >= max_turns_per_game:
                        winner_name = "DRAW"
                        break

                    start_time = time.time()
                    
                    # Evaluate the move
                    if cur_player == test_color:
                        _, best_move = test_ai.get_best_move(game, cur_player)
                        test_total_time += (time.time() - start_time)
                        test_turns += 1
                    else:
                        _, best_move = boss_ai.get_best_move(game, cur_player)
                        boss_total_time += (time.time() - start_time)
                        boss_turns += 1
                        
                    # Execute the move
                    if best_move:
                        game.make_move(best_move)
                        cur_player = WHITE if cur_player == BLACK else BLACK
                    else:
                        winner_val = WHITE if cur_player == BLACK else BLACK
                        winner_name = "TEST_AI" if winner_val == test_color else "BOSS_AI"
                        break
                
                # Calculate averages
                test_avg = test_total_time / test_turns if test_turns > 0 else 0
                boss_avg = boss_total_time / boss_turns if boss_turns > 0 else 0
                
                color_str = "BLACK" if test_color == BLACK else "WHITE"
                
                writer.writerow([
                    test_depth, boss_depth, game_num, color_str, winner_name, 
                    round(test_avg, 4), round(boss_avg, 4), test_turns + boss_turns
                ])
                file.flush() 
                
                # CLI Feedback
                print(f"Depth {test_depth} | Game {game_num}/2 | Test as {color_str} | Winner: {winner_name} | Test Avg: {round(test_avg, 3)}s")

if __name__ == "__main__":
    run_benchmarks()
