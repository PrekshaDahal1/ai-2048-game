import tkinter as tk
import random
from collections import Counter

from utilities import GRID_SIZE, BACKGROUND_COLOR, CELL_SIZE, TILE_COLORS, PADDING, FONT
from ai_simulation import Game2048AI

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")
        self.root.geometry(f"{GRID_SIZE * CELL_SIZE + 100}x{GRID_SIZE * CELL_SIZE + 100}")

        frame = tk.Frame(self.root)
        frame.pack()

        self.canvas = tk.Canvas(frame, width=GRID_SIZE * CELL_SIZE,
                                height=GRID_SIZE * CELL_SIZE, bg=BACKGROUND_COLOR)
        self.canvas.pack()

        btn = tk.Button(self.root, text="AI Move", command=self.auto_play)
        btn.pack(pady=10)

        eval_btn = tk.Button(self.root, text="Run 50 AI Games", command=self.start_auto_evaluate)
        eval_btn.pack(pady=10)

        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.add_random_tile()
        self.add_random_tile()
        self.draw_board()

        self.root.bind("<Key>", self.key_handler)

        self.auto_runs = 0
        self.max_auto_runs = 50
        self.auto_scores = []
        self.auto_max_tiles = []

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
                self.show_game_over()

    def move_horizontal(self, left=True):
        moved = False
        for i in range(GRID_SIZE):
            row = self.board[i]
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
            self.board[i] = row
        return moved

    def move_vertical(self, up=True):
        moved = False
        for j in range(GRID_SIZE):
            col = [self.board[i][j] for i in range(GRID_SIZE)]
            original = list(col)
            if not up:
                col = col[::-1]
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

    def get_best_move(self):
        directions = ['Up', 'Down', 'Left', 'Right']
        best_score = -float('inf')
        best_direction = None

        for direction in directions:
            temp_game = Game2048AI(self.board)
            moved = temp_game.move(direction)
            if moved:
                score = temp_game.heuristic()
                if score > best_score:
                    best_score = score
                    best_direction = direction
        return best_direction

    def auto_play(self):
        direction = self.get_best_move()
        if direction:
            if direction == "Up":
                self.move_vertical(up=True)
            elif direction == "Down":
                self.move_vertical(up=False)
            elif direction == "Left":
                self.move_horizontal(left=True)
            elif direction == "Right":
                self.move_horizontal(left=False)
            self.add_random_tile()
            self.draw_board()
            if self.can_move():
                self.root.after(300, self.auto_play)
            else:
                self.show_game_over()

    def show_game_over(self):
        self.canvas.create_text(GRID_SIZE * CELL_SIZE / 2, GRID_SIZE * CELL_SIZE / 2,
                                text="Game Over!", font=("Verdana", 32, "bold"), fill="red")

    def reset_game(self):
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.add_random_tile()
        self.add_random_tile()
        self.draw_board()

    def start_auto_evaluate(self):
        self.auto_runs = 0
        self.auto_scores = []
        self.auto_max_tiles = []
        self.run_single_game()

    def run_single_game(self):
        if self.auto_runs >= self.max_auto_runs:
            self.show_auto_results()
            return

        self.reset_game()
        self.root.after(500, self.auto_play_once)

    def auto_play_once(self):
        if not self.can_move():
            self.auto_scores.append(sum(map(sum, self.board)))
            self.auto_max_tiles.append(max(map(max, self.board)))
            self.auto_runs += 1
            self.root.after(300, self.run_single_game)
            return

        direction = self.get_best_move()
        if direction:
            if direction == "Up":
                self.move_vertical(up=True)
            elif direction == "Down":
                self.move_vertical(up=False)
            elif direction == "Left":
                self.move_horizontal(left=True)
            elif direction == "Right":
                self.move_horizontal(left=False)
            self.add_random_tile()
            self.draw_board()
            self.root.after(100, self.auto_play_once)

    def show_auto_results(self):
        avg_score = sum(self.auto_scores) / len(self.auto_scores)
        max_tile_counts = Counter(self.auto_max_tiles)
        result_text = f"Average Score: {avg_score:.2f}\n"
        for tile in sorted(max_tile_counts):
            percent = 100 * max_tile_counts[tile] / self.max_auto_runs
            result_text += f"Reached {tile}: {percent:.2f}% of the time\n"

        result_win = tk.Toplevel(self.root)
        result_win.title("AI Evaluation Results")
        tk.Label(result_win, text=result_text, font=("Verdana", 14), justify="left").pack(padx=20, pady=20)

if __name__ == "__main__":
    import sys
    if "--evaluate" in sys.argv:
        print("Visual evaluation not available in CLI mode. Launch the GUI to see it.")
    else:
        root = tk.Tk()
        game = Game2048(root)
        root.mainloop()
