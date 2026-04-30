import time
import csv
from Board import *
from Minimax import *

def run_benchmarks_extension():
    filename = "checkers_benchmark_results_no_tie_breaks.csv"

    boss_depth = 10
    games_per_depth = 2
    max_turns_per_game = 150

    # CHANGED: 'a' mode appends to the file instead of overwriting ('w')
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # CHANGED: Removed the header row writer so we don't inject text into the data columns

        print(f"=== RESUMING AI BENCHMARK ===")
        print(f"Appending Depths 13 and 14 to {filename}\n")

        # CHANGED: Only loop through 13 and 14
        for test_depth in range(13, 15):
            print(f"--- INITIATING DEPTH {test_depth} vs DEPTH {boss_depth} ---")
            
            for game_num in range(1, games_per_depth + 1):
                test_ai = Minimax(max_depth=test_depth, random_ties=False)
                boss_ai = Minimax(max_depth=boss_depth, random_ties=False)
                game = Board(debug=False)
                
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
                    
                    if test_turns + boss_turns >= max_turns_per_game:
                        winner_name = "DRAW"
                        break

                    start_time = time.time()
                    
                    if cur_player == test_color:
                        _, best_move = test_ai.get_best_move(game, cur_player)
                        test_total_time += (time.time() - start_time)
                        test_turns += 1
                    else:
                        _, best_move = boss_ai.get_best_move(game, cur_player)
                        boss_total_time += (time.time() - start_time)
                        boss_turns += 1
                        
                    if best_move:
                        game.make_move(best_move)
                        cur_player = WHITE if cur_player == BLACK else BLACK
                    else:
                        winner_val = WHITE if cur_player == BLACK else BLACK
                        winner_name = "TEST_AI" if winner_val == test_color else "BOSS_AI"
                        break
                
                test_avg = test_total_time / test_turns if test_turns > 0 else 0
                boss_avg = boss_total_time / boss_turns if boss_turns > 0 else 0
                
                color_str = "BLACK" if test_color == BLACK else "WHITE"
                
                writer.writerow([
                    test_depth, boss_depth, game_num, color_str, winner_name, 
                    round(test_avg, 4), round(boss_avg, 4), test_turns + boss_turns
                ])
                file.flush() 
                
                print(f"Depth {test_depth} | Game {game_num}/2 | Test as {color_str} | Winner: {winner_name} | Test Avg: {round(test_avg, 3)}s")

if __name__ == "__main__":
    run_benchmarks_extension()
