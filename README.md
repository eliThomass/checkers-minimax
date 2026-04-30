# Checkers Minimax Engine 

A C++/Python hybrid Checkers AI. Uses Minimax with Alpha-Beta pruning and deterministic move-ordering to achieve a 12 ply search depth.

## Setup
**Requirements:** Python 3.x, C++ Compiler (`g++`).

1. **Install Python dependencies:**
   ```bash
   pip install pygame pandas matplotlib numpy
   ```

2. **Compile the C++ Backend:**
   ```bash
   g++ -O3 -shared -fPIC -o engine.so engine.cpp
   ```
   *(Note for Windows: Compile as a `.dll` and update the `ctypes` call in `Minimax.py`)*

## Usage

* **Play the Game (GUI):** ```bash
  python3 gui.py
  ```
* **Run Automated Benchmarks:** Outputs match results and time complexities to CSV.
  ```bash
  python3 benchmark.py
  ```
* **Generate Evaluation Graphs:** Parses the CSV to create performance charts.
  ```bash
  python3 generate_graphs.py
  ```

## Architecture Summary
* `gui.py`: Pygame interactive frontend.
* `engine.cpp`: Highly optimized C++ search algorithm.
* `Minimax.py`: The `ctypes` bridge connecting the UI to the engine.
