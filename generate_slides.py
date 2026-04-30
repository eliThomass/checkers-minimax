import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def generate_slide_graphics(csv_file="checkers_benchmark_results_no_tie_breaks.csv"):
    # Load data 
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: Could not find {csv_file}")
        return

    # Group by depth
    depths = sorted(df['Test_Depth'].unique())
    
    avg_times = []
    test_wins = []
    draws = []
    boss_wins = []

    for d in depths:
        group = df[df['Test_Depth'] == d]
        avg_times.append(group['Test_Avg_Turn_Time_Sec'].mean())
        
        # Count outcomes
        w = len(group[group['Winner'] == 'TEST_AI'])
        dr = len(group[group['Winner'] == 'DRAW'])
        bw = len(group[group['Winner'] == 'BOSS_AI'])
        
        # Convert to percentages
        total = w + dr + bw
        test_wins.append((w / total) * 100)
        draws.append((dr / total) * 100)
        boss_wins.append((bw / total) * 100)

    # PLOT 1: TIME COMPLEXITY 
    plt.style.use('seaborn-v0_8-darkgrid')
    fig1, ax1 = plt.subplots(figsize=(8, 6), dpi=300)     

    ax1.plot(depths, avg_times, marker='o', color='#E63946', linewidth=3, markersize=8)
    ax1.fill_between(depths, avg_times, color='#E63946', alpha=0.1)
    
    ax1.set_title("Time Complexity: Turn Time vs Search Depth", fontsize=16, fontweight='bold', pad=15)
    ax1.set_xlabel("Test AI Search Depth (Plies)", fontsize=14)
    ax1.set_ylabel("Average Turn Time (Seconds)", fontsize=14)
    ax1.set_xticks(depths)
    ax1.tick_params(axis='both', labelsize=12)
    
    plt.tight_layout()
    fig1.savefig("slide_graph_time.png")
    print("Saved 'slide_graph_time.png'")

    # PLOT 2: OUTCOMES 
    fig2, ax2 = plt.subplots(figsize=(8, 6), dpi=300)
    
    bar_width = 0.6
    # Stack the bars: Boss Wins (Losses) on bottom, Draws in middle, Test Wins on top
    p1 = ax2.bar(depths, boss_wins, bar_width, color='#457B9D', label='Boss AI Wins (Loss)')
    p2 = ax2.bar(depths, draws, bar_width, bottom=boss_wins, color='#F4A261', label='Draws')
    
    bottom_for_wins = np.add(boss_wins, draws).tolist()
    p3 = ax2.bar(depths, test_wins, bar_width, bottom=bottom_for_wins, color='#2A9D8F', label='Test AI Wins')

    ax2.set_title("Intelligence Scaling: Match Outcomes by Depth", fontsize=16, fontweight='bold', pad=15)
    ax2.set_xlabel("Test AI Search Depth (Plies)", fontsize=14)
    ax2.set_ylabel("Outcome Percentage (%)", fontsize=14)
    ax2.set_xticks(depths)
    ax2.tick_params(axis='both', labelsize=12)
    
    # Put legend outside the plot area so it doesn't cover data
    ax2.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
    
    plt.tight_layout()
    fig2.savefig("slide_graph_outcomes.png", bbox_inches='tight')
    print("Saved 'slide_graph_outcomes.png'")

if __name__ == "__main__":
    generate_slide_graphics()
