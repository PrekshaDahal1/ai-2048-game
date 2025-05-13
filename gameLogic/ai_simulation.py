import tkinter as tk
import random
import copy

from utilities import GRID_SIZE, BACKGROUND_COLOR, CELL_SIZE, TILE_COLORS, PADDING, FONT

class Game2048AI:
    def __init__(self, board):
        self.board = copy.deepcopy(board)

    def compress(self, row):
        new_row = [num for num in row if num != 0]
        new_row += [0] * (GRID_SIZE - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(GRID_SIZE - 1):
            if row[i] != 0 and row[i] == row[i+1]:
                row[i] *= 2
                row[i+1] = 0
        return row

    def move_horizontal(self, left=True):
        moved = False
        for i in range(GRID_SIZE):
            row = self.board[i]
            if not left:
                row = row[::-1]
            new_row = self.compress(row)
            new_row = self.merge(new_row)
            new_row = self.compress(new_row)
            if not left:
                new_row = new_row[::-1]
            if new_row != self.board[i]:
                moved = True
            self.board[i] = new_row
        return moved

    def move_vertical(self, up=True):
        moved = False
        for j in range(GRID_SIZE):
            col = [self.board[i][j] for i in range(GRID_SIZE)]
            if not up:
                col = col[::-1]
            new_col = self.compress(col)
            new_col = self.merge(new_col)
            new_col = self.compress(new_col)
            if not up:
                new_col = new_col[::-1]
            for i in range(GRID_SIZE):
                if self.board[i][j] != new_col[i]:
                    moved = True
                self.board[i][j] = new_col[i]
        return moved

    def move(self, direction):
        if direction == 'Up':
            return self.move_vertical(up=True)
        elif direction == 'Down':
            return self.move_vertical(up=False)
        elif direction == 'Left':
            return self.move_horizontal(left=True)
        elif direction == 'Right':
            return self.move_horizontal(left=False)
        return False
    
    def heuristic(self):
        empty_cells = sum(row.count(0) for row in self.board)
        max_tile    = max(max(row) for row in self.board)
        return empty_cells + 0.1 * max_tile  