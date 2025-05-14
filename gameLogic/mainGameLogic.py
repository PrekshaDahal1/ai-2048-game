import tkinter as tk
import random
import pickle
import numpy as np
import copy
from collections import Counter

from utilities import GRID_SIZE, BACKGROUND_COLOR, CELL_SIZE, TILE_COLORS, PADDING, FONT

class GameLogic:
    def compress(self, row):
        new_row = [num for num in row if num != 0]
        new_row += [0] * (GRID_SIZE - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(GRID_SIZE - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                row[i + 1] = 0
        return row

    def move_horizontal(self, board, left=True):
        moved = False
        for i in range(GRID_SIZE):
            row = board[i]
            original = list(row)
            if not left:
                row = row[::-1]
            row = self.compress(row)
            row = self.merge(row)
            row = self.compress(row)
            if not left:
                row = row[::-1]
            if row != original:
                moved = True
            board[i] = row
        return moved

    def move_vertical(self, board, up=True):
        moved = False
        for j in range(GRID_SIZE):
            col = [board[i][j] for i in range(GRID_SIZE)]
            original = list(col)
            if not up:
                col = col[::-1]
            col = self.compress(col)
            col = self.merge(col)
            col = self.compress(col)
            if not up:
                col = col[::-1]
            for i in range(GRID_SIZE):
                if board[i][j] != col[i]:
                    moved = True
                board[i][j] = col[i]
        return moved