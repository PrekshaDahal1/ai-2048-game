import tkinter as tk
import random

GRID_SIZE = 4
CELL_SIZE = 100
PADDING = 10
FONT = ("Verdana", 24, "bold")
BACKGROUND_COLOR = "#92877d"
EMPTY_CELL_COLOR = "#9e948a"
TILE_COLORS = {
    0: "#9e948a",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
}

class Game2048GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.canvas = tk.Canvas(root, bg=BACKGROUND_COLOR,
                                width=GRID_SIZE * CELL_SIZE,
                                height=GRID_SIZE * CELL_SIZE)
        self.canvas.pack()
        self.add_new_tile()
        self.add_new_tile()
        self.draw_board()
        self.root.bind("<Key>", self.key_handler)

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                self.draw_tile(i, j, self.board[i][j])

    def draw_tile(self, i, j, value):
        x0 = j * CELL_SIZE + PADDING
        y0 = i * CELL_SIZE + PADDING
        x1 = x0 + CELL_SIZE - 2 * PADDING
        y1 = y0 + CELL_SIZE - 2 * PADDING

        color = TILE_COLORS.get(value, "#3c3a32")
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        if value != 0:
            self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2,
                                    text=str(value), font=FONT, fill="#776e65")

    def add_new_tile(self):
        empty = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.board[i][j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def key_handler(self, event):
        key = event.keysym
        moved = False
        if key == "Up":
            moved = self.move_up()
        elif key == "Down":
            moved = self.move_down()
        elif key == "Left":
            moved = self.move_left()
        elif key == "Right":
            moved = self.move_right()

        if moved:
            self.add_new_tile()
            self.draw_board()
            if not self.can_move():
                self.canvas.create_text(GRID_SIZE * CELL_SIZE / 2, GRID_SIZE * CELL_SIZE / 2,
                                        text="Game Over!", font=("Verdana", 32, "bold"), fill="red")

    # Movement methods (same logic as before)
    def compress(self, row):
        new_row = [i for i in row if i != 0]
        new_row += [0] * (GRID_SIZE - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(GRID_SIZE - 1):
            if row[i] == row[i+1] and row[i] != 0:
                row[i] *= 2
                row[i+1] = 0
        return row

    def move_left(self):
        moved = False
        new_board = []
        for row in self.board:
            compressed = self.compress(row)
            merged = self.merge(compressed)
            final = self.compress(merged)
            if final != row:
                moved = True
            new_board.append(final)
        self.board = new_board
        return moved

    def move_right(self):
        self.board = [row[::-1] for row in self.board]
        moved = self.move_left()
        self.board = [row[::-1] for row in self.board]
        return moved

    def move_up(self):
        self.board = list(map(list, zip(*self.board)))
        moved = self.move_left()
        self.board = list(map(list, zip(*self.board)))
        return moved

    def move_down(self):
        self.board = list(map(list, zip(*self.board)))
        moved = self.move_right()
        self.board = list(map(list, zip(*self.board)))
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
    game = Game2048GUI(root)
    root.mainloop()
