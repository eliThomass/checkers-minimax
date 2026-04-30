import pandas as pd

def analyze_results(csv_file="checkers_benchmark_results.csv"):
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: Could not find '{csv_file}'. Run the benchmark script first!")
        return


    print("=== Benchmark Results ===") 

    grouped = df.groupby('Test_Depth')

    for depth, group in grouped:
        total_games = len(group)
        boss_depth = group['Boss_Depth'].iloc[0]
        
        wins = len(group[group['Winner'] == 'TEST_AI'])
        draws = len(group[group['Winner'] == 'DRAW'])
        losses = len(group[group['Winner'] == 'BOSS_AI'])
        
        avg_time = group['Test_Avg_Turn_Time_Sec'].mean()
        avg_turns = group['Total_Turns'].mean()
        
        print(f"Depth {depth} (vs Boss Depth {boss_depth}) | Total Games: {total_games}")
        print(f"  Win Rate:  {(wins/total_games)*100:>5.1f}%")
        print(f"  Draw Rate: {(draws/total_games)*100:>5.1f}%")
        print(f"  Loss Rate: {(losses/total_games)*100:>5.1f}%")
        print(f"  Avg Turn Time:   {avg_time:.4f} seconds")
        print(f"  Avg Total Turns: {avg_turns:.1f} turns")
        print("-" * 45)

if __name__ == "__main__":
    analyze_results()
