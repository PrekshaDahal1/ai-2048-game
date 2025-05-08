import tkinter as tk
import random

from utilities import GRID_SIZE, BACKGROUND_COLOR, CELL_SIZE, TILE_COLORS, PADDING, FONT

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")
        self.canvas = tk.Canvas(root, width=GRID_SIZE * CELL_SIZE,
                                height=GRID_SIZE * CELL_SIZE, bg=BACKGROUND_COLOR)
        self.canvas.pack()

        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.add_random_tile()
        self.add_random_tile()
        self.draw_board()

        self.root.bind("<Key>", self.key_handler)

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.board[i][j]
                color = TILE_COLORS.get(value, "#3c3a32")
                x0 = j * CELL_SIZE + PADDING
                y0 = i * CELL_SIZE + PADDING
                x1 = x0 + CELL_SIZE - 2 * PADDING
                y1 = y0 + CELL_SIZE - 2 * PADDING
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

                if value != 0:
                    self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2,
                                            text=str(value), font=FONT, fill="#776e65")

    def add_random_tile(self):
        empty = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.board[i][j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def key_handler(self, event):
        key = event.keysym
        moved = False

        if key == "Up":
            moved = self.move_vertical(up=True)
        elif key == "Down":
            moved = self.move_vertical(up=False)
        elif key == "Left":
            moved = self.move_horizontal(left=True)
        elif key == "Right":
            moved = self.move_horizontal(left=False)

        if moved:
            self.add_random_tile()
            self.draw_board()
            if not self.can_move():
                self.canvas.create_text(GRID_SIZE * CELL_SIZE / 2, GRID_SIZE * CELL_SIZE / 2,
                                        text="Game Over!", font=("Verdana", 32, "bold"), fill="red")

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
            original = list(row)
            row = self.compress(row)
            row = self.merge(row)
            row = self.compress(row)
            if not left:
                row = row[::-1]
            if row != self.board[i]:
                moved = True
            self.board[i] = row
        return moved

    def move_vertical(self, up=True):
        moved = False
        for j in range(GRID_SIZE):
            col = [self.board[i][j] for i in range(GRID_SIZE)]
            if not up:
                col = col[::-1]
            original = list(col)
            col = self.compress(col)
            col = self.merge(col)
            col = self.compress(col)
            if not up:
                col = col[::-1]
            for i in range(GRID_SIZE):
                if self.board[i][j] != col[i]:
                    moved = True
                self.board[i][j] = col[i]
        return moved

    def can_move(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.board[i][j] == 0:
                    return True
                if j < GRID_SIZE - 1 and self.board[i][j] == self.board[i][j+1]:
                    return True
                if i < GRID_SIZE - 1 and self.board[i][j] == self.board[i+1][j]:
                    return True
        return False


if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
