import tkinter as tk
import random

# Grid and UI settings
GRID_SIZE = 4  # 4x4 grid
CELL_SIZE = 120
PADDING = 10
FONT = ("Verdana", 24, "bold")
BACKGROUND_COLOR = "#ffeaf4"      
EMPTY_CELL_COLOR = "#fff5fb"      

TILE_COLORS = {
    0: "#fff5fb",        # empty
    2: "#fbc4e7",       # pale pink
    4: "#ffe0f0",        # soft rose
    8: "#f9add3",        # pastel pink
    16: "#f6a0c7",       # light blush
    32: "#e499b8",       # soft magenta
    64: "#d891c6",       # lavender rose
    128: "#e6b4f0",      # lilac
    256: "#d9a4f5",      # light purple
    512: "#c38df2",      # orchid
    1024: "#b38cf2",     # lavender purple
    2048: "#a377e9",     # violet
    4096: "#dcb3f0",     # bonus pastel lavender
}
