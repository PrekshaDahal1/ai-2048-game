import numpy as np
import random

class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.score = 0
        self.reset()

    def reset(self):
        self.board.fill(0)
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()
        return self.board.copy()

    def add_random_tile(self):
        empty_cells = list(zip(*np.where(self.board == 0)))
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row, col] = 4 if random.random() < 0.1 else 2

    def can_move(self):
        if np.any(self.board == 0):
            return True
        for row in range(self.size):
            for col in range(self.size - 1):
                if self.board[row, col] == self.board[row, col + 1]:
                    return True
        for col in range(self.size):
            for row in range(self.size - 1):
                if self.board[row, col] == self.board[row + 1, col]:
                    return True
        return False

    def move(self, direction):
        original_board = self.board.copy()
        if direction == 'Up':
            self.board = self._move_up(self.board)
        elif direction == 'Down':
            self.board = self._move_down(self.board)
        elif direction == 'Left':
            self.board = self._move_left(self.board)
        elif direction == 'Right':
            self.board = self._move_right(self.board)
        else:
            return False
        changed = not np.array_equal(original_board, self.board)
        if changed:
            self.add_random_tile()
        return changed

    def _move_left(self, board):
        new_board = np.zeros_like(board)
        score_gained = 0
        for i in range(self.size):
            filtered = board[i][board[i] != 0]
            merged = []
            j = 0
            while j < len(filtered):
                if j + 1 < len(filtered) and filtered[j] == filtered[j + 1]:
                    merged.append(filtered[j] * 2)
                    score_gained += filtered[j] * 2
                    j += 2
                else:
                    merged.append(filtered[j])
                    j += 1
            merged += [0] * (self.size - len(merged))
            new_board[i] = merged
        self.score += score_gained
        return new_board

    def _move_right(self, board):
        reversed_board = np.flip(board, axis=1)
        moved = self._move_left(reversed_board)
        return np.flip(moved, axis=1)

    def _move_up(self, board):
        transposed = board.T
        moved = self._move_left(transposed)
        return moved.T

    def _move_down(self, board):
        transposed = board.T
        reversed_transposed = np.flip(transposed, axis=1)
        moved = self._move_left(reversed_transposed)
        return np.flip(moved, axis=1).T

    def is_game_over(self):
        return not self.can_move()

    def get_score(self):
        return self.score

    def get_board(self):
        return self.board.copy()
