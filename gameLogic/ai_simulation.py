import tkinter as tk
import random
import copy
from mainGameLogic import GameLogic

from utilities import GRID_SIZE, BACKGROUND_COLOR, CELL_SIZE, TILE_COLORS, PADDING, FONT

class Game2048AI(GameLogic):
    def __init__(self, board):
        self.board = copy.deepcopy(board)

    def move(self, direction):
        if direction == 'Up':
            return self.move_vertical(self.board, up=True)
        elif direction == 'Down':
            return self.move_vertical(self.board, up=False)
        elif direction == 'Left':
            return self.move_horizontal(self.board, left=True)
        elif direction == 'Right':
            return self.move_horizontal(self.board, left=False)
        return False

    def heuristic(self):
        empty_cells = sum(row.count(0) for row in self.board)
        max_tile = max(max(row) for row in self.board)
        return empty_cells + 0.1 * max_tile