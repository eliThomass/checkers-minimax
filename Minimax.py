import ctypes
import os
import random

# Get library extension
ext = '.so'
lib_path = os.path.join(os.path.dirname(__file__), f'engine{ext}')

# Load the C++ Shared Library
try:
    engine = ctypes.CDLL(lib_path)
except OSError:
    print(f"ERROR: Could not find compiled C++ engine ({lib_path}).")
    print("Please compile engine.cpp into a shared library first.")
    exit()

# Define the C-Struct equivalent for Move
class CMove(ctypes.Structure):
    _fields_ = [
        ("r", ctypes.c_int * 12),
        ("c", ctypes.c_int * 12),
        ("len", ctypes.c_int)
    ]

# Setup the input/output types for the exported C function
engine.get_best_move_c.argtypes = [
    ctypes.POINTER(ctypes.c_int), # flat_board
    ctypes.c_int,                 # max_player
    ctypes.c_int,                 # depth
    ctypes.c_bool,                # random_ties
    ctypes.POINTER(CMove),        # out_move (pointer to write the answer to)
    ctypes.c_int                  # eval score
]
engine.get_best_move_c.restype = None


class Minimax:
    def __init__(self, max_depth=5, random_ties=False):
        self.max_depth = max_depth
        self.random_ties = random_ties

    def get_best_move(self, board, max_player):
        """
        Flattens the Python board, passes it to C++, and translates the result.
        Returns the move as a Python list of tuples, e.g., [(2,1), (3,2)]
        """
        # Flatten the 8x8 2D Python list into a 1D C-Array of 64 ints
        flat_list = [item for sublist in board.get_board() for item in sublist]
        c_board = (ctypes.c_int * 64)(*flat_list)
        
        # Create an empty CMove struct for C++ to write the answer into
        out_move = CMove()
        score = 0
        
        # Call the C++ Engine that was compiled
        engine.get_best_move_c(
            c_board, 
            ctypes.c_int(max_player), 
            ctypes.c_int(self.max_depth), 
            ctypes.c_bool(self.random_ties), 
            ctypes.byref(out_move),
            ctypes.c_int(score)
        )
        
        # If length is 0, the AI surrendered or has no moves
        if out_move.len == 0:
            return None, None
            
        # Translate the C-Struct back into Python standard format
        python_move = []
        for i in range(out_move.len):
            python_move.append((out_move.r[i], out_move.c[i]))
            
        # Return a dummy evaluation score and the actual move sequence
        # (The C++ engine only returns the move to save memory/complexity)
        # The eval score is kinda not used, but let's keep it just for future use/reference.
        return 0, python_move
